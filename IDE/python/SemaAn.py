# -*- coding: utf-8 -*-
import sys


if len(sys.argv) != 2:
    print("Uso: python programa.py <ruta_del_archivo_lexico>")

lexico_file = sys.argv[1]
auxCont = 0

class Token:
    def __init__(self, token_type, value, line):
        self.token_type = token_type
        self.value = value
        self.line = line


class Node:
    def __init__(self, value, line=None, children=None):
        self.value = value
        self.line_no = line  # Guardamos el número de línea
        self.type = None  # Nuevo atributo para el tipo
        self.val = None  # Nuevo atributo para el valor
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
        # print(self.token_index,"  -  ")
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
        else:
            self.current_token = None

    
    def advance2(self, token_type):
        self.token_index += 1
        # print(self.token_index,"  -  ", self.current_token.token_type)
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
        else:
            self.current_token = None

    def match(self, token_type):
        if self.current_token and self.current_token.token_type == token_type:
            self.advance2(self)
        else:
            expected_token = token_type if token_type else "end of input"
            found_token = self.current_token.token_type if self.current_token else "end of input"
            line_token = self.current_token.line if self.current_token else "'last'"
            self.errors.append(f"Expected '{expected_token}', found '{found_token}', linea {line_token}")
            self.panic_mode()
            return

    def panic_mode(self):
        sync_tokens = {"{", "}", "int", "float", "if", "else", "while", "do", "cin", "cout", "end", ";"}
        while self.current_token and self.current_token.token_type not in sync_tokens:
            #print("Saltado: ",self.current_token.token_type)
            self.advance2(self)
        if self.current_token:
            #print("Encontrado: ",self.current_token.token_type)
            if self.current_token and self.current_token.token_type == ";":
                self.advance2(self)
            
    def panic_mode3(self):
        sync_tokens = {"{", "}", "int", "float", "if", "while", "do", "cin", "cout", ";"}
        while self.current_token and self.current_token.token_type not in sync_tokens:
            #print("Saltado: ",self.current_token.token_type)
            self.advance2(self)
        if self.current_token:
            #print("Encontrado: ",self.current_token.token_type)
            if self.current_token and self.current_token.token_type == ";":
                self.advance2(self)

    def panic_mode2(self, tokenEs):
        
        while self.current_token and self.current_token.token_type != tokenEs:
            #print("Saltado panico 2: ",self.current_token.token_type)
            self.advance2(self)
        if self.current_token and self.current_token.token_type == ";":
                self.advance2(self)
            

    def program22(self):
        root = Node("Programa", self.current_token.line)
        self.match("main")
        self.match("{")
        root.add_child(self.stmts())
        self.match("}")
        return root

    def program(self):
        root = Node("Programa", self.current_token.line)
        
        if self.current_token and self.current_token.token_type == "main":
            self.match("main")
            if self.current_token and self.current_token.token_type == "{":
                self.match("{")
                root.add_child(self.stmts())
                if self.current_token and self.current_token.token_type == "}":
                    self.match("}")
                else:
                    aux = Node("Error")
                    root.add_child(aux)
                    self.match("}")
            else:
                root = Node("Error")
                error_token = self.current_token.value if self.current_token else "None"
                linea = self.current_token.line if self.current_token else "last"
                self.errors.append("Expected '{', found '"+error_token+"', linea "+linea)
                root.add_child(self.stmts())
        else:
            root = Node("Error")
            error_token = self.current_token.value if self.current_token else None
            self.errors.append("Expected 'main', found '"+error_token+"', linea "+self.current_token.line)
            self.panic_mode()
            if self.current_token and self.current_token.token_type == "{":
                self.match("{")
                root.add_child(self.stmts())
                self.match("}")
            else:
                root = Node("Error")
                error_token = self.current_token.value if self.current_token else None
                self.errors.append("Expected '{', found '"+error_token+"', linea "+self.current_token.line)
                root.add_child(self.stmts())
        return root
    

    def stmts(self):
        root = Node("Declaraciones", self.current_token.line)
        if self.current_token and self.current_token.token_type in ["int", "float", "id", "if", "{", "while", "cin", "cout"]:
            root.add_child(self.stmt())
        while self.current_token and self.current_token.token_type != "}":
            if self.current_token.token_type == "do":
                root.add_child(self.do_while_stmt())
            else:
                root.add_child(self.stmt())
        return root



    def stmts2(self):
        root = Node("Sentencias", self.current_token.line)
        if self.current_token and self.current_token.token_type in ["int", "float", "id", "if", "{", "while", "cin", "cout"]:
            root.add_child(self.stmt())
        while self.current_token and self.current_token.token_type != "}":
            if self.current_token.token_type == "do":
                root.add_child(self.do_while_stmt())
            else:
                root.add_child(self.stmt())
        return root


  
    def do_while_stmt222(self):
        root = Node("SentenciaDoWhile", self.current_token.line)
        self.match("do")
        root.add_child(self.stmt())  # Agregar la primera expresión dentro del do-while
        while self.current_token and self.current_token.token_type != "while":
            root.add_child(self.stmts2())  # Agregar más expresiones dentro del do-while
        self.match("while")
        self.match("(")
        root.add_child(self.expr())
        self.match(")")
        self.match(";")
        return root


    def do_while_stmt(self):
        root = Node("SentenciaDoWhile", self.current_token.line)
        self.match("do")
        if self.current_token and self.current_token.token_type != "{":
            aux = Node("Error")
            error_token = self.current_token.value if self.current_token else None
            self.errors.append("Expected '{', found '",error_token,"', linea ",self.current_token.line)
            root.add_child(aux)
        self.match("{")
        # print("Entramos en el DO")
        # root.add_child(self.stmt())  # Agregar la primera expresión dentro del do-while
        while self.current_token and self.current_token.token_type != "}":
            # print("Encontramos expresiones en el DO")
            root.add_child(self.stmts2())  # Agregar más expresiones dentro del do-while
        # print("Salimos del DO")
        self.match("}")
        if self.current_token and self.current_token.token_type == "until":
            self.match("until")
            if self.current_token and self.current_token.token_type == "(":
                self.match("(")
                aux = self.expr()
                if aux.value == "Error":
                    root.add_child(aux)
                    return root
                root.add_child(aux)
                if self.current_token and self.current_token.token_type == ")":
                    self.match(")")
                else:
                    aux = Node("Error")
                    error_token = self.current_token.value if self.current_token else None
                    self.errors.append("Expected ')', found '"+error_token+"', linea "+self.current_token.line)
                    root.add_child(aux)
            else:
                aux = Node("Error")
                root.add_child(aux)
                self.match("(")
                return root
        else:
            aux = Node("Error")
            root.add_child(aux)
            self.match("until")
            return root
        #print("antes de acabar el dowhile: ", self.current_token.token_type)
        if self.current_token and self.current_token.token_type == ";":
            self.match(";")
        else:
            aux = Node("Error")
            root.add_child(aux)
            self.match(";")
        return root


    def stmt(self):
        if self.current_token and self.current_token.token_type == "int":
            root = Node("Entero", self.current_token.line)
            self.match("int")
            aux = self.idList()
            root.add_child(aux)
            if aux.value != "Error":
                self.match(";")
            else:
                self.panic_mode()
        elif self.current_token and self.current_token.token_type == "do":
            root = self.do_while_stmt()
        elif self.current_token and self.current_token.token_type == "float":
            root = Node("Flotante", self.current_token.line)
            self.match("float")
            aux = self.idList()
            root.add_child(aux)
            if aux.value != "Error":
                self.match(";")
            else:
                self.panic_mode()
        elif self.current_token and self.current_token.token_type == "id":
                errorflag = True
                root = Node("Asignacion", self.current_token.line)
                id_node = Node(self.current_token.value, self.current_token.line)
                root.add_child(id_node)
                self.match("id")# a
                if self.current_token and self.current_token.token_type in ["++", "--"]:
                    #op_node = Node(self.current_token.value) # ++
                    if self.current_token.token_type == "++":
                        op_node = Node("+", self.current_token.line)
                        op_node.add_child(id_node)
                        uno_node = Node("1", self.current_token.line)
                        op_node.add_child(uno_node)
                        root.add_child(op_node)
                    else:
                        op_node = Node("-", self.current_token.line)
                        op_node.add_child(id_node)
                        uno_node = Node("1", self.current_token.line)
                        op_node.add_child(uno_node)
                        root.add_child(op_node)                  
                    self.match(self.current_token.token_type)
                    #root.add_child(op_node)
                elif self.current_token and self.current_token.token_type in ["<", ">", "<=", ">=", "==", "!=", "&&", "||"]:
                    op_node = Node(self.current_token.value, self.current_token.line)
                    self.match(self.current_token.token_type)
                    if self.current_token and self.current_token.token_type in ["id", "num"]:
                        operand_node = Node(self.current_token.value, self.current_token.line)
                        root.add_child(operand_node)
                        self.match(self.current_token.token_type)
                else:
                    if self.current_token and self.current_token.token_type == "=":
                        self.match("=")
                        #global auxCont
                        expr_node = self.expr()
                        #auxCont = 0
                        root.add_child(expr_node)
                        if expr_node.value == "Error":
                            errorflag = False
                    else:
                        self.match("=")
                        aux = Node("Error")
                        root.add_child(aux)
                        errorflag = False
                # print("Cierre con punto y coma.............")
                # print("Pre ';' = ", self.current_token.token_type," - ", self.current_token.value)
                # print("Bandera", errorflag)
                if errorflag:
                    if self.current_token and self.current_token.token_type != ';':
                        aux = Node("Error")
                        root.add_child(aux)
                    self.match(";")
                    # print("post ';' = ", self.current_token.token_type," - ", self.current_token.value)
                #root.add_child(id_node)
        elif self.current_token and self.current_token.token_type == "if":
            root = Node("Sentencia If", self.current_token.line)
            self.match("if")
            if self.current_token and self.current_token.token_type == "(":
                self.match("(")
                root.add_child(self.expr())
                if self.current_token and self.current_token.token_type == ")":
                    self.match(")")
            else:
                aux = Node("Error")
                root.add_child(aux)
                self.match("(")
            if self.current_token and self.current_token.token_type != "{":
                aux = Node("Error")
                error_token = self.current_token.value if self.current_token else None
                # self.errors.append("Expected '{', found '"+error_token+"', linea "+self.current_token.line)
                root.add_child(aux)
            self.match("{")
            root.add_child(self.stmts2())

            if self.current_token and self.current_token.token_type != "}":
                aux = Node("Error")
                error_token = self.current_token.value if self.current_token else None
                self.errors.append("Expected 'main', found '"+error_token+"', linea "+self.current_token.line)
                root.add_child(aux)
            self.match("}")

            if self.current_token and self.current_token.token_type == "else":
                auxElse = Node("Sentencia Else", self.current_token.line)
                self.match("else")
                if self.current_token and self.current_token.token_type != "{":
                    aux = Node("Error")
                    error_token = self.current_token.value if self.current_token else None
                    self.errors.append("Expected '{', found '"+error_token+"', linea "+self.current_token.line)
                    auxElse.add_child(aux)
                self.match("{")
                else_stmt_node = self.stmts2()
                auxElse.add_child(else_stmt_node)

                if self.current_token and self.current_token.token_type != "}":
                    aux = Node("Error")
                    error_token = self.current_token.value if self.current_token else None
                    self.errors.append("Expected 'main', found '"+error_token+"', linea "+self.current_token.line)
                    auxElse.add_child(aux)
                self.match("}")
                root.add_child(auxElse)

            if self.current_token and self.current_token.token_type != "end":
                aux = Node("Error")
                error_token = self.current_token.value if self.current_token else None
                self.errors.append("Expected 'end', found '"+error_token+"', linea "+self.current_token.line)
                root.add_child(aux)
            else:
                self.match("end")
           
        elif self.current_token and self.current_token.token_type == "while":
            root = Node("Sentencia While", self.current_token.line)
            self.match("while")
            if self.current_token and self.current_token.token_type == "(":
                self.match("(")
                root.add_child(self.expr())
                if self.current_token and self.current_token.token_type == ")":
                    self.match(")")
            else:
                aux = Node("Error")
                root.add_child(aux)
                self.match("(")
            if self.current_token and self.current_token.token_type != "{":
                aux = Node("Error")
                error_token = self.current_token.value if self.current_token else None
                #auxText = "Expected '{', found '"+error_token+"', linea "+self.current_token.line
                self.errors.append("Expected '{', found '"+error_token+"', linea "+self.current_token.line)
                root.add_child(aux)
            self.match("{")
            root.add_child(self.stmts2())
            if self.current_token and self.current_token.token_type != "}":
                aux = Node("Error")
                error_token = self.current_token.value if self.current_token else None
                self.errors.append("Expected 'main', found '"+error_token+"', linea "+self.current_token.line)
                root.add_child(aux)
            self.match("}")
        elif self.current_token and self.current_token.token_type == "{":
            root = Node("Bloque", self.current_token.line)
            self.match("{")
            root.add_child(self.stmts2())
            self.match("}")
        elif self.current_token and self.current_token.token_type == "cin":
            root = Node("Entrada", self.current_token.line)
            self.match("cin")
            aux = self.idList()
            root.add_child(aux)
            if aux.value == "Error":
                self.panic_mode3()
                # print(self.current_token.token_type + " - " + self.current_token.value)
                return root
            self.match(";")
        elif self.current_token and self.current_token.token_type == "cout":
            root = Node("Salida", self.current_token.line)
            self.match("cout")
            aux = self.expr()
            if aux.value == "Error":
                root.add_child(aux)
                return root
            root.add_child(aux)
            if self.current_token and self.current_token.token_type == ";":
                self.match(";")
            else:
                aux = Node("Error")
                root.add_child(aux)
        else:
            root = Node("Error")
            error_token = self.current_token.value if self.current_token else None
            if error_token:
                self.errors.append(f"Sentencia inválida: {error_token}, linea {self.current_token.line}")
            self.panic_mode3()
        return root

