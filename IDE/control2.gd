extends Control

# Uso del método para guardar o sobrescribir un archivo
var ruta_del_archivo = ""
var pythonRuta = "python.exe" 
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
# Called when the node enters the scene tree for the first time.
func _ready():
	print(OS.get_name())
	print(OS.get_distribution_name())
	file_dialog = FileDialog.new()
	add_child(file_dialog)
	file_dialog.access = FileDialog.ACCESS_FILESYSTEM
	file_dialog.size = Vector2(500 , 500)
	file_dialog.use_native_dialog = true
	file_dialog.file_mode = 0
	cascada.id_pressed.connect(_on_item_pressed)
	var keywords = ["bool", "char", "double", "float", "int", "long", "short", "signed", "unsigned", "wchar_t"]
	for keyword in keywords:
		code.syntax_highlighter.add_keyword_color(keyword, Color.CRIMSON)
	keywords = ["break", "case", "continue", "default", "do", "else", "for", "goto", "if", "return", "switch", "while"]
	for keyword in keywords:
		code.syntax_highlighter.add_keyword_color(keyword, Color.CADET_BLUE)
	#file_dialog.popup_centered()
	
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
	ruta_del_archivo = file_dialog.current_file
	print(file_dialog.current_file)
	guardar_archivo("",code.text)

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	size = get_viewport().size
	$VBoxContainer.size = size
	countLnCol.text = str("Ln ",(code.get_caret_line()+1),", Col ",(code.get_caret_column()+1))

func _on_button_5_pressed():
	if code.text != "":
		_on_button_2_pressed()
		ejecutar_Python()
		resultados.text = output[output.size()-1]

# Crear un nuevo archivo (o sobrescribir si ya existe)
func guardar_archivo(ruta: String, contenido: String) -> bool:
	var file = FileAccess.open(ruta_del_archivo, FileAccess.WRITE)
	if file:
		file.store_string(code.text)
		print(code.text)
		guardado = true
		return true
	return false

func ejecutar_Python():
	OS.execute(pythonRuta,[ruta_del_archivo], output,true)
	print("Output: .",output[i],".")
	var aux = "Python was not found; run without arguments to install from the Microsoft Store, or disable this shortcut from Settings > Manage App Execution Aliases."
	if output[output.size()-1].contains(aux) and !seleccion:
		OS.execute("python.exe",[""])
		seleccion = true
	elif seleccion:
		file_dialog.file_mode = 0
		file_dialog.title = "Selecciona Python"
		file_dialog.popup_centered()
		seleccion = false

# Guardar
func _on_button_2_pressed():
	if ruta_del_archivo == "":
		file_dialog.file_mode = 4
		file_dialog.popup_centered()
		ruta_del_archivo = file_dialog.current_file
		print(file_dialog.current_file)
		guardar_archivo("",code.text)
	else:
		guardar_archivo("",code.text)
		guardado = true

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
		ruta_del_archivo = file_dialog.current_file
		var file = FileAccess.open(ruta_del_archivo, FileAccess.READ)
		if file:
			code.text = file.get_as_text()
			guardado = true
 
# Nuevo
func _on_button_3_pressed():
	if guardado == false and code.text != "":
		state = 2
		popup.popup_centered()
	else:
		code.clear()
		ruta_del_archivo = ""

# Cerrar
func _on_button_4_pressed():
	if guardado == false:
		state = 3
		popup.popup_centered()
		pass
	else:
		code.clear()
		ruta_del_archivo = ""

func _on_code_edit_text_changed():
	guardado = false
	
func _on_confirmation_dialog_confirmed():
	confirmacion = true
	match state:
		1:
			file_dialog.file_mode = 0
			file_dialog.popup_centered()
			ruta_del_archivo = file_dialog.current_file
			var file = FileAccess.open(ruta_del_archivo, FileAccess.READ)
			if file:
				code.text = file.get_as_text()
				guardado = true
		2:
			code.clear()
			ruta_del_archivo = ""
		3:
			code.clear()
			ruta_del_archivo = ""
		var other:
			pass


func _on_confirmation_dialog_canceled():
	confirmacion = false

# Lexico
func _on_button_6_pressed():
	_on_button_2_pressed()
	OS.execute("python.exe",["C:\\Users\\yo130\\Documents\\IDE\\python\\AnalizadorLexico.py","-f",ruta_del_archivo], output,true)
	print(output[output.size()-1])
	var file = FileAccess.open("res://python/lexico.txt", FileAccess.READ)
	lex.text = file.get_as_text()
	$VBoxContainer/VSplitContainer/HSplitContainer/TabContainer2.current_tab = 0
	file = FileAccess.open("res://python/errors.txt", FileAccess.READ)
	errLex.text = file.get_as_text()
	$VBoxContainer/VSplitContainer/HBoxContainer3/TabContainer.current_tab = 0
