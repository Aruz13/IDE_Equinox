# -*- coding: utf-8 -*-
from pathlib import Path
import json
# Para Windows
documents_folder = Path.home() / 'Documents'

# Para Unix/Linux/Mac
# documents_folder = Path.home() / 'Documents'

#print("Carpeta de Documentos:", documents_folder)
# Crear la ruta completa del archivo
file_path = documents_folder / 'python' / 'arbol_sintactico.json'

class Node:
    def __init__(self, value, children=None, line_no=None, type=None, identificator=False, val=None):
        self.value = value
        self.children = children if children is not None else []
        self.line_no = line_no
        self.type = type
        self.identificator = identificator
        self.val = val  # Agregar el manejo del parámetro val

def leer_entradas(archivo):
    entradas = {}
    with open(archivo, "r") as f:
        for linea in f:
            partes = linea.strip().split()
            if len(partes) == 2:
                var_name, value = partes
                try:
                    entradas[var_name] = float(value)
                except ValueError:
                    print(f"Error: valor no numérico para la variable '{var_name}'.")
                    return
    return entradas


def deserialize_node(node_dict):
    node = Node(
        value=node_dict['value'],
        line_no=node_dict['line_no'],
        type=node_dict['type'],
        identificator=node_dict['identificator'],
        val=node_dict['val']
    )
    node.children = [deserialize_node(child) for child in node_dict['children']]
    return node

with open(str(file_path), 'r') as file:
    tree_data = json.load(file)
    root_node = deserialize_node(tree_data)

class CodeGenerator:
    def __init__(self):
        self.code = []
        self.temp_count = 0
        self.output_file = "salida.txt" 
        self.label_count = 0

    def new_label(self):
        self.label_count += 1
        return f"LABEL_{self.label_count}"

    def get_temp(self):
        """ Obtiene un nuevo registro temporal """
        self.temp_count += 1
        return f"T{self.temp_count}"

    def generate_code(self, node, parent=None):
        """ Genera código a partir del nodo del árbol sintáctico """
        if node.value in ["Programa", "Sentencias", "Bloque"]:
            for child in node.children:
                self.generate_code(child)

        elif node.value == "Asignación":
            dest = node.children[0].value
            src_code = self.generate_expression_code(node.children[1])
            self.code.append(f"ST {src_code}, {dest}")


        if node.value == "SentenciaIf":
            if parent and parent.value == "SentenciaIf":
                is_nested = True
            else:
                is_nested = False
            if_body_label = self.new_label()
            else_body_label = self.new_label() if len(node.children) > 2 else None
            end_if_label = self.new_label()

            # Genera código para la condición
            condition_code = self.generate_expression_code(node.children[0],if_body_label)
            #self.code.append(f"JLE {condition_code}, {if_body_label}")
            if not is_nested:
                if else_body_label:
                    self.code.append(f"JMP {else_body_label}")
                else:
                    self.code.append(f"JMP {end_if_label}")

            # Cuerpo del if
            self.code.append(f"{if_body_label}:")
            self.generate_code(node.children[1], parent=node)
            if else_body_label:
                self.code.append(f"JMP {end_if_label}")

            # Cuerpo del else si existe
            if else_body_label:
                self.code.append(f"{else_body_label}:")
                self.generate_code(node.children[2], parent=node)

            # Etiqueta de fin del if
            self.code.append(f"{end_if_label}:")

        elif node.value == "SentenciaWhile":
            start_label = self.new_label()
            end_label = self.new_label()
            self.code.append(f"{start_label}:")
            condition_code = self.generate_expression_code(node.children[0], end_label, is_while=True)
            #self.code.append(f"JNE {condition_code}, {end_label}")
            self.generate_code(node.children[1])
            self.code.append(f"JMP {start_label}")
            self.code.append(f"{end_label}:")

        elif node.value == "SentenciaOutput":
            self.code.append(f"OUT {node.children[0].value}")
            with open(self.output_file, "a") as output_file:
                output_file.write(f"{node.children[0].val}\n")
        # Implementar casos para otros tipos de nodos (DoWhileStatement, OutputStatement, etc.)
        elif node.value == "SentenciaDo":
            start_label = self.new_label()
            end_label = self.new_label()
            self.code.append(f"{start_label}:")
            for child in node.children[:-1]:  # Todos los hijos excepto la condición
                self.generate_code(child)
            condition_code = self.generate_expression_code(node.children[-1],start_label)
            #self.code.append(f"JNE {condition_code}, {start_label}")
            self.code.append(f"{end_label}:")  # Fin del bucle
        elif node.value == "SentenciaInput":
            var_name = node.children[0].children[0].value  # Asume que el primer hijo es el nombre de la variable
            self.code.append(f"IN {var_name} #Valor Input")

    def generate_expression_code(self, node, label=None, is_while=False):
        """ Genera código para expresiones """
        if node.value in ["+", "-", "*", "/"]:
            left_code = self.generate_expression_code(node.children[0])
            right_code = self.generate_expression_code(node.children[1])
            result = self.get_temp()
            if node.value == "+":
                self.code.append(f"ADD {left_code}, {right_code}, {result}")
            elif node.value == "-":
                self.code.append(f"SUB {left_code}, {right_code}, {result}")
            elif node.value == "*":
                self.code.append(f"MUL {left_code}, {right_code}, {result}")
            elif node.value == "/":
                self.code.append(f"DIV {left_code}, {right_code}, {result}")
            return result

        elif self.is_int(node.value):
            temp = self.get_temp()
            self.code.append(f"LDC {temp}, {node.value}")
            return temp

        elif self.is_float(node.value):
            temp = self.get_temp()
            self.code.append(f"LDC {temp}, {node.value}")
            return temp

        elif node.identificator:
            return node.value  # Retorna el nombre de la variable
