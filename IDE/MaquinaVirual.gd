extends PanelContainer

signal user_input_completed(value)
var detener = false 
@export var pasoXpaso = false
var user_input
@onready var codeIntermedio = $"../../../HSplitContainer/TabContainer2/Codigo intermedio"

# Interpreta código intermedio en GDScript
func execute_intermediate_code(input_code: String) -> void:
	var lines = input_code.split("\n")
	var environment = {"variables": {}, "labels": {}}
	var output = []

	# Preprocesamiento: identificar etiquetas
	for index in range(lines.size()):
		var line = lines[index].strip_edges()
		#print("Linea: ",line)
		if line.ends_with(":"):
			#print("Es una etiqueta")
			var label = line.substr(0, line.length() - 1)
			environment["labels"][label] = index

	#print(environment)
	# Ejecución del código
	var prevLine = 0
	var current_line = 0
	#print("Lineas totales: ",lines.size())
	#print("Lineas totales: ",lines.size())
	#print("Lineas totales: ",lines.size())
	while current_line < lines.size():
		if pasoXpaso:
			
			codeIntermedio.set_line_background_color(current_line, Color(0, 0.5, 0.5, 0.7))
			codeIntermedio.set_caret_line(current_line, true)
			codeIntermedio.set_line_background_color(prevLine, Color.TRANSPARENT)
			await get_tree().create_timer(.5).timeout
			prevLine = current_line
		if detener:
			detener = false
			$VBoxContainer/Resultados.text += "\n\n\nSimulacion detenida de manera forzada."
			break
		
		var line = lines[current_line].strip_edges()
		#print(line)
		#print("Linea escaneada: ", current_line)
		var tokens = []
		for token in line.split(" "):
			tokens.append(token.replace(",",""))

		if tokens.size() == 0 or line.ends_with(":"):
			current_line += 1
			continue

		var instruction = tokens[0]
		var args = tokens.slice(1)

		match instruction:
			"DIN":
				environment["variables"][args[0]] = [int(args[1]), "int"]
			"DFL":
				environment["variables"][args[0]] = [float(args[1]), "float"]
			"LDC":
				environment["variables"][args[0]] = [float(args[1]), "float"] if args[1].find(".") != -1 else [int(args[1]), "int"]
			"ST":
				var aux
				if environment["variables"][args[1]][1] == "int":
					aux = int(environment["variables"].get(args[0], 0)[0])
				else:
					aux = environment["variables"].get(args[0], 0)[0]
				environment["variables"][args[1]] = [aux, environment["variables"][args[1]][1]]
				
			"ADD", "SUB", "MUL", "DIV", "MOD", "POT":
				var op1 = environment["variables"].get(args[0], 0)[0]
				var op2 = environment["variables"].get(args[1], 0)[0]
				#print("Inicio - ", op1 ," - ", op2)
				var op1T = environment["variables"].get(args[0], 0)[1]
				var op2T = environment["variables"].get(args[1], 0)[1]
				if op1T == "int":
					op1 = int(op1)
				else:
					op1 = float(op1)
				if op2T == "int":
					op2 = int(op2)
				else:
					op2 = float(op2)
				
				#print("Despues de convertir - ", op1 ," - ", op2)
				var auxT = ""
				var result = 0

				match instruction:
					"ADD":
						result = float(op1) + float(op2)
						#print(result ," - ", op1 ," - ", op2)
						if ((op1T == "int") and (op2T == "int")):
							result = int(result)
							auxT = "int"
						elif (((op1T == "float") and (op2T == "int")) or ((op1T == "int") and (op2T == "float")) or ((op1T == "float") and (op2T == "float"))):
							result = float(result)
							auxT = "float"
					"SUB":
						result = float(op1) - float(op2)
						#print(result ," - ", op1 ," - ", op2)
						if ((op1T == "int") and (op2T == "int")):
							result = int(result)
							auxT = "int"
						elif (((op1T == "float") and (op2T == "int")) or ((op1T == "int") and (op2T == "float")) or ((op1T == "float") and (op2T == "float"))):
							result = float(result)
							auxT = "float"
					"MUL":
						result = float(op1) * float(op2)
						#print(result ," - ", op1 ," - ", op2)
						if ((op1T == "int") and (op2T == "int")):
							result = int(result)
							auxT = "int"
						elif (((op1T == "float") and (op2T == "int")) or ((op1T == "int") and (op2T == "float")) or ((op1T == "float") and (op2T == "float"))):
							result = float(result)
							auxT = "float"
					"DIV":
						if op2 == 0:
							$VBoxContainer/Resultados.text += "\n\n\nERROR: Division entre 0"
							break
						result = float(op1) / float(op2) if op2 != 0 else 0
						print(result ," - ", op1 ," - ", op2)
						if ((op1T == "int") and (op2T == "int")):
							result = int(result)
							auxT = "int"
						elif (((op1T == "float") and (op2T == "int")) or ((op1T == "int") and (op2T == "float")) or ((op1T == "float") and (op2T == "float"))):
							result = float(result)
							auxT = "float"
					"MOD":
						var auxt1 = typeof(op1)
						var auxt2 = typeof(op2)
						#print(auxt1, " - ", auxt2)
						if ((auxt1 == 2) and (2 == auxt2)):  # Ambos operandos son enteros
							result = op1 % op2 if op2 != 0 else 0
						if (((auxt1 == 3) and (3 == auxt2)) or ((auxt1 == 2) and (3 == auxt2)) or ((auxt1 == 3) and (2 == auxt2))):  # Ambos operandos son enteros
						#if (TYPE_FLOAT, TYPE_FLOAT), (TYPE_INT, TYPE_FLOAT), (TYPE_FLOAT, TYPE_INT):  # Al menos un operando es flotante
							result = fmod(op1, op2) if op2 != 0 else 0
							#_:
								#result = 0  # Manejo por defecto si los tipos no son compatibles
						
						if ((op1T == "int") and (op2T == "int")):
							result = int(result)
							auxT = "int"
						elif (((op1T == "float") and (op2T == "int")) or ((op1T == "int") and (op2T == "float")) or ((op1T == "float") and (op2T == "float"))):
							result = float(result)
							auxT = "float"
					"POT":
						result = pow(op1, op2)  # Potencia usando la función `pow`
						
						if ((op1T == "int") and (op2T == "int")):
							result = int(result)
							auxT = "int"
						elif (((op1T == "float") and (op2T == "int")) or ((op1T == "int") and (op2T == "float")) or ((op1T == "float") and (op2T == "float"))):
							result = float(result)
							auxT = "float"
				environment["variables"][args[2]] = [result, auxT]

			"JLT", "JGT", "JLE", "JGE", "JEQ", "JNE":
				var comp_result = environment["variables"].get(args[0], 0)[0]
				var label = args[1]
				#print("Comparacion")

				if ((instruction == "JLT" and comp_result < 0) or
					(instruction == "JGT" and comp_result > 0) or
					(instruction == "JLE" and comp_result <= 0) or
					(instruction == "JGE" and comp_result >= 0) or
					(instruction == "JEQ" and comp_result == 0) or
					(instruction == "JNE" and comp_result != 0)):
					if environment["labels"].has(label):
						current_line = environment["labels"][label]
					continue

			"JMP":
				#print("Salto")
				var label = args[0]
				current_line = environment["labels"].get(label, current_line)
				continue

			"OUT":
				#print("Salto")
				await get_tree().create_timer(0.0001).timeout
				#print(environment)
				var var_value = environment["variables"].get(args[0], 0)[0]
				output.append(str(var_value))
				$VBoxContainer/Resultados.text += "COUT "+args[0]+" > "+ str(var_value) +"\n"
				$VBoxContainer/Resultados.set_caret_line($VBoxContainer/Resultados.get_line_count() - 1, true)

			"IN":
				$VBoxContainer/HBoxContainer.visible = true
				$VBoxContainer/HBoxContainer/labInput.text = "Ingresar valor de variable "+args[0]+":"
				$VBoxContainer/HBoxContainer/input.grab_focus()
				await prompt_user_input()
				user_input = $VBoxContainer/HBoxContainer/input.text.to_float()
				$VBoxContainer/Resultados.text += "CIN "+args[0]+" > "+ str(user_input) +"\n"
				var op1T = environment["variables"].get(args[0], 0)[1]
				#print(user_input, "- -", typeof(user_input))
				if (op1T == "int"):
					user_input = int(user_input)
				elif (op1T == "float"):
					user_input = float(user_input)
				#print(user_input, "- -", op1T)
				environment["variables"][args[0]] = [user_input, op1T]
				$VBoxContainer/HBoxContainer/input.text = ""
				$VBoxContainer/HBoxContainer.visible = false
				$VBoxContainer/Resultados.set_caret_line($VBoxContainer/Resultados.get_line_count() - 1, true)
				
		#print(environment)
		current_line += 1
	$VBoxContainer/Resultados.text += """
	
	FIN DE LA SIMULACION
	"""
	$VBoxContainer/Resultados.set_caret_line($VBoxContainer/Resultados.get_line_count() - 1, true)
	environment["variables"]["prueba"] = 14.0
	#print(environment)

# Solicita entrada al usuario
func prompt_user_input() -> void:
	print("Esperando entrada del usuario...")
	await user_input_completed
	
	
func _input(event):
	if event.is_action_pressed("ui_accept"):
		emit_signal("user_input_completed", 0)  # Simular entrada por ahora
	if event.is_action_pressed("ui_cancel"):
		detener = true


func _on_timer_timeout():
	print("tiempo")