# corregir para la coma 
    def idList222(self):
        root = Node("Identificadores", self.current_token.line)
        while self.current_token and self.current_token.token_type == "id":
            id_node = Node(self.current_token.value, self.current_token.line)
            root.add_child(id_node)
            self.match("id")
            if self.current_token and self.current_token.token_type == ",":
                self.match(",")
        return root



    def idList(self):
        root = Node("Identificadores", self.current_token.line)
        if self.current_token and self.current_token.token_type == "id":
            id_node = Node(self.current_token.value, self.current_token.line)
            root.add_child(id_node)
            self.match("id")
            if self.current_token and self.current_token.token_type not in [",",";"]:
                # print("Marca error", self.current_token.token_type)
                root = Node("Error")
                error_token = self.current_token.value if self.current_token else None
                self.errors.append(f"Expected ',' or ';', found '{error_token}', linea {self.current_token.line}")
                #print("Antes de salir del ciclo idList", self.current_token.token_type)
                return root
        else:
            #print("Error de int o float inicio.")
            root = Node("Error")
            error_token = self.current_token.value if self.current_token else None
            self.errors.append(f"Expected 'id', found '{error_token}', linea {self.current_token.line}")
            #self.errors.append(f"Token invalido: {error_token}")
            #self.errors.append("Se esperaba un identificador al inicio de la lista de identificadores.")
            #print("Antes de salir del ciclo idList", self.current_token.token_type)
            return root
        
        while self.current_token and self.current_token.token_type == ",":
            self.match(",")
            if self.current_token and self.current_token.token_type == "id":
                id_node = Node(self.current_token.value, self.current_token.line)
                root.add_child(id_node)
                self.match("id")
                #print(self.current_token.token_type)
                if self.current_token and self.current_token.token_type not in [",",";"]:
                    #print("Marca error", self.current_token.token_type)
                    root = Node("Error")
                    error_token = self.current_token.value if self.current_token else None
                    self.errors.append(f"Expected ',' or ';', found '{error_token}', linea {self.current_token.line}")
                    #self.advance2(self)
                    #print("Antes de salir del ciclo idList", self.current_token.token_type)
                    return root
            else:
                #print("Error de las comas - ", self.current_token.token_type)
                root = Node("Error")
                error_token = self.current_token.value if self.current_token else None
                self.errors.append(f"Expected 'id', found '{error_token}', linea {self.current_token.line}")
                #self.advance2(self)
                #print("Antes de salir del ciclo idList", self.current_token.token_type)
                return root
        
        # print("Antes de salir del ciclo idList", self.current_token.token_type)
        return root


    def expr(self):
        # print("Entra expr")
        root = self.relational_expr()
        if root.value == "Error":
            return root
        while self.current_token and self.current_token.token_type in ["+", "-"]:
            op_node = Node(self.current_token.value, self.current_token.line)
            self.match(self.current_token.token_type)
            op_node.add_child(root)
            aux = self.relational_expr()
            if aux.value == "Error":
                return aux
            op_node.add_child(aux)
            root = op_node
        # print("Sale expr")
        return root
    

    def relational_expr(self):
        # print("Entra relational_expr")
        root = self.term()
        if root.value == "Error":
            return root
        while self.current_token and self.current_token.token_type in ["<", ">", "<=", ">=", "==", "!=", "&&", "||"]:
            op_node = Node(self.current_token.value, self.current_token.line)
            self.match(self.current_token.token_type)
            op_node.add_child(root)
            aux = self.term() 
            if aux.value == "Error":
                return aux
            op_node.add_child(aux)
            root = op_node
        # print("Sale relational_expr")
        return root


    def term(self):
        # print("Entra term")
        root = self.factor()
        if root.value == "Error":
            return root
        while self.current_token and self.current_token.token_type in ["*", "/", "%"]:
            op_node = Node(self.current_token.value, self.current_token.line)
            self.match(self.current_token.token_type)
            op_node.add_child(root)
            aux = self.factor() 
            if aux.value == "Error":
                return aux
            op_node.add_child(aux)
            root = op_node
        # print("Sale term")
        return root

    def factor(self):
        #global auxCont
        #auxCont = auxCont + 1
        # print("Entra factor")
        root = Node("Factor", self.current_token.line)
        if self.current_token and self.current_token.token_type == "(":
            self.match("(")
            root = self.expr()
            if root.value == "Error":
                return root
            if self.current_token and self.current_token.token_type != ")":
                #print("Marca error", self.current_token.token_type)
                root = Node("Error")
                error_token = self.current_token.value if self.current_token else None
                # self.errors.append(f"Expected ')', found '{error_token}', linea {self.current_token.line}, cont {auxCont}")
                #self.advance2(self)
                #print("Antes de salir del ciclo idList", self.current_token.token_type)
                self.match(")")
                return root
            self.match(")")
        elif self.current_token and self.current_token.token_type in ["id", "num"]:
            value = self.current_token.value if self.current_token else None
            if value is not None:
                value_node = Node(value, self.current_token.line)
                root = value_node
            self.match(self.current_token.token_type)
            if self.current_token and self.current_token.token_type not in ["(", ")", ";", "*", "/", "%", "<", ">", "<=", ">=", "==", "!=", "&&", "||", "+", "-"]:
                root = Node("Error")
                error_token = self.current_token.value if self.current_token else None
                self.errors.append(f"Expected 'operador', ')' or ';', found '{error_token}', linea {self.current_token.line}")
                self.panic_mode()
            # print("Antes de salir del ciclo idList", self.current_token.token_type)
        else:
            root = Node("Error")
            error_token = self.current_token.value if self.current_token else None
            self.errors.append(f"Expected '(','id' or 'num', found '{error_token}', linea {self.current_token.line}")
            self.panic_mode()
            # self.advance2(self)
        # print("Sale factor")
        return root


    def parse(self):
        ast = self.program()

        if self.errors:
            print("Errores de sintaxis encontrados. Compilacion fallida.")
        else:
            print("Sintaxis correcta. Compilacion exitosa.")

        return ast
    

