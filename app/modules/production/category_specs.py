"""Definições de categorias de assets com resoluções dedicadas.

Segue o padrão de estúdio profissional:
- Personagens: 64x64 (tamanho in-game)
- Mobs/Pets: 32x32 (menores, mantém consistência)
- Tiles: 16x16 (tileset padrão)
- Itens/Efeitos: 32x32

A geração em alta resolução (512/1024) é feita no provider e depois
reduzida para o tamanho alvo in-game com filtro nearest (pixels nítidos).
"""

CATEGORY_SPECS = {
    "Character": {
        "label": "Character",
        "game_size": 64,
        "denoise": 0.60,
        "target": "64x64 (in-game)",
    },
    "Mob": {
        "label": "Mob",
        "game_size": 32,
        "denoise": 0.55,
        "target": "32x32 (in-game)",
    },
    "Pet": {
        "label": "Pet",
        "game_size": 32,
        "denoise": 0.55,
        "target": "32x32 (in-game)",
    },
    "Item": {
        "label": "Item",
        "game_size": 32,
        "denoise": 0.55,
        "target": "32x32 (in-game)",
    },
    "Tiles": {
        "label": "Tiles",
        "game_size": 16,
        "denoise": 0.50,
        "target": "16x16 (in-game)",
    },
    "Dungeon": {
        "label": "Dungeon",
        "game_size": 16,
        "denoise": 0.50,
        "target": "16x16 (in-game)",
    },
    "Effects": {
        "label": "Effects",
        "game_size": 32,
        "denoise": 0.50,
        "target": "32x32 (in-game)",
    },
}

GAME_SIZE_MAP = {
    "Character": 64,
    "Mob": 32,
    "Pet": 32,
    "Item": 32,
    "Tiles": 16,
    "Dungeon": 16,
    "Effects": 32,
}


def game_size_for(category: str) -> int:
    """Retorna o tamanho in-game alvo para a categoria."""
    return GAME_SIZE_MAP.get(category, 64)


def target_label(category: str) -> str:
    """Rótulo exibível com o tamanho alvo da categoria."""
    spec = CATEGORY_SPECS.get(category)
    if spec:
        return spec["target"]
    return "64x64 (in-game)"
