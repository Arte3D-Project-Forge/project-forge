extends Node
## Grimoire — arvore de magias do Mago Mestre.
## Escolas elementais e versos desbloqueados (docs/04_SYSTEMS.md).

signal school_unlocked(school: String)
signal spell_unlocked(spell_id: String)
signal spell_leveled(spell_id: String, new_level: int)

var unlocked_schools: Array[String] = []
var spells: Dictionary = {}  # spell_id -> { "level": int }
var active_school: String = "fogo"


func unlock_school(school: String) -> void:
	if not unlocked_schools.has(school):
		unlocked_schools.append(school)
		school_unlocked.emit(school)
		active_school = school


func unlock_spell(spell_id: String) -> void:
	if spells.has(spell_id):
		return
	spells[spell_id] = { "level": 1 }
	spell_unlocked.emit(spell_id)


func level_up_spell(spell_id: String) -> bool:
	if not spells.has(spell_id):
		return false
	spells[spell_id]["level"] = mini(spells[spell_id]["level"] + 1, 3)
	spell_leveled.emit(spell_id, spells[spell_id]["level"])
	return true


func has_spell(spell_id: String) -> bool:
	return spells.has(spell_id)


func spell_level(spell_id: String) -> int:
	return spells.get(spell_id, {}).get("level", 0)


func set_active_school(school: String) -> void:
	if unlocked_schools.has(school):
		active_school = school
