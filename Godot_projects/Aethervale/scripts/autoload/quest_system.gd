extends Node
## QuestSystem — quetes ativas, objetivos e recompensas.
## Docs: docs/04_SYSTEMS.md (secao 7).

signal quest_started(quest_id: String)
signal quest_updated(quest_id: String)
signal quest_completed(quest_id: String)

var active_quests: Dictionary = {}  # quest_id -> { "progress": int }
var completed_quests: Array[String] = []


func start_quest(quest_id: String) -> void:
	if not DataStore.quests.has(quest_id):
		push_warning("QuestSystem: quest inexistente -> %s" % quest_id)
		return
	if active_quests.has(quest_id) or completed_quests.has(quest_id):
		return
	active_quests[quest_id] = { "progress": 0 }
	quest_started.emit(quest_id)


func progress_quest(quest_id: String, amount: int = 1) -> void:
	if not active_quests.has(quest_id):
		return
	active_quests[quest_id]["progress"] += amount
	quest_updated.emit(quest_id)
	_check_completion(quest_id)


func _check_completion(quest_id: String) -> void:
	var quest: Dictionary = DataStore.quests.get(quest_id, {})
	var objective: Dictionary = quest.get("objective", {})
	var target: int = objective.get("target", 0)
	if active_quests[quest_id]["progress"] >= target:
		active_quests.erase(quest_id)
		completed_quests.append(quest_id)
		_grant_rewards(quest.get("rewards", {}))
		quest_completed.emit(quest_id)


func _grant_rewards(rewards: Dictionary) -> void:
	if rewards.has("mana"):
		InventorySystem.add_mana(rewards["mana"])
	if rewards.has("crystal"):
		InventorySystem.add_crystal(rewards["crystal"], rewards.get("count", 1))
	if rewards.has("essence"):
		InventorySystem.add_essence(rewards["essence"], rewards.get("count", 1))
	if rewards.has("xp"):
		PlayerStats.add_xp(rewards["xp"])
