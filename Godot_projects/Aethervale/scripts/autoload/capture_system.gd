extends Node
## CaptureSystem — formula de captura de monstros.
## Docs: docs/04_SYSTEMS.md (secao 1).
##
## Recebe o node do inimigo (enemy_base.gd) que expoe:
##   monster_id, hp, hp_max, base_capture, capture_vinculo,
##   has_status(), enraged(), is_capturable()

signal capture_success(monster_id: String)
signal capture_failed(monster_id: String)

const CRYSTAL_BONUS := {
	"common": 1.0,
	"rare": 1.25,
	"legendary": 1.5,
}


func try_capture(enemy: Node, crystal_rarity: String = "common") -> bool:
	if enemy == null or not is_instance_valid(enemy):
		return false
	if not enemy.has_method("is_capturable") or not enemy.is_capturable():
		capture_failed.emit(enemy.monster_id if enemy.monster_id else "")
		return false

	var base_capture: float = enemy.base_capture
	var hp_frac: float = float(enemy.hp) / float(enemy.hp_max) if enemy.hp_max > 0 else 1.0
	var vinculo := 1.0
	if enemy.get("capture_vinculo") != null:
		vinculo = enemy.capture_vinculo

	var status_bonus := 1.0
	if enemy.has_method("has_status") and enemy.has_status():
		status_bonus = 1.3

	var item_bonus: float = CRYSTAL_BONUS.get(crystal_rarity, 1.0)

	var chance := base_capture * (1.0 - hp_frac) * vinculo * status_bonus * item_bonus
	chance = clampf(chance, 0.05, 0.98)

	if randf() <= chance:
		capture_success.emit(enemy.monster_id)
		enemy.queue_free()
		return true

	capture_failed.emit(enemy.monster_id)
	if enemy.has_method("enraged"):
		enemy.enraged()
	return false
