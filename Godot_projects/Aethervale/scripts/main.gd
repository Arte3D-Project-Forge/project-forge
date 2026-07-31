extends Node
## Main — cena raiz do jogo.
## Monta o mundo base (tilemap provisorio), o jogador e o HUD.
## Prototipo: gera um piso simples para o player andar.

const PlayerScene := preload("res://scenes/player/player.tscn")

@onready var player: CharacterBody2D = $Player
@onready var debug_label: Label = $DebugLabel

var is_playing := true


func _ready() -> void:
	SaveSystem.load_game()
	_player_spawn()
	_update_debug()


func _player_spawn() -> void:
	# Spawn inicial (provisorio — vila Aetherport no futuro).
	player.global_position = Vector2(320, 200)
	if PlayerStats.hp_current <= 0:
		PlayerStats.hp_current = PlayerStats.hp_max


func _update_debug() -> void:
	if not is_instance_valid(debug_label):
		return
	debug_label.text = "AETHERVA — prototipo\nBioma: %s | Nivel: %d\nHP: %d/%d | Mana: %d/%d" % [
		GameState.current_biome,
		PlayerStats.level,
		PlayerStats.hp_current,
		PlayerStats.hp_max,
		PlayerStats.mana_current,
		PlayerStats.mana_max,
	]


func _process(_delta: float) -> void:
	_update_debug()
