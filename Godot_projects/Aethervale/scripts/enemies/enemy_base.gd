extends CharacterBody2D
## EnemyBase — base de todos os inimigos: AI de chase, HP, dano,
## loot e suporte a captura (docs/04_SYSTEMS.md).

signal died(enemy)
signal damaged(amount: int, hp: int, hp_max: int)

const ATTACK_RANGE := 18.0
const ATTACK_COOLDOWN := 1.2

var monster_id: String = "tola"
var hp_max: int = 20
var hp: int = 20
var atk: int = 3
var speed: float = 40.0
var base_capture: float = 0.6
var capture_vinculo: float = 1.0
var is_boss: bool = false

var _player: CharacterBody2D
var _aggro_range := 120.0
var _attack_timer := 0.0
var _enraged_timer := 0.0
var _statuses: Array[String] = []


func _ready() -> void:
	add_to_group("enemies")
	_player = get_tree().get_first_node_in_group("player")
	_init_from_data()
	hp = hp_max


func _init_from_data() -> void:
	if not DataStore.monsters.has(monster_id):
		return
	var data: Dictionary = DataStore.monsters[monster_id]
	hp_max = int(data.get("hp", hp_max))
	atk = int(data.get("atk", atk))
	speed = 20.0 + float(data.get("vel", 2)) * 8.0
	base_capture = float(data.get("base_captura", base_capture))
	is_boss = bool(data.get("boss", false))
	var weak: String = data.get("fraca_a", "")
	if weak != "":
		capture_vinculo = 1.15  # marcado com elemento fraco


func _physics_process(delta: float) -> void:
	_attack_timer = maxf(_attack_timer - delta, 0.0)
	if _enraged_timer > 0.0:
		_enraged_timer -= delta

	if _player == null or not is_instance_valid(_player):
		velocity = Vector2.ZERO
		move_and_slide()
		return

	var to_player: Vector2 = _player.global_position - global_position
	var distance := to_player.length()

	if distance < _aggro_range:
		# Chase simples
		velocity = to_player.normalized() * speed
		if distance < ATTACK_RANGE and _attack_timer <= 0.0:
			_attack()
	else:
		velocity = Vector2.ZERO

	move_and_slide()


func _attack() -> void:
	_attack_timer = ATTACK_COOLDOWN
	if _player.has_method("take_damage"):
		var bonus := 1.25 if _enraged_timer > 0.0 else 1.0
		_player.take_damage(int(atk * bonus))


func take_damage(amount: int) -> void:
	hp -= amount
	damaged.emit(amount, hp, hp_max)
	if hp <= 0:
		_die()


func apply_status(status_name: String) -> void:
	if not _statuses.has(status_name):
		_statuses.append(status_name)
	capture_vinculo = 1.3


func has_status() -> bool:
	return _statuses.size() > 0


func enraged() -> void:
	_enraged_timer = 10.0


func is_capturable() -> bool:
	return not is_boss


func _die() -> void:
	died.emit(self)
	_drop_loot()
	queue_free()


func _drop_loot() -> void:
	var loot: Dictionary = DataStore.monsters.get(monster_id, {}).get("loot", {})
	for item_id in loot:
		if randf() <= float(loot[item_id]):
			InventorySystem.add_item(str(item_id), 1)
	InventorySystem.add_mana(5 + int(randf() * 10))
