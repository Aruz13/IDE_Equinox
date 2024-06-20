# -*- coding: utf-8 -*-
import sys

if len(sys.argv) != 2:
    print("Uso: python programa.py <ruta_del_archivo_lexico>")
    sys.exit(1)

lexico_file = sys.argv[1]

class Token:
    def __init__(self, token_type, value):
        self.token_type = token_type
        self.value = value

class Node:
    def __init__(self, value, children=None):
        self.value = value
        self.children = children or []

    def add_child(self, node):
        self.children.append(node)

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.token_index = -1
        self.errors = []
        self.advance()

    def advance(self):
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
        else:
            self.current_token = None

    def match(self, token_type):
        if self.current_token and self.current_token.token_type == token_type:
            self.advance()
        else:
            expected_token = token_type if token_type else "end of input"
            found_token = self.current_token.token_type if self.current_token else "end of input"
            self.errors.append(f"Expected {expected_token}, found {found_token} at token index {self.token_index}")
            self.panic_mode(token_type)
            return

    def panic_mode(self, sync_token_type):
        while self.current_token and self.current_token.token_type != sync_token_type:
            self.advance()
        if self.current_token:
            self.advance()

    def program(self):
        root = Node("Programa")
        self.match("main")
        self.match("{")
        root.add_child(self.stmts())
        self.match("}")
        return root

    def stmts(self):
        root = Node("Declaraciones")
        while self.current_token and self.current_token.token_type not in ["}", "until", "else", "end"]:
            if self.current_token.token_type == "do":
                root.add_child(self.do_while_stmt())
            else:
                root.add_child(self.stmt())
        return root

    def do_while_stmt(self):
        root = Node("SentenciaDoWhile")
        self.match("do")
        root.add_child(self.stmt())
        while self.current_token and self.current_token.token_type != "until":
            root.add_child(self.stmt())
        self.match("until")
        self.match("(")
        root.add_child(self.expr())
        self.match(")")
        self.match(";")
        return root

    def stmt(self):
        if self.current_token and self.current_token.token_type == "int":
            root = Node("Entero")
            self.match("int")
            root.add_child(self.idList())
            self.match(";")
        elif self.current_token and self.current_token.token_type == "float":
            root = Node("Flotante")
            self.match("float")
            root.add_child(self.idList())
            self.match(";")
        elif self.current_token and self.current_token.token_type == "id":
            root = Node("Asignacion")
            id_node = Node(self.current_token.value)
            root.add_child(id_node)
            self.match("id")
            if self.current_token and self.current_token.token_type in ["++", "--"]:
                if self.current_token.token_type == "++":
                    op_node = Node("+")
                    op_node.add_child(id_node)
                    uno_node = Node("1")
                    op_node.add_child(uno_node)
                    root.add_child(op_node)
                else:
                    op_node = Node("-")
                    op_node.add_child(id_node)
                    uno_node = Node("1")
                    op_node.add_child(uno_node)
                    root.add_child(op_node)
                self.match(self.current_token.token_type)
            elif self.current_token and self.current_token.token_type in ["<", ">", "<=", ">=", "==", "!=", "&&", "||"]:
                op_node = Node(self.current_token.value)
                self.match(self.current_token.token_type)
                if self.current_token and self.current_token.token_type in ["id", "num"]:
                    operand_node = Node(self.current_token.value)
                    root.add_child(operand_node)
                    self.match(self.current_token.token_type)
            else:
                self.match("=")
                expr_node = self.expr()
                root.add_child(expr_node)
            self.match(";")
        elif self.current_token and self.current_token.token_type == "if":
            root = Node("Sentencia If")
            self.match("if")
            if self.current_token and self.current_token.token_type == "(":
                self.match("(")
                expr_node = self.expr()
                root.add_child(expr_node)
                self.match(")")
            stmt_node = self.stmt()
            if self.current_token and self.current_token.token_type == "{":
                self.match("{")
                root.add_child(stmt_node)
                self.match("}")
            else:
                root.add_child(stmt_node)
            if self.current_token and self.current_token.token_type == "else":
                self.match("else")
                else_stmt_node = self.stmt()
                root.add_child(else_stmt_node)
            self.match("end")
        elif self.current_token and self.current_token.token_type == "while":
            root = Node("Sentencia While")
            self.match("while")
            self.match("(")
            expr_node = self.expr()
            root.add_child(expr_node)
            self.match(")")
            stmt_node = self.stmt()
            root.add_child(stmt_node)
        elif self.current_token and self.current_token.token_type == "{":
            root = Node("Bloque")
            self.match("{")
            root.add_child(self.stmts())
            self.match("}")
        elif self.current_token and self.current_token.token_type == "cin":
            root = Node("Entrada")
            self.match("cin")
            root.add_child(self.idList())
            self.match(";")
        elif self.current_token and self.current_token.token_type == "cout":
            root = Node("Salida")
            self.match("cout")
            root.add_child(self.expr())
            self.match(";")
        else:
            root = Node("Error")
            error_token = self.current_token.value if self.current_token else None
            if error_token:
                self.errors.append(f"Sentencia inválida: {error_token}")
            self.advance()
        return root

    def idList(self):
        root = Node("Identificadores")
        if self.current_token and self.current_token.token_type == "id":
            id_node = Node(self.current_token.value)
            root.add_child(id_node)
            self.match("id")
        else:
            self.errors.append("Se esperaba un identificador al inicio de la lista de identificadores.")
        while self.current_token and self.current_token.token_type == ",":
            self.match(",")
            if self.current_token and self.current_token.token_type == "id":
                id_node = Node(self.current_token.value)
                root.add_child(id_node)
                self.match("id")
            else:
                self.errors.append("Se esperaba un identificador después de la coma.")
                break
        return root

    def expr(self):
        root = self.relational_expr()
        while self.current_token and self.current_token.token_type in ["+", "-"]:
            op_node = Node(self.current_token.value)
            self.match(self.current_token.token_type)
            op_node.add_child(root)
            op_node.add_child(self.relational_expr())
            root = op_node
        return root

    def relational_expr(self):
        root = self.term()
        while self.current_token and self.current_token.token_type in ["<", ">", "<=", ">=", "==", "!=", "&&", "||"]:
            op_node = Node(self.current_token.value)
            self.match(self.current_token.token_type)
            op_node.add_child(root)
            operand_node = self.term()
            op_node.add_child(operand_node)
            root = op_node
        return root

    def term(self):
        root = self.factor()
        while self.current_token and self.current_token.token_type in ["*", "/", "%"]:
            op_node = Node(self.current_token.value)
            self.match(self.current_token.token_type)
            op_node.add_child(root)
            op_node.add_child(self.factor())
            root = op_node
        return root

    def factor(self):
        root = Node("Factor")
        if self.current_token and self.current_token.token_type == "(":
            self.match("(")
            root = self.expr()
            self.match(")")
        elif self.current_token and self.current_token.token_type in ["id", "num"]:
            value = self.current_token.value if self.current_token else None
            if value is not None:
                value_node = Node(value)
                root = value_node
            self.match(self.current_token.token_type)
        else:
            root = Node("Error")
            error_token = self.current_token.value if self.current_token else None
            self.errors.append(f"Factor inválido: {error_token}")
            self.advance()
        return root

    def parse(self):
        ast = self.program()
        if self.errors:
            print("Errores de sintaxis encontrados. Compilación fallida.")
        else:
            print("Sintaxis correcta. Compilación exitosa.")
        return ast

with open(lexico_file, 'r') as file:
    lines = file.readlines()

token_list = []
for line in lines:
    line = line.strip()
    if line:
        token_parts = line.split('~~~')
        if token_parts[1].strip() == "identificador":
            token_type = "id"
            value = token_parts[0].strip()
        elif token_parts[1].strip() == "flotante" or token_parts[1].strip() == "entero":
            token_type = "num"
            value = token_parts[0].strip()
        else:
            token_type = token_parts[0].strip()
            value = token_parts[0].strip()
        token = Token(token_type, value)
        token_list.append(token)

for tok in token_list:
    try:
        _ = tok.token_type
    except AttributeError:
        print(f"El registro {tok} puede generar el error 'NoneType' object has no attribute 'value'")

parser = Parser(token_list)
ast = parser.parse()

if parser.errors:
    print("Errores de sintaxis:")
    for error in parser.errors:
        print(error)

def print_ast(node, level=0):
    indent = ("~") * level
    line = f"{indent} ==> {node.value}"
    print(line)
    for child in node.children[:-1]:
        print_ast(child, level + 1)
    if node.children:
        print_ast(node.children[-1], level + 1)

print("Arbol de análisis sintáctico:")
print_ast(ast)
