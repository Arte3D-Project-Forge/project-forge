extends Node
## CaptureSystem — formula de captura de monstros.
## Docs: docs/04_SYSTEMS.md (secao 1).

signal capture_success(monster_id: String)
signal capture_failed(monster_id: String)


func try_capture(enemy, crystal_rarity: String = "common") -> bool:
	var monster_id: String = enemy.monster_id
	var base_capture: float = enemy.base_capture
	var hp_frac: float = float(enemy.hp) / float(enemy.hp_max) if enemy.hp_max > 0 else 1.0
	var vinctulo: float = enemy.capture_vinculo
	var status_bonus: float = 1.0
	if enemy.has_status():
		status_bonus = 1.3

	var item_bonus: float = {
		"common": 1.0,
		"rare": 1.25,
		"legendary": 1.5,
	}.get(crystal_rarity, 1.0)

	var chance := base_capture * (1.0 - hp_frac) * vinctulo * status_bonus * item_bonus
	chance = clampf(chance, 0.05, 0.98)

	if randf() <= chance:
		capture_success.emit(monster_id)
		return true

	capture_failed.emit(monster_id)
	enemy.enraged()
	return false
