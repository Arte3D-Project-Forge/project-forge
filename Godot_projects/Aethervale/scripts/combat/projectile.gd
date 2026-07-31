extends Area2D
## Projectile — feitico em projetil. Move na direcao e causa dano
## ao entrar em area de inimigo. Prototipo minimo.

var damage := 10
var direction := Vector2.RIGHT
var speed := 260.0
var life_time := 2.0
var status_effect := ""


func setup(spell: Dictionary, dir: Vector2) -> void:
	damage = int(spell.get("dano", 10))
	status_effect = spell.get("status", "")
	direction = dir
	monitoring = true
	body_entered.connect(_on_body_entered)
	await get_tree().create_timer(life_time).timeout
	queue_free()


func _physics_process(delta: float) -> void:
	global_position += direction * speed * delta


func _on_body_entered(body: Node) -> void:
	if body.is_in_group("player"):
		return
	if body.has_method("take_damage"):
		body.take_damage(damage)
		if status_effect != "" and body.has_method("apply_status"):
			body.apply_status(status_effect)
	queue_free()
