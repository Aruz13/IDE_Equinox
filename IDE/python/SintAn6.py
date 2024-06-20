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
            self.panic_mode()
            return

    def panic_mode(self):
        sync_tokens = {"main", "{", "}", "integer", "double", "if", "while", "do", "cin", "cout", "end", "id", ";", "(", ")"}
        while self.current_token and self.current_token.token_type not in sync_tokens:
            self.advance()
        if self.current_token:
            self.advance()

    def program(self):
        root = Node("Programa")
        self.match("main")
        self.match("{")
        root.add_child(self.listaDeclaracion())
        self.match("}")
        return root

    def listaDeclaracion(self):
        root = Node("ListaDeclaracion")
        while self.current_token and self.current_token.token_type not in ["}"]:
            root.add_child(self.declaracion())
        return root

    def declaracion(self):
        if self.current_token and self.current_token.token_type in ["integer", "double"]:
            return self.declaracionVariable()
        else:
            return self.listaSentencias()

    def declaracionVariable(self):
        root = Node("DeclaracionVariable")
        root.add_child(Node(self.current_token.value))
        self.match(self.current_token.token_type)
        root.add_child(self.identificador())
        self.match(";")
        return root

    def identificador(self):
        root = Node("Identificador")
        while self.current_token and self.current_token.token_type == "id":
            id_node = Node(self.current_token.value)
            root.add_child(id_node)
            self.match("id")
            if self.current_token and self.current_token.token_type == ",":
                self.match(",")
        return root

    def listaSentencias(self):
        root = Node("ListaSentencias")
        while self.current_token and self.current_token.token_type not in ["}", "until", "else", "end"]:
            root.add_child(self.sentencia())
        return root

    def sentencia(self):
        if self.current_token and self.current_token.token_type == "if":
            return self.seleccion()
        elif self.current_token and self.current_token.token_type == "while":
            return self.iteracion()
        elif self.current_token and self.current_token.token_type == "do":
            return self.repeticion()
        elif self.current_token and self.current_token.token_type == "cin":
            return self.sentIn()
        elif self.current_token and self.current_token.token_type == "cout":
            return self.sentOut()
        elif self.current_token and self.current_token.token_type == "id":
            return self.asignacion()
        else:
            root = Node("Error")
            error_token = self.current_token.value if self.current_token else None
            if error_token:
                self.errors.append(f"Sentencia inválida: {error_token}")
            self.advance()
            return root

    def asignacion(self):
        root = Node("Asignacion")
        root.add_child(Node(self.current_token.value))
        self.match("id")
        self.match("=")
        root.add_child(self.sentExpresion())
        return root

    def sentExpresion(self):
        root = self.expresion()
        self.match(";")
        return root

    def seleccion(self):
        root = Node("Seleccion")
        self.match("if")
        root.add_child(self.expresion())
        root.add_child(self.sentencia())
        if self.current_token and self.current_token.token_type == "else":
            self.match("else")
            root.add_child(self.sentencia())
        self.match("end")
        return root

    def iteracion(self):
        root = Node("Iteracion")
        self.match("while")
        root.add_child(self.expresion())
        root.add_child(self.sentencia())
        self.match("end")
        return root

    def repeticion(self):
        root = Node("Repeticion")
        self.match("do")
        root.add_child(self.sentencia())
        self.match("while")
        root.add_child(self.expresion())
        return root

    def sentIn(self):
        root = Node("SentIn")
        self.match("cin")
        root.add_child(Node(self.current_token.value))
        self.match("id")
        self.match(";")
        return root

    def sentOut(self):
        root = Node("SentOut")
        self.match("cout")
        root.add_child(self.expresion())
        self.match(";")
        return root

    def expresion(self):
        root = self.expresionSimple()
        while self.current_token and self.current_token.token_type in ["<", "<=", ">", ">=", "==", "!="]:
            op_node = Node(self.current_token.value)
            self.match(self.current_token.token_type)
            op_node.add_child(root)
            op_node.add_child(self.expresionSimple())
            root = op_node
        return root

    def expresionSimple(self):
        root = self.termino()
        while self.current_token and self.current_token.token_type in ["+", "-"]:
            op_node = Node(self.current_token.value)
            self.match(self.current_token.token_type)
            op_node.add_child(root)
            op_node.add_child(self.termino())
            root = op_node
        return root

    def termino(self):
        root = self.factor()
        while self.current_token and self.current_token.token_type in ["*", "/", "%"]:
            op_node = Node(self.current_token.value)
            self.match(self.current_token.token_type)
            op_node.add_child(root)
            op_node.add_child(self.factor())
            root = op_node
        return root

    def factor(self):
        if self.current_token and self.current_token.token_type == "(":
            self.match("(")
            root = self.expresion()
            self.match(")")
        elif self.current_token and self.current_token.token_type in ["id", "num"]:
            root = Node(self.current_token.value)
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
