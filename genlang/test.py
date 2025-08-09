from generator import generate_from_json


def main() -> None:
    # 基本示例（schema-like JSON）
    schema = {
        "rules": {
            "nihao": [
                {"elems": [ {"type": 'terminal',"value": 'a' } ] },
                {
                "elems": [
                    {"type": 'terminal', "value": 'B1' },
                    { "type": 'ref', "ref": 'B2' }
                ]
                },
                { "elems": [ { "type": 'terminal', "value": 'OP' } ] }
            ],
            "b": [
                {
                "elems": [
                    { "type": 'terminal', "value": 'c' },
                    { "type": 'terminal', "value": 'asf' }
                ]
                }
            ]
        },
        "start": "nihao",
    }

    text = generate_from_json(schema, seed=42)
    print("示例1:", text)

    # # 表达式 + 变量示例
    # schema_expr = {
    #     "rules": {
    #         "START": [[{"expr": "N * 2"}, {"ref": "p"}]],
    #         "p": [
    #             [{"prob": 0.5}, "p"],
    #             [{"prob": 0.5}, "q"],
    #         ],
    #         "q": [
    #             [{"prob": 0.5}, "q"],
    #             [{"prob": 0.5}, "r"],
    #         ],
    #         "r": [["r"]],
    #     },
    #     "start": "START",
    #     "variables": {"N": 3},
    # }
    # text2 = generate_from_json(schema_expr)  # 使用内置 variables
    # print("示例2:", text2)

    # text3 = generate_from_json(schema_expr, variables={"N": 5})  # 覆盖变量
    # print("示例3:", text3)

import subprocess
if __name__ == "__main__":
    main()


