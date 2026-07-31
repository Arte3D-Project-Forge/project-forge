extends Node
## InventorySystem — itens, essencias, cristais, equipamentos.
## Docs: docs/04_SYSTEMS.md (secao 4).

signal inventory_changed
signal item_used(item_id: String)

const MAX_SLOTS := 24

var items: Dictionary = {}  # item_id -> { "count": int }
var crystals: Dictionary = {}  # crystal_type -> count
var essence_count: Dictionary = {}  # essence_id -> count
var equipment: Array[String] = []
var mana_currency: int = 0
var prisma_currency: int = 0


func add_item(item_id: String, count: int = 1) -> void:
	if items.has(item_id):
		items[item_id]["count"] += count
	else:
		items[item_id] = { "count": count }
	inventory_changed.emit()


func remove_item(item_id: String, count: int = 1) -> bool:
	if not items.has(item_id) or items[item_id]["count"] < count:
		return false
	items[item_id]["count"] -= count
	if items[item_id]["count"] <= 0:
		items.erase(item_id)
	inventory_changed.emit()
	return true


func add_crystal(crystal_type: String, count: int = 1) -> void:
	crystals[crystal_type] = crystals.get(crystal_type, 0) + count
	inventory_changed.emit()


func use_crystal(crystal_type: String) -> bool:
	if crystals.get(crystal_type, 0) <= 0:
		return false
	crystals[crystal_type] -= 1
	inventory_changed.emit()
	return true


func add_essence(essence_id: String, count: int = 1) -> void:
	essence_count[essence_id] = essence_count.get(essence_id, 0) + count
	inventory_changed.emit()


func spend_essences(essence_id: String, count: int) -> bool:
	if essence_count.get(essence_id, 0) < count:
		return false
	essence_count[essence_id] -= count
	inventory_changed.emit()
	return true


func add_mana(amount: int) -> void:
	mana_currency += amount
	inventory_changed.emit()


func spend_mana(amount: int) -> bool:
	if mana_currency < amount:
		return false
	mana_currency -= amount
	inventory_changed.emit()
	return true
