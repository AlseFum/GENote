Start
	= RuleList

RuleList "rule_list"
	= head:Rule tail:(__ Rule)* __{
			let result_ = [head];
			for (let t of tail) result_.push(t[1]);
      let result = Object.fromEntries(result_.map(e=>[e.name,e.options]));
			return result;
		}

Rule
	= name:Identifier __ '=' __ body:OptionList {
			return { name, options: body };
		}

OptionList
	= first:Option rest:(__ '|' _ Option)* {
			let result = [first];
			for (let r of rest) result.push(r[3]);
			return result;
		}

Option
  = prob:ProbElement* _
  elems:(Element _)+ { 
    let result = {elems:elems.map(e=>e[0])};
    if(prob.length > 0) {
        result.prob = prob[0].prob;
      }
    return result;
  }

Element
  = RefElement
  / TerminalElement

RefElement
  = '$' id:(QuotedString/Identifier) { return { type: 'ref', ref: id }; }

TerminalElement
  = t:(SimpleTerminal / QuotedString) { return { type: 't', value:t }; }
ProbElement
  = '^' prob:ProbExpr _ { return { type: 'prob', prob }; }
ProbExpr
	= '[' expr:Expression ']' { return expr; }
	/ num:Number { return num; }

Expression
	= chars:[^|\n\]]+ { return chars.join('').trim(); }


Identifier
	= SimpleTerminal / QuotedString
SimpleTerminal
  = id:[a-zA-Z_][a-zA-Z0-9_]* { return text(); }

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

Number
	= digits:[0-9]+ { return parseInt(text(), 10); }
_ = [ \t]*
__ = [ \t\r\n]*