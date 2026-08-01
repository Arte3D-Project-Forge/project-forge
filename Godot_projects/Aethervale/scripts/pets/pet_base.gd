extends CharacterBody2D
## PetBase — pet ativo que segue o jogador.
## Docs: docs/04_SYSTEMS.md (secao 2) e roadmap M3.

const FOLLOW_DISTANCE := 24.0
const SPEED := 160.0

var pet_id: String = "tola"
var _target: Node2D
var _is_attacking := false


func _ready() -> void:
	add_to_group("pets")
	_apply_pet_data()
	_target = get_tree().get_first_node_in_group("player")


func _apply_pet_data() -> void:
	if not DataStore.pets.has(pet_id):
		return
	var data: Dictionary = DataStore.pets[pet_id]
	# usa o nivel do pet ativo para aplicar stat base simples
	var pet: Dictionary = PetSystem.active_pet
	if not pet.is_empty():
		pet_id = str(pet.get("id", pet_id))


func _physics_process(delta: float) -> void:
	if _target == null or not is_instance_valid(_target):
		velocity = Vector2.ZERO
		move_and_slide()
		return

	var to_player: Vector2 = _target.global_position - global_position
	var distance := to_player.length()

	# Fica atras do jogador (posicao inversa da direcao de movimento)
	if distance > FOLLOW_DISTANCE:
		var offset := Vector2.ZERO
		if _target is CharacterBody2D:
			var move_dir: Vector2 = _target.velocity.normalized()
			offset = -move_dir * 12.0
		var dest := _target.global_position + offset
		var dir := dest - global_position
		if dir.length() > 2.0:
			velocity = dir.normalized() * SPEED
		else:
			velocity = Vector2.ZERO
	else:
		velocity = Vector2.ZERO

	move_and_slide()
