extends CharacterBody2D
## Player — movimento do Mago Mestre (8 direcoes), mira no mouse e casting.

const SPEED := 120.0

@onready var sprite: Sprite2D = $Sprite2D
@onready var animation: AnimationPlayer = $AnimationPlayer if has_node("AnimationPlayer") else null


func _ready() -> void:
	add_to_group("player")
	_face(Vector2.RIGHT)


func _physics_process(delta: float) -> void:
	var direction := Input.get_vector("move_left", "move_right", "move_up", "move_down")
	velocity = direction * SPEED
	move_and_slide()

	if direction != Vector2.ZERO:
		_face(direction)
		if animation != null and animation.has_animation("walk"):
			animation.play("walk")
	elif animation != null and animation.has_animation("idle"):
		animation.play("idle")


func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventMouseButton:
		if event.button_index == MOUSE_BUTTON_LEFT and event.pressed:
			_cast_primary()
		elif event.button_index == MOUSE_BUTTON_RIGHT and event.pressed:
			_cast_secondary()
	elif event is InputEventKey and event.pressed and not event.echo:
		if event.keycode == KEY_C:
			_try_capture()


func _try_capture() -> void:
	var enemy := _nearest_enemy()
	if enemy == null:
		return
	if enemy is Node and enemy.has_method("is_capturable") and not enemy.is_capturable():
		return
	var rarity := "common"
	if not InventorySystem.use_crystal(rarity):
		rarity = "rare"
		if not InventorySystem.use_crystal(rarity):
			rarity = "legendary"
			if not InventorySystem.use_crystal(rarity):
				return
	CaptureSystem.try_capture(enemy, rarity)


func _nearest_enemy() -> Node:
	var best: Node = null
	var best_dist := 90.0
	for enemy in get_tree().get_nodes_in_group("enemies"):
		var d := global_position.distance_to(enemy.global_position)
		if d < best_dist:
			best_dist = d
			best = enemy
	return best


func _cast_primary() -> void:
	var spell := _primary_spell()
	if spell.is_empty():
		return
	var cost: int = spell.get("custo", 5)
	if not PlayerStats.try_spend_mana(cost):
		return
	_fire_projectile(spell)


func _cast_secondary() -> void:
	var spell := _secondary_spell()
	if spell.is_empty():
		return
	var cost: int = spell.get("custo", 8)
	if not PlayerStats.try_spend_mana(cost):
		return
	_fire_projectile(spell)


func _primary_spell() -> Dictionary:
	var school: String = Grimoire.active_school
	for spell_id in DataStore.magias:
		var s: Dictionary = DataStore.magias[spell_id]
		if s.get("escola", "") == school and Grimoire.has_spell(spell_id):
			return s
	return {}


func _secondary_spell() -> Dictionary:
	# Prototipo: retorna o primeiro feitico de "escudo" (nao projetil).
	for spell_id in DataStore.magias:
		var s: Dictionary = DataStore.magias[spell_id]
		if Grimoire.has_spell(spell_id) and not s.get("projetil", false):
			return s
	return {}


func _fire_projectile(spell: Dictionary) -> void:
	var projectile := preload("res://scripts/combat/projectile.gd").new()
	var aim := get_global_mouse_position() - global_position
	if aim.length() == 0:
		aim = Vector2.RIGHT
	var dir := aim.normalized()
	# Nota: no prototipo o projétil é um nó simples; a cena real
	# projectile.tscn será criada junto com os sprites.
	var proj := Area2D.new()
	proj.position = global_position + dir * 16.0
	proj.add_child(_make_visual(spell))
	get_tree().current_scene.add_child(proj)
	proj.set_script(projectile)
	proj.setup(spell, dir)


func _make_visual(spell: Dictionary) -> Node:
	var col := ColorRect.new()
	col.color = _school_color(spell.get("escola", "fogo"))
	col.size = Vector2(8, 8)
	return col


func _school_color(school: String) -> Color:
	return {
		"fogo": Color(1.0, 0.4, 0.2),
		"gelo": Color(0.5, 0.8, 1.0),
		"vento": Color(0.7, 0.9, 0.6),
		"terra": Color(0.7, 0.5, 0.3),
		"agua": Color(0.3, 0.6, 1.0),
		"trovao": Color(1.0, 0.9, 0.3),
		"luz": Color(1.0, 1.0, 0.8),
		"sombra": Color(0.5, 0.3, 0.7),
	}.get(school, Color.WHITE)


func _face(direction: Vector2) -> void:
	if absf(direction.x) > absf(direction.y):
		sprite.flip_h = direction.x < 0
