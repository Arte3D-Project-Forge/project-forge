# ARQUITETURA TÉCNICA — AETHERVA (Godot 4.x)

> Documento técnico para a implementação na Godot 4 (2D top-down).
> Leia `00_MASTER.md` e `01_GDD.md` primeiro.

---

## 1. STACK

| Item | Escolha |
|---|---|
| Engine | Godot 4.x (versão 4.2+ recomendada) |
| Linguagem | GDScript |
| Render | 2D, TileMap, camera2D com limite |
| Resolução | 640x360 lógica, escalada 2x → 1280x720 |
| Dados | JSON em `data/` (carregados via autoloads) |
| Persistência | JSON local (`user://save/`) |

---

## 2. ESTRUTURA DE CENAS (prevista)

```
scenes/
├── main.tscn                 — nó raiz do jogo (Player, Camera, HUD, WorldManager)
├── player/
│   └── player.tscn           — CharacterBody2D (Mago Mestre) + player.gd
├── enemies/
│   ├── enemy_base.tscn       — CharacterBody2D base (stats, AI, loot, captura)
│   └── <especies>.tscn       — 1 cena por espécie (sprite, ataques)
├── bosses/
│   ├── boss_base.tscn
│   └── vassalo_almaris.tscn, forjado_kelvin.tscn, ...
├── pets/
│   ├── pet_base.tscn         — pet ativo (segue, ataca, coleta)
│   └── tola.tscn, ...
├── items/
│   ├── crystal.tscn          — cristal de captura (consumível)
│   └── chest.tscn            — baú (raridades + loot table)
├── ui/
│   ├── hud.tscn              — vida, mana, grimório, hotbar
│   ├── dialogue.tscn         — caixa de diálogo
│   ├── capture_result.tscn   — resultado de captura
│   └── inventory.tscn        — inventário
├── villages/
│   └── aetherport.tscn       — vila central + NPCs
├── biomes/
│   ├── vale_verdejante.tscn  — TileMap + spawns + calabouço porta
│   └── brasas.tscn, profundezas.tscn, coroa.tscn
└── dungeons/
    └── tumba_almaris.tscn    — 3 salas + boss room
```

---

## 3. AUTOLOADS (singletons globais)

| Autoload | Arquivo | Responsabilidade |
|---|---|---|
| `GameState` | `scripts/autoload/game_state.gd` | Jogo geral: bioma atual, tempo, flags |
| `PlayerStats` | `scripts/autoload/player_stats.gd` | Nível, atributos, mana, XP |
| `Grimoire` | `scripts/autoload/grimoire.gd` | Escolas e feitiços desbloqueados |
| `InventorySystem` | `scripts/autoload/inventory_system.gd` | Itens, essências, cristais, equip. |
| `CaptureSystem` | `scripts/autoload/capture_system.gd` | Fórmula de captura + resultado |
| `PetSystem` | `scripts/autoload/pet_system.gd` | Pets ativos, estábulo, evolução |
| `QuestSystem` | `scripts/autoload/quest_system.gd` | Quêtes ativas e objetivos |
| `DialogueSystem` | `scripts/autoload/dialogue_system.gd` | Diálogos (carrega dialogue.json) |
| `SaveSystem` | `scripts/autoload/save_system.gd` | Save/load JSON |
| `DataStore` | `scripts/autoload/data_store.gd` | Carrega todos os JSON de data/ |

---

## 4. SCRIPTS NÚCLEO (previstos)

```
scripts/
├── autoload/ (acima)
├── player/
│   └── player.gd             — movimento 8 dir, aim, casting, colisão
├── combat/
│   ├── damageable.gd         — node componente (HP, dano, morte)
│   ├── spell.gd              — feitiço (elemento, dano, custo, animação)
│   ├── projectile.gd         — projétil
│   └── status_effect.gd      — queimadura, congelado, choque, ...
├── enemies/
│   ├── enemy_base.gd         — AI, aggro, chase, HP, loot, captura
│   ├── boss_base.gd          — fases, enrage, attacks
│   └── <especie>.gd          — comportamento específico
├── pets/
│   └── pet_base.gd           — follow, auto-attack, collect, evolve
├── items/
│   ├── chest.gd              — abrir, spawnar loot
│   └── item.gd               — pickup + efeito
└── ui/ (HUD, diálogo, captura, inventário)
```

