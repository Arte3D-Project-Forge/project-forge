# PRODUÇÃO DE SPRITES — AETHERVA

> **Plano de arte para amanhã.** Este documento define o estilo, o processo
> de geração via Project Forge e a organização dos arquivos na Godot.
> Leia `docs/00_MASTER.md` e `docs/05_TECHNICAL.md` primeiro.

---

## 1. DIRETOR DE ARTE: O ESTILO "AETHERVA"

Combina três referências com uma identidade própria:

| Referência | O que emprestamos |
|---|---|
| **Zelda (ALTTP/ALBW)** | Silhuetas claras, leitura rápida, mundo orgânico, paletas calorosas |
| **Final Fantasy (SNES)** | Proporções chibi-épicas, detalhe nas armaduras, bosses imponentes |
| **Sea of Stars** | **HD 2D Pixel Art**: luz volumétrica, sombras suaves, profundidade de campo, animação fluida, cenários detalhados |

### 1.1 Decisão técnica
- **Estilo base:** **HD 2D Pixel Art** (16-bit estendido) — é o que melhor
  combina os três e fica bonito + funcional na Godot 4.
- **Tamanho dos sprites de personagens:** **32x32 px** (quadro) — escala 1x
  no jogo; consistente com Zelda.
- **Tiles do cenário:** **16x16 px**, desenhados para compor blocos 32x32.
- **Bosses:** 64x64 ou 96x96 (2-3x o jogador).
- **Fundo:** pintado em pixel, com luz/atmosfera (estilo Sea of Stars).
- **Paleta:** terrosos quentes (Vale), vermelhos/laranjas (Brasas),
  azuis/verdes profundos (Profundezas), brancos/celestes (Alta Coroa).

### 1.2 Regras de qualidade (não negociável)
1. **Contorno escuro** limpo (leitura em cima de qualquer fundo).
2. **Sombreado** em 2-3 tons (luz + meia-tinta + sombra), nunca 1 tom chapado.
3. **Olhos/rosto legíveis** mesmo em 32x32.
4. **Pixels consistentes** (sem "pintura a pincel"); blocos uniformes.
5. **Direção do jogador:** 4 direções (baixo/cima/esquerda/direita) com
   espelhamento horizontal para esquerda/direita.
6. **Grid:** tudo alinhado ao grid 16px; centro de gravidade no pé.

---

## 2. PROCESSO DE GERAÇÃO VIA PROJECT FORGE

O Forge (ComfyUI + Pixel Art Diffusion XL Sprite Shaper) gera a base; depois
passamos pelo fluxo automático: **fundo transparente → pixelização → 256 cores**.

### 2.1 Como gerar
1. Abrir o Forge → **Criar Asset**.
2. Selecionar categoria (Character / Mob / Pet / Item / Tiles / Dungeon).
3. Clicar no chip de estilo **"Aetherva (Zelda/FF/Sea)"** (novo preset,
   adicionado em 31/07 — aplica sufixo dedicado no config).
4. Digitar prompt do asset (ver seção 3).
5. Gerar (ComfyUI conectado) → salvar em `Godot_projects/Aethervale/assets/`.

### 2.2 Organização dos arquivos (NÃO QUEBRAR)
```
Godot_projects/Aethervale/assets/
├── sprites/
│   ├── characters/          → player_mage/*.png, npc_tayla.png, ...
│   ├── enemies/             → tola.png, raposa_musgo.png, ...
│   ├── bosses/              → vassalo_almaris.png, ...
│   ├── pets/                → pet_tola.png, pet_coruja.png, ...
│   ├── tilesets/            → vale_tileset.png, brasas_tileset.png, ...
│   └── items/               → crystal.png, potion.png, chest_*.png, ...
├── backgrounds/             → vale_fundo.png, ...
└── audio/                   → (futuro)
```

> Cada sprite gerado pelo Forge sai em `MeuJogo/sprites/<nome>/` — **copiar**
> para o caminho acima. Manter os metadados (`sprite_generation.json`) numa
> pasta `assets/_meta/` para auditoria de prompts.

### 2.3 Filtro do que manter
- Gerar 2-3 variações por asset; escolher a melhor pela regra 1.2.
- Se sair "pintado" (gradiente), regerar com o sufixo Aetherva (já aplica
  hard pixels) — a pixelização do worker corrige automaticamente.

---

## 3. LISTA DE PRODUÇÃO (ordem recomendada)

> Estilo de prompt a usar no Forge: **"HD 2D pixel art, [descrição], Zelda
> style, Final Fantasy inspired, full body, top-down, game sprite"**.
> O preset Aetherva adiciona o resto automaticamente.

### Fase A — PROTAGONISTA E PET INICIAL (prioridade)
| Asset | Prompt (descrição) | Destino |
|---|---|---|
| Mago Mestre (4 dir) | "young master mage, blue robes, silver trim, magical staff, white hair" | `characters/player_mage/` |
| Neb (coruja familiar) | "small glowing white owl companion, blue eyes" | `pets/pet_neb/` |
| Tola (slime) | "small green slime monster, gooey, cute face" | `enemies/tola/` + `pets/pet_tola/` |