class SemanticAnalyzer:
    def __init__(self):
        self.errors = []
        self.symbol_table = {}

    def analyze(self, ast):
        self.visit_node(ast)

    def visit_node(self, node):
        if node.value == "Entero":
            self.handle_int_declaration(node)
        elif node.value == "Flotante":
            self.handle_float_declaration(node)
        elif node.value == "Asignacion":
            self.handle_assignment(node)

        for child in node.children:
            self.visit_node(child)

    def handle_int_declaration(self, node):
        variable_name = node.children[0].value
        if variable_name in self.symbol_table:
            self.errors.append(f"Duplicado: Variable {variable_name} ya declarada, linea: {node.children[0].line_no}")
        else:
            self.symbol_table[variable_name] = {
                "type": "int",
                "value": None,
                "line_numbers": [node.children[0].line_no],  # Agregamos el número de línea
            }

    def handle_float_declaration(self, node):
        variable_name = node.children[0].value
        if variable_name in self.symbol_table:
            self.errors.append(f"Duplicado: Variable {variable_name} ya declarada, linea: {node.children[0].line_no}")
        else:
            self.symbol_table[variable_name] = {
                "type": "float",
                "value": None,
                "line_no": [node.children[0].line_no],  # Agregamos el número de línea
            }

    def handle_assignment(self, node):
        variable_name = node.children[0].value
        if variable_name not in self.symbol_table:
            self.errors.append(f"No declarado: Variable {variable_name} no se ha declarado, linea: {node.children[0].line_no}")
        else:
            # Realizar más comprobaciones semánticas para asignaciones si es necesario
            pass


