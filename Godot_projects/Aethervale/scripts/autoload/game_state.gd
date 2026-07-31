extends Node
## GameState — estado geral do jogo: bioma atual, flags, tempo.
## Preserva dados entre trocas de cena (biomas/vilas/calaboucos).

var current_biome: String = "aetherport"
var current_scene_path: String = ""
var purified_biomes: Array[String] = []
var time_of_day: float = 0.0
var total_time_seconds: float = 0.0
var flags: Dictionary = {}


func set_biome(biome_id: String) -> void:
	current_biome = biome_id


func mark_purified(biome_id: String) -> void:
	if not purified_biomes.has(biome_id):
		purified_biomes.append(biome_id)
		flags["bioma_%s_purificado" % biome_id] = true


func set_flag(key: String, value: Variant = true) -> void:
	flags[key] = value


func has_flag(key: String) -> bool:
	return flags.get(key, false)


func _process(delta: float) -> void:
	time_of_day += delta
	total_time_seconds += delta