### Fase B — VALE VERDEJANTE (MVP)
| Asset | Prompt | Destino |
|---|---|---|
| Raposa Musgo | "moss fox creature, forest colors" | `enemies/raposa_musgo/` |
| Tronco Andarilho | "walking tree stump enemy, mossy" | `enemies/tronco_andarilho/` |
| Fada Negra | "dark fairy, corrupted purple glow" | `enemies/fada_negra/` |
| Vaga-lume | "glowing firefly creature" | `enemies/vagalume/` |
| Tileset do Vale | "grass, dirt path, flowers, tree canopy, water, cliff" (2-3 tiles) | `tilesets/vale_tileset.png` |
| Baús (4 raridades) | "treasure chest, wooden/blue/purple/gold" | `items/chests/` |
| Cristal de Captura | "capture crystal, blue mana gem" | `items/crystal_capture/` |
| Poções | "mana potion, health potion, pixel art" | `items/potions/` |

### Fase C — NPCs E VILA (Aetherport)
| Asset | Prompt | Destino |
|---|---|---|
| Tayla (inventora) | "young inventor girl, goggles, tinkerer" | `characters/npc_tayla/` |
| Brom (ferreiro) | "dwarf blacksmith, apron, hammer" | `characters/npc_brom/` |
| Seer Voss | "old librarian mage, glasses, robes" | `characters/npc_voss/` |
| Puck (mercador) | "traveling merchant, backpack, hat" | `characters/npc_puck/` |
| Vilarejo tileset | "village stone path, wooden houses, lantern" | `tilesets/aetherport_tileset.png` |

### Fase D — BOSS E CALABOUÇO (Vale)
| Asset | Prompt | Destino |
|---|---|---|
| Vassalo de Almaris (boss) | "giant treant guardian boss, mossy, glowing eyes, imposing" | `bosses/vassalo_almaris/` |
| Calabouço tileset | "ancient stone dungeon, moss, torches, cracks" | `tilesets/tumba_tileset.png` |
| Portas/chaves | "dungeon gate, rusty key" | `items/` |

### Fase E — OUTROS BIOMAS (depois)
- Serraria de Brasas (corvo de cinza, salamandra, golem, tileset vulcânico).
- Profundezas (caranguejo, anemone, tileset coral).
- Alta Coroa (harpia, yeti, tileset gelado).

---

## 4. SPRITESHEETS E ANIMAÇÕES (plano)

- Cada personagem terá um `SpriteFrames` com animações: `idle`, `walk`
  (4 direções), `attack`, `hurt`, `death`.
- Para o MVP: animações **idle** (2-4 quadros) e **walk** (4 quadros) —
  já cobrem o essencial. Attack/hurt/death depois.
- **Formato:** PNG transparente, quadros em linha (sheet) OU arquivos separados
  `idle_0.png, idle_1.png...`. Recomenda-se **arquivos separados por quadro**
  (mais fácil de gerar/inserir no Godot).

---

## 5. CAPTURA DE MONSTROS (integrada ao protótipo)

A captura já foi implementada no protótipo Godot (31/07) — ver
`docs/04_SYSTEMS.md` e `docs/06_ROADMAP.md`. Resumo do que existe:

- `CaptureSystem` (autoload) — fórmula completa com base_captura, HP%, vínculo,
  status e bônus de cristal (comum/raro/lendário).
- `PetSystem` (autoload) — pet ativo + estábulo (20 slots) + evolução em 3 formas.
- Fluxo no jogo: enfraquecer inimigo → usar cristal → sucesso vira pet /
  falha deixa inimigo enfurecido.

**Para terminar amanhã (M2/M3 do roadmap):**
1. `enemy_base.tscn` com AI de chase + barra de HP + método `enraged()`.
2. Item de cristal consumível (hotbar) que chama `CaptureSystem.try_capture`.
3. Cena de resultado de captura (HUD).
4. Pet ativo seguindo o jogador (Node2D com colisão leve).

---

## 6. CHECKLIST PARA AMANHÃ (ordem de execução)

- [ ] 1. Reabrir Forge → verificar ComfyUI conectado (rodar célula 8 se cair).
- [ ] 2. Gerar Fase A (Mago, Neb, Tola) com preset "Aetherva (Zelda/FF/Sea)".
- [ ] 3. Copiar sprites para `assets/sprites/...` (organização da seção 2.2).
- [ ] 4. Inserir no Godot: criar `player.gd` com AnimatedSprite2D + `SpriteFrames`.
- [ ] 5. Implementar `enemy_base.tscn` (AI) + `capture_item.tscn` (cristal).
- [ ] 6. Testar: derrotar/capturar uma Tola → pet segue o Mago.
- [ ] 7. Gerar Fase B (Vale: inimigos, tileset, baús) e montar o TileMap.
