__all__ = ['parse', 'ParseError']

import ply.lex as lex
import ply.yacc as yacc
from dataclasses import dataclass
from random import randint

class ParseError(Exception):
    """
    Exception raised for errors encountered during parsing of dice roll expressions.

    Args:
        text (str): A description of the specific error encountered.

    Example:
        raise ParseError("Illegal character %")
    """
    def __init__(self, text):
        super().__init__(text)

### LEXER DEFINITIONS

tokens = (
   'NUMBER',
   'PLUS',
   'TIMES',
   'LPAREN',
   'RPAREN',
   'DIE',
   'COMMA',
   'IDENT',
)

t_PLUS = r'\+'
t_TIMES = r'x'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_DIE = r'd'
t_COMMA = ','

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_IDENT(t):
    r'(?![dDxX])[a-zA-Z]+'
    t.value = t.value.upper()
    if t.value not in ['MAX', 'MIN', 'MEAN']:
        raise ParseError(f"Invalid function name {t.value}")
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = ' \t'

def t_error(t):
    raise ParseError(f"Illegal character {t.value[0]}")

lexer = lex.lex()

### PARSER DEFINITIONS

class Node(object):
    """
    Base class for nodes in the parsed syntax tree. Each subclass should implement the
    eval() method to evaluate the node's value or perform its specific operation.

    Methods:
        eval(): Evaluates the node's value or operation. Must be implemented in subclasses.
    """

    def eval(self) -> int:
        """
        Allows expressions to be evaluated in a convenient way, 
        such as by calling `parse('2x3d4').eval()`.

        Returns:
            int: The result of node evaluation.

        Raises:
            NotImplementedError: If the eval() method is not implemented in a subclass.
        """
        raise NotImplementedError

@dataclass
class Literal(Node):
    value: int

    def eval(self):
        return self.value

@dataclass
class Die(Node):
    sides: int

    def eval(self):
        #10-sided dice go from 0-9, whereas other N-sided dice go from 1-N
        return randint(0, self.sides - 1) if self.sides == 10 else randint(1, self.sides)

@dataclass
class Rolls(Node):
    node: Node
    count: int

    def eval(self):
        return sum(self.node.eval() for _ in range(self.count))

@dataclass
class Mult(Node):
    node: Node
    count: int

    def eval(self):
        return self.node.eval() * self.count

@dataclass
class Add(Node):
    lhs: Node
    rhs: Node

    def eval(self):
        return self.lhs.eval() + self.rhs.eval()
    
@dataclass
class Min(Node):
    params: list[Node]

    def eval(self):
        return min([i.eval() for i in self.params])

@dataclass
class Max(Node):
    params: list[Node]

    def eval(self):
        return max([i.eval() for i in self.params])

@dataclass
class Mean(Node):
    params: list[Node]

# Reduction rules for the parser:

def p_add(p):
    'sum : mult PLUS mult'
    p[0] = Add(p[1], p[3])

def p_no_add(p):
    'sum : mult'
    p[0] = p[1]

def p_mult(p):
    'mult : NUMBER TIMES value'
    p[0] = Mult(p[3], p[1])

def p_no_mult(p):
    'mult : value'
    p[0] = p[1]

def p_die(p):
    '''value : NUMBER DIE NUMBER
             | DIE NUMBER'''
    p[0] = Rolls(Die(p[2]), 1) if p[1] == 'd' else Rolls(Die(p[3]), p[1])

def p_literal(p):
    'value : NUMBER'
    p[0] = Literal(p[1])

def p_function(p):
    'value : IDENT LPAREN list RPAREN'
    if p[1] == 'MIN':
        p[0] = Min(p[3])
    elif p[1] == 'MAX':
        p[0] = Max(p[3])
    else:
        p[0] = Mean(p[3])

def p_parens(p):
    'value : LPAREN sum RPAREN'
    p[0] = p[2]

def p_list_new(p):
    'list : sum COMMA sum'
    p[0] = [p[1], p[3]]

def p_list_append(p):
    'list : list COMMA sum'
    p[0] = p[1] + [p[3]]

def p_error(p):
    raise ParseError(f'Syntax Error')

parser = yacc.yacc()

def parse(text: str) -> Node:
    """
    Parses the dice roll text and returns a syntax tree representation.

    Args:
        text (str): The text to be parsed.

    Returns:
        Node: The root node of the parsed syntax tree.

    Raises:
        ParseError: If the text cannot be parsed.

    Example:
        >>> parse("min(3d6,d20) + 1")
        Add(lhs=Min(params=[Rolls(node=Die(sides=6), count=3), Rolls(node=Die(sides=20), count=1)]), rhs=Literal(value=1))
    """
    return parser.parse(text)
