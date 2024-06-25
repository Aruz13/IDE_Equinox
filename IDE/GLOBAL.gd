extends Node

var ruta_del_archivo = ""
var pythonRuta = "python.exe" 
var firstOpen = false
var docRuta = OS.get_system_dir(OS.SYSTEM_DIR_DOCUMENTS)
var analizaLex = docRuta+"/python/AnalizadorLexico.py"
var analizaSint = docRuta+"/python/SintAn.py"
# Called when the node enters the scene tree for the first time.
func _ready():
	leerVariables()
	crearArchivosPy()
	var ruta_completa = ProjectSettings.globalize_path("user://config1.config")
	print(ruta_completa)
	pass # Replace with function body.

func leerVariables():
	var file = FileAccess.open("user://config1.config", FileAccess.READ)
	if file:
		pythonRuta = file.get_as_text()
		firstOpen = false
	else:
		pythonRuta = "python.exe"
		firstOpen = true
	file = FileAccess.open("user://config2.config", FileAccess.READ)
	if file:
		ruta_del_archivo = file.get_as_text()
	pass


func guardarRutaPython():
	var file = FileAccess.open("user://config1.config", FileAccess.WRITE)
	print("guardar ruta python")
	if file:
		file.store_string(pythonRuta)
		print(pythonRuta)
	pass


func crearArchivosPy():
	var file = FileAccess.open("res://python/AnalizadorLexico2.py", FileAccess.READ)
	var file1 = FileAccess.open("res://python/SintAn2v5.py", FileAccess.READ)
	if file:
		print("Encuentra el archivo")
		var AnalizadorLexico = file.get_as_text()
		var directorio = DirAccess.make_dir_absolute(docRuta+"/python")
		file = FileAccess.open(docRuta+"/python/AnalizadorLexico.py", FileAccess.WRITE)
		if file:
			print("Crea el archivo Lexico")
			file.store_string(AnalizadorLexico)
		else:
			print("No creo el archivo Lexico")
	else:
		print("No lee unu Lexico")
	
	if file1:
		print("Encuentra el archivo")
		var AnalizadorSinta = file1.get_as_text()
		var directorio = DirAccess.make_dir_absolute(docRuta+"/python")
		file = FileAccess.open(docRuta+"/python/SintAn.py", FileAccess.WRITE)
		if file:
			print("Crea el archivo Sintac")
			file.store_string(AnalizadorSinta)
		else:
			print("No creo el archivo Sintac")
	else:
		print("No lee unu Sintac")
	