# Dentro de generate_expression_code

        elif node.value in ["<", ">", "<=", ">=", "==", "!="]:
            left_code = self.generate_expression_code(node.children[0])
            right_code = self.generate_expression_code(node.children[1])
            result = self.get_temp()
            self.code.append(f"SUB {left_code}, {right_code}, {result}")

            inverse_jumps = {
                "<": "JGE",
                ">": "JLE",
                "<=": "JGT",
                ">=": "JLT",
                "==": "JNE",
                "!=": "JEQ"
            }
            jump_instruction = inverse_jumps[node.value] if is_while else {
                "<": "JLT",
                ">": "JGT",
                "<=": "JLE",
                ">=": "JGE",
                "==": "JEQ",
                "!=": "JNE"
            }[node.value]

            self.code.append(f"{jump_instruction} {result}, {label}")

            return result  # Retornar el registro temporal que contiene el resultado

        # Implementar casos para otros tipos de nodos (relaciones, booleanos, etc.)

    def is_int(self, value):
        """ Verifica si un valor es un entero """
        try:
            int(value)
            return True
        except ValueError:
            return False

    def is_float(self, value):
        """ Verifica si un valor es un flotante """
        try:
            float(value)
            return True
        except ValueError:
            return False


code_generator = CodeGenerator()
code_generator.generate_code(root_node)
generated_code = code_generator.code


file_path2 = documents_folder / 'python' / 'codigo_intermedio.txt'

# Opcional: guardar en un archivo
with open(file_path2, "w") as file:
    for line in generated_code:
        print(line)
        file.write(line + "\n")

def execute_intermediate_code(filename):
    output_file_name = "output.txt"
    with open(output_file_name, "w") as filed:
        filed.write("")
    with open(filename, "r") as filed:
        lines = filed.readlines()

    environment = {"variables": {}, "labels": {}}
    for index, line in enumerate(lines):
        if line.strip().endswith(":"):
            label = line.strip()[:-1]
            environment["labels"][label] = index

    current_line = 0
    while current_line < len(lines):
        line = lines[current_line].strip()
        tokens = [token.strip(",") for token in line.split()]
        print(f"Executing line {current_line}: {line}")
        if not tokens or line.endswith(":"):
            current_line += 1
            continue

        instruction = tokens[0]
        args = tokens[1:]

        if instruction == "LDC":
            environment["variables"][args[0]] = float(args[1]) if '.' in args[1] else int(args[1])
        elif instruction == "ST":
            environment["variables"][args[1]] = environment["variables"][args[0]]
        elif instruction in ["ADD", "SUB", "MUL", "DIV"]:
            op1 = environment["variables"][args[0]]
            op2 = environment["variables"][args[1]]
            if instruction == "ADD":
                result = op1 + op2
            elif instruction == "SUB":
                result = op1 - op2
            elif instruction == "MUL":
                result = op1 * op2
            elif instruction == "DIV":
                result = op1 / op2
            environment["variables"][args[2]] = result
        elif instruction in ["JLT", "JGT", "JLE", "JGE", "JEQ", "JNE"]:
            comp_result = environment["variables"][args[0]]
            label = args[1]
            if (instruction == "JLT" and comp_result < 0) or \
               (instruction == "JGT" and comp_result > 0) or \
               (instruction == "JLE" and comp_result <= 0) or \
               (instruction == "JGE" and comp_result >= 0) or \
               (instruction == "JEQ" and comp_result == 0) or \
               (instruction == "JNE" and comp_result != 0):
                current_line = environment["labels"][label]
                continue
        elif instruction == "JMP":
            current_line = environment["labels"][args[0]]
            continue
        elif instruction == "IN":
            var_name = args[0]
        elif instruction == "OUT":
            var_value = environment["variables"].get(args[0], 0)
            with open(output_file_name, "a") as output_file:
                output_file.write(str(var_value) + "\n")
            output_file.close()

        current_line += 1

#execute_intermediate_code("codigo_intermedio.txt")