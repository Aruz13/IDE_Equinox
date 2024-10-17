extends Control

# Uso del método para guardar o sobrescribir un archivo
var docRuta = OS.get_system_dir(OS.SYSTEM_DIR_DOCUMENTS)
var ruta_del_archivo = ["", docRuta+"/python/temporal.py"]
var archivo = 0
@onready var pythonRuta = Global.pythonRuta 
@onready var ruta_Tokens = (Global.analizaLex.get_base_dir()+"/lexico.txt")
var file_dialog : FileDialog
var output = []
var i = 0
var state = 0
var guardado = false
var confirmacion = false
var seleccion = false
@onready var code = $VBoxContainer/VSplitContainer/HSplitContainer/CodeEdit
@onready var resultados = $VBoxContainer/VSplitContainer/HBoxContainer3/TabContainer/Resultados
@onready var popup = $ConfirmationDialog
@onready var menu = $VBoxContainer/HBoxContainer/MenuButton
@onready var cascada = menu.get_popup()
@onready var countLnCol = $VBoxContainer/HBoxContainer2/Label
@onready var lex = $VBoxContainer/VSplitContainer/HSplitContainer/TabContainer2/Lexico
@onready var errLex = $"VBoxContainer/VSplitContainer/HBoxContainer3/TabContainer/Errores Lexicos"
@onready var errPyt = $AcceptDialogPython
@onready var sin = $VBoxContainer/VSplitContainer/HSplitContainer/TabContainer2/Sintactico/Sintactico
@onready var sem = $VBoxContainer/VSplitContainer/HSplitContainer/TabContainer2/Semantico/Semantico
@onready var errSin = $"VBoxContainer/VSplitContainer/HBoxContainer3/TabContainer/Errores Sintacticos"
@onready var tree = $VBoxContainer/VSplitContainer/HSplitContainer/TabContainer2/Sintactico/Tree
@onready var tree2 = $VBoxContainer/VSplitContainer/HSplitContainer/TabContainer2/Semantico/Tree
@onready var fontSi = $VBoxContainer/HBoxContainer2/HBoxContainer/SpinBox
@onready var tabla = $"VBoxContainer/VSplitContainer/HBoxContainer3/TabContainer/Hash Table"
@onready var time = $Timer
var viewport

# Called when the node enters the scene tree for the first time.
func _ready():
	print(OS.get_name())
	print(OS.get_distribution_name())
	
	fontSi.value = code.get_theme_font_size("font_size")
	viewport = get_viewport()
	viewport.connect("size_changed", Callable(self, "size_changed"))
	
	file_dialog = FileDialog.new()
	add_child(file_dialog)
	file_dialog.access = FileDialog.ACCESS_FILESYSTEM
	file_dialog.size = Vector2(500 , 500)
	file_dialog.use_native_dialog = true
	file_dialog.file_mode = 0
	cascada.id_pressed.connect(_on_item_pressed)
	var keywords = ["if", "else", "do", "while", "switch", "case", "int", "float", "integer", "double", "main", "cin", "cout", "end", "until"]
	for keyword in keywords:
		code.syntax_highlighter.add_keyword_color(keyword, Color.PALE_VIOLET_RED)
	
	code.syntax_highlighter.add_color_region('\"', '\"', Color.AQUAMARINE, false)
	code.syntax_highlighter.add_color_region("\'", "\'", Color.AQUAMARINE, false)
	code.syntax_highlighter.add_color_region('//', '//', Color.DARK_GRAY, true)
	code.syntax_highlighter.add_color_region("/*", "*/", Color.DARK_GRAY, false)
	
	# code.syntax_highlighter.set_symbol_color(Color.AQUA) # setter
	# code.syntax_highlighter.get_symbol_color() # getter
	#file_dialog.popup_centered()
	size_changed()
	
func _on_item_pressed(id):
	match id:
		0:
			_on_button_3_pressed()
		1:
			_on_button_pressed()
		2:
			_on_button_2_pressed()
		3:
			_guardar_como()

func _guardar_como():
	file_dialog.file_mode = 4
	file_dialog.popup_centered()
	ruta_del_archivo[0] = file_dialog.current_file
	#print(file_dialog.current_file)
	guardar_archivo("",code.text)


func size_changed():
	size = get_viewport().size
	$VBoxContainer.size = size
	

func _on_button_5_pressed():
	archivo = 0
	_on_button_8_pressed()
	#if code.text != "":
	#	_on_button_2_pressed()
	#	ejecutar_Python()
	#	resultados.text = output[output.size()-1]
	#	$VBoxContainer/VSplitContainer/HBoxContainer3/TabContainer.current_tab = 3

