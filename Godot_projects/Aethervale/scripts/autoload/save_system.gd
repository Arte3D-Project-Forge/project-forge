extends Node
## SaveSystem — salvamento local em JSON (user://save/).
## Docs: docs/04_SYSTEMS.md (secao 8).

const SAVE_PATH := "user://save/player_save.json"
const SAVE_DIR := "user://save"

signal game_saved(path: String)


func save_game() -> void:
	DirAccess.make_dir_recursive_absolute(SAVE_DIR)
	var data := {
		"biome": GameState.current_biome,
		"purified_biomes": GameState.purified_biomes,
		"flags": GameState.flags,
		"player": {
			"level": PlayerStats.level,
			"xp_current": PlayerStats.xp_current,
			"xp_required": PlayerStats.xp_required,
			"stats": PlayerStats.stats,
			"attribute_points": PlayerStats.attribute_points,
		},
		"grimoire": {
			"schools": Grimoire.unlocked_schools,
			"spells": Grimoire.spells,
			"active_school": Grimoire.active_school,
		},
		"inventory": {
			"items": InventorySystem.items,
			"crystals": InventorySystem.crystals,
			"essences": InventorySystem.essence_count,
			"equipment": InventorySystem.equipment,
			"mana": InventorySystem.mana_currency,
			"prisma": InventorySystem.prisma_currency,
		},
		"pets": {
			"active": PetSystem.active_pet,
			"stable": PetSystem.stable,
		},
		"quests": {
			"active": QuestSystem.active_quests,
			"completed": QuestSystem.completed_quests,
		},
	}
	var file := FileAccess.open(SAVE_PATH, FileAccess.WRITE)
	if file == null:
		push_error("SaveSystem: nao foi possivel gravar save")
		return
	file.store_string(JSON.stringify(data, "\t"))
	game_saved.emit(SAVE_PATH)


func load_game() -> bool:
	if not FileAccess.file_exists(SAVE_PATH):
		return false
	var file := FileAccess.open(SAVE_PATH, FileAccess.READ)
	if file == null:
		return false
	var parsed = JSON.parse_string(file.get_as_text())
	if not parsed is Dictionary:
		return false

	var data: Dictionary = parsed
	GameState.current_biome = data.get("biome", "aetherport")
	GameState.purified_biomes = data.get("purified_biomes", [])
	GameState.flags = data.get("flags", {})

	var p: Dictionary = data.get("player", {})
	PlayerStats.level = p.get("level", 1)
	PlayerStats.xp_current = p.get("xp_current", 0)
	PlayerStats.xp_required = p.get("xp_required", PlayerStats.xp_required)
	PlayerStats.stats = p.get("stats", PlayerStats.stats)
	PlayerStats.attribute_points = p.get("attribute_points", 0)

	var g: Dictionary = data.get("grimoire", {})
	Grimoire.unlocked_schools = g.get("schools", [])
	Grimoire.spells = g.get("spells", {})
	Grimoire.active_school = g.get("active_school", "fogo")

	var inv: Dictionary = data.get("inventory", {})
	InventorySystem.items = inv.get("items", {})
	InventorySystem.crystals = inv.get("crystals", {})
	InventorySystem.essence_count = inv.get("essences", {})
	InventorySystem.equipment = inv.get("equipment", [])
	InventorySystem.mana_currency = inv.get("mana", 0)
	InventorySystem.prisma_currency = inv.get("prisma", 0)

	var pets: Dictionary = data.get("pets", {})
	PetSystem.active_pet = pets.get("active", {})
	PetSystem.stable = pets.get("stable", [])

	var q: Dictionary = data.get("quests", {})
	QuestSystem.active_quests = q.get("active", {})
	QuestSystem.completed_quests = q.get("completed", [])

	return true
