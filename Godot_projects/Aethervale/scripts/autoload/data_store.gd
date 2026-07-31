extends Node
## DataStore — carrega todos os JSON de data/ em memoria.
## Os dados de design vivem em arquivos JSON para facil balanceamento
## (e para o Project Forge poder gerar/ajustar conteudo depois).

const DATA_DIR := "res://data/"

var monsters: Dictionary = {}
var magias: Dictionary = {}
var biomes: Dictionary = {}
var dungeons: Dictionary = {}
var pets: Dictionary = {}
var items: Dictionary = {}
var quests: Dictionary = {}
var dialogue: Dictionary = {}
var loot_tables: Dictionary = {}


func _ready() -> void:
	_load_all()


func _load_all() -> void:
	monsters = _load_json("monsters.json")
	magias = _load_json("magias.json")
	biomes = _load_json("biomes.json")
	dungeons = _load_json("dungeons.json")
	pets = _load_json("pets.json")
	items = _load_json("items.json")
	quests = _load_json("quests.json")
	dialogue = _load_json("dialogue.json")
	loot_tables = _load_json("loot_tables.json")


func _load_json(file_name: String) -> Dictionary:
	var path := DATA_DIR + file_name
	if not FileAccess.file_exists(path):
		push_warning("DataStore: arquivo ausente -> %s" % path)
		return {}
	var file := FileAccess.open(path, FileAccess.READ)
	if file == null:
		push_warning("DataStore: nao foi possivel ler -> %s" % path)
		return {}
	var parsed = JSON.parse_string(file.get_as_text())
	if parsed is Dictionary:
		return parsed
	push_warning("DataStore: JSON invalido -> %s" % path)
	return {}
