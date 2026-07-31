extends Node
## DialogueSystem — dialogo por NPC com condicoes de quest.
## Docs: docs/04_SYSTEMS.md (secao 7).

signal dialogue_started(npc_id: String)
signal dialogue_finished(npc_id: String)

var current_npc: String = ""
var current_index: int = 0
var current_lines: Array = []


func start(npc_id: String) -> void:
	var all_dialogues: Dictionary = DataStore.dialogue.get(npc_id, {})
	current_lines = _matching_lines(all_dialogues)
	current_npc = npc_id
	current_index = 0
	dialogue_started.emit(npc_id)


func _matching_lines(all_dialogues: Dictionary) -> Array:
	# all_dialogues: { "default": [...], "quest_x": [...], ... }
	if all_dialogues.has("quest"):
		var quest_lines = all_dialogues["quest"]
		if quest_lines is Array:
			return quest_lines
	if all_dialogues.has("default"):
		return all_dialogues["default"]
	return []


func has_next() -> bool:
	return current_index < current_lines.size()


func next_line() -> String:
	if current_index >= current_lines.size():
		return ""
	var line: String = current_lines[current_index]
	current_index += 1
	if not has_next():
		dialogue_finished.emit(current_npc)
	return line


func is_finished() -> bool:
	return current_index >= current_lines.size()
