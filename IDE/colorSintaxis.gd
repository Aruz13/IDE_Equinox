extends CodeHighlighter

const KEYWORD_COLOR := Color("#ff7085")
const KEYWORDS := ["int", "float", "var"]

func _ready():
	_init()

func _init() -> void:
	for word in KEYWORDS:
		add_keyword_color(word, KEYWORD_COLOR)