# Crear un nuevo archivo (o sobrescribir si ya existe)
func guardar_archivo(ruta: String, contenido: String) -> bool:
	var file = FileAccess.open(ruta_del_archivo[archivo], FileAccess.WRITE)
	if file:
		file.store_string(code.text)
		#print(code.text)
		guardado = true
		return true
	return false

func ejecutar_Python():
	OS.execute(pythonRuta,[ruta_del_archivo[archivo]], output,true)
	#print("Output: .",output[i],".")
	var aux = "Python was not found"
	var aux2 = "No se encontró Python"
	if (output[output.size()-1].contains(aux) or output[output.size()-1].contains(aux2)) and !seleccion:
		OS.execute("python.exe",[""])
		seleccion = true
		errPyt.popup_centered()
	elif output[output.size()-1].contains(aux) and seleccion:
		file_dialog.file_mode = 0
		file_dialog.title = "Selecciona Python"
		file_dialog.popup_centered()
		if file_dialog.current_file.contains("python.exe"):
			pythonRuta = file_dialog.current_file
			Global.pythonRuta = pythonRuta
			Global.guardarRutaPython()
		seleccion = false

# Guardar
func _on_button_2_pressed() -> bool:
	print("Funcion boton")
	archivo = 0
	if ruta_del_archivo[0] == "":
		file_dialog.file_mode = 4
		file_dialog.popup_centered()
		ruta_del_archivo[0] = file_dialog.current_file
		print("Archivo seleccionado: " +file_dialog.current_file)
		if(!file_dialog.current_file):
			return false
		#print(file_dialog.current_file)
		guardar_archivo("",code.text)
		return true
	else:
		guardar_archivo("",code.text)
		guardado = true
		return true

func accionar_ejecucion() -> bool:
	print("Funcion Otra")
	if code.text != "":
		if ruta_del_archivo[archivo] == "":
			file_dialog.file_mode = 4
			file_dialog.popup_centered()
			ruta_del_archivo[0] = file_dialog.current_file
			print("Archivo seleccionado: " +file_dialog.current_file)
			if(!file_dialog.current_file):
				return false
			#print(file_dialog.current_file)
			guardar_archivo("",code.text)
			return true
		else:
			guardar_archivo("",code.text)
			guardado = true
			return true
	else:
		return false
# Abrir
func _on_button_pressed():
	if guardado == false and code.text != "":
		state = 1
		popup.popup_centered()
		pass
	else:
		file_dialog.file_mode = 0
		file_dialog.title = "Abrir Archivo"
		file_dialog.popup_centered()
		ruta_del_archivo[0] = file_dialog.current_file
		var file = FileAccess.open(ruta_del_archivo[0], FileAccess.READ)
		if file:
			code.text = file.get_as_text()
			guardado = true
			_on_button_8_pressed()
 
# Nuevo
func _on_button_3_pressed():
	if guardado == false and code.text != "":
		state = 2
		popup.popup_centered()
	else:
		code.clear()
		ruta_del_archivo[0] = ""

# Cerrar
func _on_button_4_pressed():
	if guardado == false:
		state = 3
		popup.popup_centered()
		pass
	else:
		code.clear()
		ruta_del_archivo[0] = ""

func _on_code_edit_text_changed():
	guardado = false
	archivo = 1
	time.start(0.5)
	
func _on_confirmation_dialog_confirmed():
	confirmacion = true
	match state:
		1:
			file_dialog.file_mode = 0
			file_dialog.popup_centered()
			ruta_del_archivo[0] = file_dialog.current_file
			var file = FileAccess.open(ruta_del_archivo[0], FileAccess.READ)
			if file:
				code.text = file.get_as_text()
				guardado = true
		2:
			code.clear()
			ruta_del_archivo[0] = ""
		3:
			code.clear()
			ruta_del_archivo[0] = ""
		var other:
			pass


func _on_confirmation_dialog_canceled():
	confirmacion = false

