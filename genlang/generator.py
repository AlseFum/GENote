from typing import Any, Dict, List, Optional, Sequence
import ast
import json
import operator as op
import random

__all__ = ["generate_from_json"]

def eval_prob_expression(expr: Any, variables: Dict[str, Any], rng: random.Random) -> Any:
    if isinstance(expr, (int, float, bool)):
        return expr
    if not isinstance(expr, str):
        return expr
    tree = ast.parse(expr, mode="eval")

    _BIN = {ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul, ast.Div: op.truediv,
            ast.FloorDiv: op.floordiv, ast.Mod: op.mod, ast.Pow: op.pow}
    _BOOL = {ast.And: all, ast.Or: any}
    _CMP = {ast.Eq: op.eq, ast.NotEq: op.ne, ast.Lt: op.lt, ast.LtE: op.le, ast.Gt: op.gt, ast.GtE: op.ge}

    def ev(node: ast.AST) -> Any:
        if isinstance(node, ast.Constant):
            return node.value
        if isinstance(node, ast.Name):
            return variables.get(node.id)
        if isinstance(node, ast.BinOp) and type(node.op) in _BIN:
            return _BIN[type(node.op)](ev(node.left), ev(node.right))
        if isinstance(node, ast.BoolOp) and type(node.op) in _BOOL:
            vals = [bool(ev(v)) for v in node.values]
            return _BOOL[type(node.op)](vals)
        if isinstance(node, ast.UnaryOp):
            if isinstance(node.op, ast.Not):
                return not ev(node.operand)
            if isinstance(node.op, ast.UAdd):
                return +ev(node.operand)
            if isinstance(node.op, ast.USub):
                return -ev(node.operand)
        if isinstance(node, ast.Compare):
            left = ev(node.left)
            for o, comp in zip(node.ops, node.comparators):
                right = ev(comp)
                if type(o) not in _CMP or not _CMP[type(o)](left, right):
                    return False
                left = right
            return True
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            fn = node.func.id
            if fn == "rand":
                args = [ev(a) for a in node.args]
                if not args:
                    return rng.randrange(0, 1_000_000)
                n = int(args[0])
                return 0 if n <= 0 else rng.randrange(0, n)
            if fn == "randf":
                return rng.random()
            raise ValueError("Unsupported function")
        if isinstance(node, ast.IfExp):
            return ev(node.body) if bool(ev(node.test)) else ev(node.orelse)
        if isinstance(node, ast.List):
            return [ev(e) for e in node.elts]
        if isinstance(node, ast.Tuple):
            return tuple(ev(e) for e in node.elts)
        if isinstance(node, ast.Dict):
            return {ev(k): ev(v) for k, v in zip(node.keys, node.values)}
        raise ValueError(f"Unsupported node: {type(node).__name__}")

    return ev(tree.body)
class MRng:
    def random(self):
        import secrets
        return secrets.randbits(16) /65535 # 0~65535
def choose_option(options,
                   variables,
                   rng: random.Random) -> Optional[int]:
    weights: List[float] = []
    for opt in options:
        w = eval_prob_expression(opt.get("prob",1), variables, rng)
        weights.append(max(0.0, w))
    total = sum(weights)
    if total <= 0:
        return None
 
    r =rng.random()*total
    acc = 0.0
    for i, w in enumerate(weights):
        acc += w
        if r <= acc:
            return i
    return len(options) - 1


def expand_option(opt: List[Dict[str, Any]], 
                  rules: Dict[str, List[List[Dict[str, Any]]]], 
                  variables: Dict[str, Any], 
                  rng: random.Random, depth: int) -> str:
    parts: List[str] = []

    for el in opt.get("elems",[]):
        print(f"[el]{el}")
        t = el.get("type")
        if t is None:
            # 只有 prob 的权重元素，忽略输出
            continue
        if t == "terminal" or t == "t":
            parts.append(str(el.get("value", "")))
        elif t == "ref" or t == "r":
            ref = str(el.get("ref", ""))
            parts.append(expand_nonterminal(ref, rules, variables, rng, depth))
        else:
            print(f"unknown type {t}")
            parts.append(str(el))
    return "".join(parts)


def expand_nonterminal(name: str, 
                       rules: Dict[str, List[List[Dict[str, Any]]]], 
                       variables: Dict[str, Any], 
                       rng: random.Random, depth: int) -> str:
    if depth <= 0:
        return "<stop for too deep>"
    options = rules.get(name)
    if not options:
        return name
    idx = choose_option(options, variables, rng)
    if idx is None:
        return ""
    return   expand_option(options[idx], rules, variables, rng, depth - 1)


def generate_from_json(
    data: Any,
    start: Optional[str] = None,
    variables: Optional[Dict[str, Any]] = None
) -> str:
    if isinstance(data, str):
        data = json.loads(data)
    rules = data.get("rules") if isinstance(data.get("rules"), dict) else {}
    
    vars_final: Dict[str, Any] = {}
    if isinstance(data.get("variables"), dict):
        vars_final.update(data["variables"])
    if variables:
        vars_final.update(variables)

    # 选择开始符号：优先参数 start；否则 data.start；否则 "START"；再否则第一个规则名
    start_symbol: Optional[str] = None
    if isinstance(start, str) and start:
        start_symbol = start
    elif isinstance(data.get("start"), str) and data.get("start"):
        start_symbol = data.get("start")
    elif "START" in rules:
        start_symbol = "START"
    else:
        # 取第一个规则名（Python 3.7+ 字典有序）
        start_symbol = next(iter(rules.keys()), None)
        if not start_symbol:
            raise ValueError("rules is empty; no start symbol can be determined")
    return expand_nonterminal(start_symbol, rules, vars_final, MRng(), depth=128)