---

## 5. MODELO DE DADOS (JSON em `data/`)

### monsters.json (exemplo)
```json
{
  "tola": {
    "nome": "Tola",
    "elemento": "terra",
    "hp": 20, "atk": 3, "def": 1, "vel": 2,
    "fraca_a": "fogo",
    "base_captura": 0.60,
    "loot": { "mana": [5, 15], "essencia_tola": 0.8 },
    "sprite": "res://assets/sprites/characters/tola.png"
  }
}
```

### magias.json (exemplo)
```json
{
  "brasa": {
    "escola": "fogo", "nome": "Brasa", "custo": 5, "dano": 10,
    "status": "queimadura", "projetil": true
  }
}
```

### pets.json (exemplo)
```json
{
  "tola": {
    "nome": "Tola", "elemento": "terra",
    "evolucoes": [
      { "nivel": 1, "sprite": "tola.png" },
      { "nivel": 10, "requer": { "essencia_tola": 3, "item": "semente_almaris" } },
      { "nivel": 25, "requer": { "essencia_tola": 6, "item": "cristal_lendario" } }
    ]
  }
}
```

---

## 6. CONTROLES (padrão)

| Ação | Tecla |
|---|---|
| Mover | WASD / setas |
| Feitiço primário | Clique esquerdo (mira no mouse) |
| Feitiço secundário | Shift + clique |
| Trocar escola | Q / E |
| Usar item | 1-4 |
| Interagir (NPC/baú) | E |
| Abrir inventário | Tab |
| Diálogo (avançar) | Espaço / Enter |
| Pausa / menu | Esc |

---

## 7. MAPA / TILEMAP

- Tile 16x16; `TileMapLayer` por camada (chão, objetos, sobreposição).
- **Navegação:** `NavigationRegion2D` para inimigos seguirem o jogador.
- **Biomas:** cenas separadas, transição via portal (troca de cena preservando
  `GameState`).
- **Áreas de combate:** `Area2D` de aggro nos inimigos.

---

## 8. FLUXO DE CAPTURA (implementação)

```
EnemyBase.gd
  → expose_essencia(): instancia "essência" quando morre/enfraquecido
  → CaptureSystem.tentar_captura(enemy, cristal):
      1. calcula chance (fórmula do SYSTEMS.md)
      2. random ≤ chance → enemy.capturado() → PetSystem.adiciona(especie)
      3. senão → enemy.enraivecido()
HUD mostra resultado (capture_result.tscn)
```

---

## 9. MILESTONES DE IMPLEMENTAÇÃO (protótipo)

| Fase | Entrega |
|---|---|
| **M0 — Fundação** | project.godot, autoloads, player mover+câmera, TileMap vazio |
| **M1 — Combate** | feitiços 3 escolas, inimigos 3 espécies, HUD (vida/mana) |
| **M2 — Captura** | cristais, fórmula, resultado, 1 pet ativo (segue) |
| **M3 — Pets** | auto-ataque, coleta, estábulo, evolução simples |
| **M4 — Mundo** | Vale Verdejante completo (tilemap, spawns, baús) |
| **M5 — Calabouço** | Tumba de Almaris (3 salas, puzzles, baús) |
| **M6 — Boss** | Voz da Cobiça + Vassalo de Almaris (2 fases) |
| **M7 — Progressão** | grimório, quêtes, NPCs Aetherport, save/load |
| **M8 — Pós-MVP** | outros 3 biomas, Torre Selada, modo MMO |

> Cada milestone termina com versão jogável (regra do AGENTS.md do Forge).

---

## 10. PADRÕES DE CÓDIGO (Godot)

- Scripts em GDScript com tipagem (`: Node2D`, `var x: int`).
- Cenas em `scenes/`, scripts junto à cena (padrão Godot) OU em `scripts/`
  com paths absolutos — escolher UMA convenção desde o início (recomenda-se
  **script ao lado da cena**, padrão Godot nativo).
- Dados nunca hardcoded; tudo via `DataStore` + JSON.
- Sinais (signals) para eventos (dano, morte, captura) em vez de acoplamento.
- Nomes em snake_case; cenas PascalCase (`player.tscn`, `Player.gd`).
