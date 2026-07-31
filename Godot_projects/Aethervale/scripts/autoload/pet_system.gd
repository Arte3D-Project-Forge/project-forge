extends Node
## PetSystem — pets ativos, estabulo e evolucao.
## Docs: docs/04_SYSTEMS.md (secao 2).

signal pet_added(pet_id: String)
signal pet_evolved(pet_id: String, form: int)

var active_pet: Dictionary = {}
var stable: Array = []  # lista de pets guardados
const STABLE_MAX := 20


func add_pet(monster_id: String) -> bool:
	if not DataStore.pets.has(monster_id):
		push_warning("PetSystem: especie inexistente -> %s" % monster_id)
		return false
	var pet := {
		"id": monster_id,
		"nome": DataStore.pets[monster_id].get("nome", monster_id),
		"elemento": DataStore.pets[monster_id].get("elemento", "terra"),
		"nivel": 1,
		"exp": 0,
		"form": 0,
	}
	if active_pet.is_empty():
		active_pet = pet
	else:
		if stable.size() >= STABLE_MAX:
			return false
		stable.append(pet)
	pet_added.emit(monster_id)
	return true


func switch_pet(pet_id: String) -> void:
	for i in range(stable.size()):
		if stable[i]["id"] == pet_id:
			var old := active_pet
			active_pet = stable[i]
			stable[i] = old
			return


func evolve_pet(pet_id: String, cost: Dictionary) -> bool:
	if active_pet.is_empty() or active_pet["id"] != pet_id:
		return false
	var forms: Array = DataStore.pets[pet_id].get("evolucoes", [])
	var next_form: int = int(active_pet["form"]) + 1
	if next_form >= forms.size():
		return false
	active_pet["form"] = next_form
	pet_evolved.emit(pet_id, next_form)
	return true


func add_pet_exp(amount: int) -> void:
	if active_pet.is_empty():
		return
	active_pet["exp"] += amount
	while active_pet["exp"] >= _xp_required(active_pet["nivel"]):
		active_pet["exp"] -= _xp_required(active_pet["nivel"])
		active_pet["nivel"] += 1


func _xp_required(nivel: int) -> int:
	return 40 * nivel * nivel
