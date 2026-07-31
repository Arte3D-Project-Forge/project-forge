extends Node
## PlayerStats — nivel, atributos, mana, XP do Mago Mestre.
## Atributos: MAG, VIT, AGI, SOR, ESP (ver docs/01_GDD.md).

signal level_up(new_level: int)
signal mana_changed(current: int, max_mana: int)
signal hp_changed(current: int, max_hp: int)
signal xp_changed(current: int, required: int)

const XP_EXPONENT := 1.4
const BASE_XP := 50
const POINTS_PER_LEVEL := 4
const EXTRA_POINT_EVERY := 5

var level: int = 1
var xp_current: int = 0
var xp_required: int = BASE_XP
var attribute_points: int = 0

var stats := {
	"mag": 5,
	"vit": 5,
	"agi": 5,
	"sor": 5,
	"esp": 5,
}

var hp_max := 60
var hp_current := 60
var mana_max := 40
var mana_current := 40
var mana_regen_per_second := 1.0


func _process(delta: float) -> void:
	mana_current = mini(mana_current + mana_regen_per_second * delta, mana_max)
	mana_changed.emit(mana_current, mana_max)


func add_xp(amount: int) -> void:
	xp_current += amount
	while xp_current >= xp_required:
		xp_current -= xp_required
		_level_up()
	xp_changed.emit(xp_current, xp_required)


func _level_up() -> void:
	level += 1
	attribute_points += POINTS_PER_LEVEL
	if level % EXTRA_POINT_EVERY == 0:
		attribute_points += 1
	xp_required = int(BASE_XP * pow(level, XP_EXPONENT))
	hp_max = 60 + stats["vit"] * 8
	mana_max = 40 + stats["esp"] * 6
	hp_current = hp_max
	mana_current = mana_max
	level_up.emit(level)
	hp_changed.emit(hp_current, hp_max)
	mana_changed.emit(mana_current, mana_max)


func spend_attribute(attr: String, cost: int = 1) -> bool:
	if not stats.has(attr):
		return false
	if attribute_points < cost:
		return false
	attribute_points -= cost
	stats[attr] += 1
	_recalculate()
	return true


func _recalculate() -> void:
	hp_max = 60 + stats["vit"] * 8
	mana_max = 40 + stats["esp"] * 6
	hp_current = mini(hp_current, hp_max)
	mana_current = mini(mana_current, mana_max)
	hp_changed.emit(hp_current, hp_max)
	mana_changed.emit(mana_current, mana_max)


func try_spend_mana(cost: int) -> bool:
	if mana_current < cost:
		return false
	mana_current -= cost
	mana_changed.emit(mana_current, mana_max)
	return true


func take_damage(amount: int) -> void:
	var defense: int = int(stats["vit"]) * 2
	var final_damage := maxi(1, amount - defense)
	hp_current = maxi(0, hp_current - final_damage)
	hp_changed.emit(hp_current, hp_max)
	if hp_current <= 0:
		_die()


func _die() -> void:
	# Prototipo: ao morrer, volta para a vila com HP cheio.
	hp_current = hp_max
	mana_current = mana_max
	GameState.current_biome = "aetherport"
	hp_changed.emit(hp_current, hp_max)
	mana_changed.emit(mana_current, mana_max)
