extends Node
## Main — cena raiz do jogo.
## Monta o mundo base (tilemap provisorio), o jogador e o HUD.
## Prototipo: gera um piso simples para o player andar.

const PlayerScene := preload("res://scenes/player/player.tscn")
const EnemyScene := preload("res://scenes/enemies/enemy_base.tscn")

@onready var player: CharacterBody2D = $Player
@onready var debug_label: Label = $DebugLabel

var is_playing := true


func _ready() -> void:
	SaveSystem.load_game()
	_player_spawn()
	InventorySystem.add_crystal("common", 5)
	_spawn_test_enemies()
	CaptureSystem.capture_success.connect(_on_capture_success)
	CaptureSystem.capture_failed.connect(_on_capture_failed)
	_update_debug()


func _spawn_test_enemies() -> void:
	for i in range(3):
		var enemy := EnemyScene.instantiate()
		enemy.monster_id = "tola"
		enemy.position = Vector2(200 + i * 60, 260)
		add_child(enemy)


func _on_capture_success(monster_id: String) -> void:
	PetSystem.add_pet(monster_id)
	InventorySystem.add_essence("essencia_%s" % monster_id, 1)
	_update_debug()


func _on_capture_failed(_monster_id: String) -> void:
	_update_debug()


func _player_spawn() -> void:
	# Spawn inicial (provisorio — vila Aetherport no futuro).
	player.global_position = Vector2(320, 200)
	if PlayerStats.hp_current <= 0:
		PlayerStats.hp_current = PlayerStats.hp_max


func _update_debug() -> void:
	if not is_instance_valid(debug_label):
		return
	var pet_info := "nenhum"
	if not PetSystem.active_pet.is_empty():
		pet_info = "%s (lv %d, forma %d)" % [
			PetSystem.active_pet.get("nome", "?"),
			int(PetSystem.active_pet.get("nivel", 1)),
			int(PetSystem.active_pet.get("form", 0)),
		]
	debug_label.text = "AETHERVA — prototipo\nBioma: %s | Nivel: %d\nHP: %d/%d | Mana: %d/%d\nCristais: %d | Pet: %s\n[C] captura inimigo proximo" % [
		GameState.current_biome,
		PlayerStats.level,
		PlayerStats.hp_current,
		PlayerStats.hp_max,
		PlayerStats.mana_current,
		PlayerStats.mana_max,
		int(InventorySystem.crystals.get("common", 0)),
		pet_info,
	]


func _process(_delta: float) -> void:
	_update_debug()