# Lexico
func _on_button_6_pressed() -> bool:
	var auxBool
	if archivo == 0:
		auxBool = _on_button_2_pressed()
	else:
		auxBool = accionar_ejecucion()
	if(auxBool):
		var aux1 = "user://python/AnalizadorLexico.py"
		var ruta_completa = ProjectSettings.globalize_path(aux1)
		# print(ruta_completa)
		OS.execute(pythonRuta,[Global.analizaLex,"-f",ruta_del_archivo[archivo]], output,true)
		print(output[output.size()-1])
		
		var aux = "Python was not found"
		var aux2 = "No se encontró Python"
		if (output[output.size()-1].contains(aux) or output[output.size()-1].contains(aux2)) and !seleccion:
			OS.execute("python.exe",[""])
			seleccion = true
			errPyt.popup_centered()
			return false
		elif output[output.size()-1].contains(aux) and seleccion:
			file_dialog.file_mode = 0
			file_dialog.title = "Selecciona Python"
			file_dialog.popup_centered()
			if file_dialog.current_file.contains("python.exe"):
				pythonRuta = file_dialog.current_file
				Global.pythonRuta = pythonRuta
				Global.guardarRutaPython()
			seleccion = false
			return false
		else:
			var texto = output[output.size()-1]
			var some_array = texto.rsplit("#?#?#?#?#?#?#?#?#?#?#", true, 1)
			var file = FileAccess.open(ruta_Tokens, FileAccess.WRITE)
			if file:
				file.store_string(some_array[0])
			file = FileAccess.open((Global.analizaLex.get_base_dir()+"/errors.txt"), FileAccess.WRITE)
			if file:
				file.store_string(some_array[1])
				
			lex.text = some_array[0]
			$VBoxContainer/VSplitContainer/HSplitContainer/TabContainer2.current_tab = 0
			errLex.text = some_array[1]
			$VBoxContainer/VSplitContainer/HBoxContainer3/TabContainer.current_tab = 0
			if texto.contains("error:"):
				var lineas = some_array[1].split("\n")
				for linea in lineas:
					if linea.contains("error:"):
						var split = linea.split("linea:")
						split = split[1].split(",")
						code.set_line_background_color((int(split[0])-1), Color(0.38, 0.235, 0.239, 0.898))
				return false
			return true
	else:
		return false

	
func _on_button_7_pressed() -> bool:
	if(_on_button_6_pressed()):
		var aux1 = "res://python/analizadorsintactico.py"
		# print(ruta_completa)
		OS.execute(pythonRuta,[Global.analizaSint,ruta_Tokens], output,true)
		print(output[output.size()-1])
		
		var aux = "Python was not found"
		if !output[output.size()-1].contains(aux):
			$VBoxContainer/VSplitContainer/HSplitContainer/TabContainer2.current_tab = 1
			
			# Dividir el string en líneas
			var lines = output[output.size()-1].split("\n")
			for line in lines:
				if line.contains("Arbol"):
					sin.text = line
			tree.clear()
			$"VBoxContainer/VSplitContainer/HBoxContainer3/TabContainer/Errores Sintacticos".text = ""
			for line in lines:
				if !line.contains("==>") and !line.contains("Arbol"):
					$"VBoxContainer/VSplitContainer/HBoxContainer3/TabContainer/Errores Sintacticos".text += line + '\n'
					$VBoxContainer/VSplitContainer/HBoxContainer3/TabContainer.current_tab = 1
			
			
			var root 
			var current_item
			var item_stack = []
			var previous_level
			for line in lines:
				if line.contains("==>"):
					var level = line.count("~")
					var text = line.strip_edges()
					var auxline = line.split("==>")
					if level == 0:
						root = tree.create_item()
						root.set_text(0, line)
						tree.hide_root = false
						current_item = root
						item_stack.append([current_item, level, auxline[1]])
						previous_level = 0
					elif level > previous_level:
						# Crear un nuevo subitem
						current_item = tree.create_item(item_stack[-1][0])
						item_stack.append([current_item, level, auxline[1]])
					elif level == previous_level:
						# Crear un nuevo item al mismo nivel
						item_stack.pop_back()
						current_item = tree.create_item(item_stack[-1][0])
						item_stack.append([current_item, level, auxline[1]])
					else:
						while level < item_stack.size() :
							item_stack.pop_back()
						current_item = tree.create_item(item_stack[-1][0])
						item_stack.append([current_item, level, auxline[1]])
					
					# Establecer el texto del item
					# print(level)
					#for item in item_stack:
						#print(item)
					#print("\n")
					current_item.set_text(0, auxline[1])
					if auxline[1].contains("Error"):
						current_item.set_collapsed(true)
						current_item.set_custom_bg_color(0, Color(1,0,0,.75), true)
						current_item.set_custom_font_size(0, 20)
						current_item.visible = false 
					previous_level = level
					
			var texto = output[output.size()-1]
			var divi = texto.rsplit("Arbol de analisis sintactico:", true, 1)
			var file = FileAccess.open((Global.analizaLex.get_base_dir()+"/ErroresSinta.txt"), FileAccess.WRITE)
			if file:
				file.store_string(divi[0])
				
			file = FileAccess.open((Global.analizaLex.get_base_dir()+"/Arbol Sintact.txt"), FileAccess.WRITE)
			if file:
				file.store_string(divi[1])
			if(divi[0].contains("Errores de sintaxis")):
				var lineas = divi[0].split("\n")
				for linea in lineas:
					if linea.contains("linea"):
						var split = linea.rsplit("linea")
						code.set_line_background_color((int(split[1])-1), Color(0.38, 0.235, 0.239, 0.898))
				return false
		else:
			return false
		return true
	else:
		return false