# Función para anotar el árbol sintáctico
def annotate_tree(node, level=0, output=None):
    indent = " | " * level
    if output:
        value_str = f"{node.value} (Línea {node.line_no})"
        if hasattr(node, "type"):
            value_str += f" [Tipo: {node.type}]"
        if hasattr(node, "val"):
            value_str += f" [Valor: {node.val}]"
        output.write(f"{indent}{value_str}\n")
    for child in node.children:
        annotate_tree(child, level + 1, output)

# Función para imprimir el árbol anotado y guardarlo en un archivo
def print_ast(node, level=0, is_last_child=False, output=None):
    indent = " | " * level
    if output:
        value_str = f"{node.value} (Línea {node.line_no})"
        if hasattr(node, "type"):
            value_str += f" [Tipo: {node.type}]"
        if hasattr(node, "val"):
            value_str += f" [Valor: {node.val}]"
        output.write(f"{indent}{value_str}\n")
    for i, child in node.children:
        is_last = i == len(node.children) - 1
        print_ast(child, level + 1, is_last, output)

# Función para crear un archivo de texto para la tabla de símbolos
def create_symbol_table_text(symbol_table, filename):
    with open(filename, "w") as file:
        file.write("Nombre Variable\tTipo\tValor\tRegistro (loc)\tNúmeros de línea\n")
        for variable, data in symbol_table.items():
            line_no_numbers = ", ".join(map(str, data['line_numbers']))
            file.write(f"{variable}\t{data['type']}\t{data['value']}\t -- \t{line_no_numbers}\n")


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
            line = token_parts[2].strip()
        elif token_parts[1].strip() == "flotante":
            token_type = "num"
            value = token_parts[0].strip()
            line = token_parts[2].strip()
        elif token_parts[1].strip() == "entero":
            token_type = "num"
            value = token_parts[0].strip()
            line = token_parts[2].strip()
        else:
            token_type = token_parts[0].strip()
            value = token_parts[0].strip()
            line = token_parts[2].strip()
        token = Token(token_type, value, line)
        token_list.append(token)
# # Imprimir la lista de objetos Token
for tok in token_list:
    try:
        _ = tok.token_type  # Intentar acceder al atributo 'value'
    except AttributeError:
        print(f"El registro {tok} puede generar el error 'NoneType' object has no attribute 'value'")


parser = Parser(token_list)
ast = parser.parse()

# Crear instancia del SemanticAnalyzer y analizar el árbol sintáctico
semantic_analyzer = SemanticAnalyzer()
semantic_analyzer.analyze(ast)

# Guardar errores semánticos en un archivo
with open("errores_semanticos.txt", "w", encoding="utf-8") as error_file:
    for error in semantic_analyzer.errors:
        error_file.write(error + "\n")

# Anotar el árbol sintáctico
with open("arbol_sintactico_anotado.txt", "w", encoding="utf-8") as annotated_tree_file:
    annotated_tree_file.write("Árbol Sintáctico Anotado:\n")
    annotate_tree(ast, output=annotated_tree_file)

# Crear un archivo de texto para la tabla de símbolos
create_symbol_table_text(semantic_analyzer.symbol_table, "tabla_simbolos.txt")