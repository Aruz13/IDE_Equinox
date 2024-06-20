# -*- coding: utf-8 -*-
import sys


if len(sys.argv) != 2:
    print("Uso: python programa.py <ruta_del_archivo_lexico>")

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
            self.errors.append(f"Expected {expected_token}, found {found_token}")
            self.advance()
            return

    def program(self):
        root = Node("Programa")
        self.match("main")
        self.match("{")
        root.add_child(self.stmts())
        self.match("}")
        return root
    

    def stmts(self):
        root = Node("Declaraciones")
        if self.current_token and self.current_token.token_type in ["int", "float", "id", "if", "while", "cin", "cout"]:
            root.add_child(self.stmt())
        while self.current_token and self.current_token.token_type != "}":
            if self.current_token.token_type == "do":
                root.add_child(self.do_while_stmt())
            else:
                root.add_child(self.stmt())
        return root



    def stmts2(self):
        root = Node("Sentencias")
        if self.current_token and self.current_token.token_type in ["int", "float", "id", "if", "while", "cin", "cout"]:
            root.add_child(self.stmt())
        while self.current_token and self.current_token.token_type != "}":
            if self.current_token.token_type == "do":
                root.add_child(self.do_while_stmt())
            else:
                root.add_child(self.stmt())
        return root


  
    def do_while_stmt(self):
        root = Node("SentenciaDoWhile")
        self.match("do")
        root.add_child(self.stmt())  # Agregar la primera expresión dentro del do-while
        while self.current_token and self.current_token.token_type != "while":
            root.add_child(self.stmt())  # Agregar más expresiones dentro del do-while
        self.match("while")
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
        elif self.current_token and self.current_token.token_type == "do":
            root = self.do_while_stmt()
        elif self.current_token and self.current_token.token_type == "float":
            root = Node("Flotante")
            self.match("float")
            root.add_child(self.idList())
            self.match(";")
        elif self.current_token and self.current_token.token_type == "id":
                root = Node("Asignacion")
                id_node = Node(self.current_token.value)
                root.add_child(id_node)
                self.match("id")# a
                if self.current_token and self.current_token.token_type in ["++", "--"]:
                    #op_node = Node(self.current_token.value) # ++
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
                    #root.add_child(op_node)
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
                #root.add_child(id_node)
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
            root.add_child(self.stmts2())
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

# corregir para la coma 
    def idList222(self):
        root = Node("Identificadores")
        while self.current_token and self.current_token.token_type == "id":
            id_node = Node(self.current_token.value)
            root.add_child(id_node)
            self.match("id")
            if self.current_token and self.current_token.token_type == ",":
                self.match(",")
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
    
    def relational_expr2(self):
        root = self.term()
        while self.current_token and self.current_token.token_type in ["<", ">", "<=", ">=", "==", "!=", "&&", "||"]:
            op_node = Node(self.current_token.value)
            self.match(self.current_token.token_type)
            op_node.add_child(root)
            if self.current_token and self.current_token.token_type in ["id", "num"]:
                operand_node = Node(self.current_token.value)
                op_node.add_child(operand_node)
                self.match(self.current_token.token_type)
            root = op_node
        return root

    def relational_expr(self):
        root = self.term()
        while self.current_token and self.current_token.token_type in ["<", ">", "<=", ">=", "==", "!=", "&&", "||"]:
            op_node = Node(self.current_token.value)
            self.match(self.current_token.token_type)
            op_node.add_child(root)
            operand_node = self.term()  # Cambiado a termino en lugar de la lógica anterior
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
            self.errors.append(f"factor invalido: {error_token}")
            self.advance()
        return root

    def parse(self):
        ast = self.program()

        if self.errors:
            print("Errores de sintaxis encontrados. Compilacion fallida.")
        else:
            print("Sintaxis correcta. Compilacion exitosa.")

        return ast
# print(lexico_file)
with open(lexico_file, 'r') as file:
    lines = file.readlines()

# Crear la lista de objetos Token
token_list = []
for line in lines:
    line = line.strip()
    if line:
        token_parts = line.split('~~~')
        if token_parts[1].strip() == "identificador" :
            token_type = "id"
            value = token_parts[0].strip()
        elif token_parts[1].strip() == "flotante":
            token_type = "num"
            value = token_parts[0].strip()
        elif token_parts[1].strip() == "entero":
            token_type = "num"
            value = token_parts[0].strip()
        else:
            token_type = token_parts[0].strip()
            value = token_parts[0].strip()
        token = Token(token_type, value)
        token_list.append(token)
# # Imprimir la lista de objetos Token
for tok in token_list:
    try:
        _ = tok.token_type  # Intentar acceder al atributo 'value'
    except AttributeError:
        print(f"El registro {tok} puede generar el error 'NoneType' object has no attribute 'value'")


parser = Parser(token_list)
ast = parser.parse()

# Print errors
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

print("Arbol de analisis sintactico:")
print_ast(ast)