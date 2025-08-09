// GenLang PEG grammar for peggy.js
Start
	= __ rules:RuleList* __ { return rules; }

RuleList
	= head:Rule tail:(__ Rule)* {
			let result = [head];
			for (let t of tail) result.push(t[1]);
			return result;
		}

Rule
	= name:Identifier __ '=' __ body:OptionList {
			return { name, options: body };
		}

OptionList
	= first:Option rest:(__ '|' __ Option)* {
			let result = [first];
			for (let r of rest) result.push(r[3]);
			return result;
		}

Option
  = elems:Element+ { return elems; }

Element
  = ProbElement
  / RefElement
  / TerminalElement
  / ExprElement

ProbElement
  = '^' prob:ProbExpr __ { return { type: 'prob', prob }; }

RefElement
  = '$' __ id:Identifier { return { type: 'ref', ref: id }; }

TerminalElement
  = str:QuotedString { return { type: 'terminal', value: str }; }
  / id:Identifier { return { type: 'terminal', value: id }; }

ExprElement
  = expr:Expression { return { type: 'expr', expr }; }

ProbExpr
	= '[' expr:Expression ']' { return expr; }
	/ num:Number { return num; }

Expression
	= chars:[^|\n\]]+ { return chars.join('').trim(); }

QuotedString
  = '"' chars:EscapedChar* '"' { return chars.join(''); }

EscapedChar
  = EscapeSequence
  / [^\\"]

EscapeSequence
  = "\\" char:["\\/bfnrt] { 
      switch(char) {
        case 'b': return '\b';
        case 'f': return '\f';
        case 'n': return '\n';
        case 'r': return '\r';
        case 't': return '\t';
        default: return char;
      }
    }
//   / "\\u" digits:[0-9a-fA-F]{4} {  return String.fromCharCode(parseInt(digits.join(''), 16));}
Identifier
	= id:[a-zA-Z_][a-zA-Z0-9_]* { return text(); }

Number
	= digits:[0-9]+ { return parseInt(text(), 10); }

__ = [ \t\r\n]*