func _on_spin_box_value_changed(value):
	#print("cambia")
	#code.font_size = 15
	pass


func _on_button_8_pressed() -> bool:
	if(_on_button_7_pressed()):
		var aux1 = "res://python/analizadorsintactico.py"
		# print(ruta_completa)
		OS.execute(pythonRuta,[Global.analizaSeman,ruta_Tokens], output,true)
		print(output[output.size()-1])
		
		var aux = "Python was not found"
		if !output[output.size()-1].contains(aux):
			$VBoxContainer/VSplitContainer/HSplitContainer/TabContainer2.current_tab = 2
			
			# Dividir el string en líneas
			var lines = output[output.size()-1].split("\n")
			for line in lines:
				if line.contains("Arbol"):
					sem.text = line
			tree2.clear()
			$"VBoxContainer/VSplitContainer/HBoxContainer3/TabContainer/Errores Semanticos".text = ""
			for line in lines:
				if !line.contains("==>") and !line.contains("Arbol"):
					$"VBoxContainer/VSplitContainer/HBoxContainer3/TabContainer/Errores Semanticos".text += line + '\n'
					$VBoxContainer/VSplitContainer/HBoxContainer3/TabContainer.current_tab = 2
			$"VBoxContainer/VSplitContainer/HBoxContainer3/TabContainer/Errores Semanticos".text += "line" + '\n'
			
			var root 
			var current_item
			var item_stack = []
			var previous_level
			for line in lines:
				if line.contains("==>"):
					var level = line.count("~")
					var text = line.strip_edges()
					var auxline = line.split("==>")
					if level == 0:
						root = tree2.create_item()
						root.set_text(0, line)
						tree2.hide_root = false
						current_item = root
						item_stack.append([current_item, level, auxline[1]])
						previous_level = 0
					elif level > previous_level:
						# Crear un nuevo subitem
						current_item = tree2.create_item(item_stack[-1][0])
						item_stack.append([current_item, level, auxline[1]])
					elif level == previous_level:
						# Crear un nuevo item al mismo nivel
						item_stack.pop_back()
						current_item = tree2.create_item(item_stack[-1][0])
						item_stack.append([current_item, level, auxline[1]])
					else:
						while level < item_stack.size() :
							item_stack.pop_back()
						current_item = tree2.create_item(item_stack[-1][0])
						item_stack.append([current_item, level, auxline[1]])
					
					# Establecer el texto del item
					# print(level)
					#for item in item_stack:
						#print(item)
					#print("\n")
					current_item.set_text(0, auxline[1])
					if auxline[1].contains("Error"):
						current_item.set_collapsed(true)
						current_item.set_custom_bg_color(0, Color(1,0,0,.75), true)
						current_item.set_custom_font_size(0, 20)
						current_item.visible = false 
					previous_level = level
			var errores
			var texto = output[output.size()-1]
			var divi = texto.rsplit("=-=> Arbol Anotaciones <=-=", true, 1)
			var file = FileAccess.open((Global.analizaLex.get_base_dir()+"/ErroresSema.txt"), FileAccess.WRITE)
			if file:
				file.store_string(divi[0])
				errores = divi[0]
				$"VBoxContainer/VSplitContainer/HBoxContainer3/TabContainer/Errores Semanticos".text = divi[0]
			divi = divi[1].rsplit("=-=> Tabla Simbolos <=-=", true, 1)
			file = FileAccess.open((Global.analizaLex.get_base_dir()+"/ArbolSema.txt"), FileAccess.WRITE)
			if file:
				file.store_string(divi[0])
			file = FileAccess.open((Global.analizaLex.get_base_dir()+"/TablaSimbolos.txt"), FileAccess.WRITE)
			if file:
				file.store_string(divi[1])
				tabla.text = divi[1]
			if errores.contains("Error"):
				var lineas = errores.split("\n")
				for linea in lineas:
					if linea.contains("linea"):
						var split = linea.split(":")
						split = split[0].rsplit("linea")
						code.set_line_background_color((int(split[1])-1), Color(0.38, 0.235, 0.239, 0.898))
			
			
		else:
			return false
		return true
	else:
		return false


func _on_timer_timeout():
	print(archivo)
	for i in code.get_line_count():
		code.set_line_background_color(i, Color.TRANSPARENT)
	_on_button_8_pressed()


func _on_code_edit_caret_changed():
	countLnCol.text = str("Ln ",(code.get_caret_line()+1),", Col ",(code.get_caret_column()+1))
