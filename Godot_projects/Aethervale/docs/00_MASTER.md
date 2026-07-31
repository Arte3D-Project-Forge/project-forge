# AETHERVILLE — MMO RPG (título provisório: "Aethervale: O Juramento do Mago")

> **Documento MASTER do jogo.** Leia isto primeiro.
> Todos os documentos do jogo vivem nesta pasta (`Godot_projects/Aethervale/docs/`).
>
> Estúdio: **Forge Studio** (modo criação)
> Engine: **Godot 4.x** (2D / top-down)
> Última atualização: **31/07/2026**
> Status: **PRÉ-PRODUÇÃO — conceito + documentação**

---

## 1. IDENTIDADE DO JOGO

| Item | Descrição |
|---|---|
| **Gênero** | MMORPG 2D top-down (top view), estética pixel art |
| **Protagonista** | **Mago Mestre** (Master Mage) — arcanista supremo |
| **Inspirações** | Zelda (exploração/calabouços), Final Fantasy (jornada/classes/magias), Ragnarok Online (economia, captura de monstros, pets, mundo vivo) |
| **Plataforma** | PC (desktop), janela única |
| **Modo** | Online (servidor) com núcleo jogável offline (single-player) para prototipagem |
| **Público** | Fãs de RPG clássico, pixel art nostálgica, mundo aberto |
| **Loop central** | Explorar biomas → capturar monstros → evoluir magias → derrotar bosses → desbloquear calabouços → obter pets e baús de recompensa |

---

## 2. PILARES DE DESIGN (o que faz o jogo ser o que é)

1. **Magia é a alma** — o protagonista é um Mago Mestre; cada bioma expande sua
   biblioteca de feitiços. Combate em tempo real com magias elementais
   (fogo, gelo, trovão, terra, vento, luz).
2. **Captura e vínculo** — inspirado no sistema de pets do Ragnarok + Pokémon:
   enfraqueça o monstro e **aprisione sua essência** em um cristal de mana;
   a criatura vira um **Pet** que luta, coleta e evolui.
3. **Mundo vivo por bioma** — 4 biomas com ecossistemas próprios, inimigos
   exclusivos, mini-bosses e um **Grande Guardião** (Boss) cada.
4. **Calabouços recompensadores** — cada bioma tem 1+ calabouço temático com
   baús de recompensa, chefes e loot único.
5. **Progressão legível** — níveis, árvore de magias, bestiário, pets evoluídos,
   coleção de essências.

---

## 3. FICHA TÉCNICA RÁPIDA (para o Godot)

- **Resolução de referência:** 1280x720 (render 640x360, escala 2x).
- **Tile:** 16x16 px, câmera segue o jogador.
- **Movimento:** 4/8 direções, colisão por TileMap.
- **Autoloads previstos:** `GameState`, `PlayerStats`, `InventorySystem`,
  `CaptureSystem`, `PetSystem`, `DialogueSystem`, `QuestSystem`, `SaveSystem`.
- **Dados:** JSON em `data/` (monstros, magias, biomas, calabouços, loot).
- **Servidor (futuro):** Godot Multiplayer API ou servidor Node.js;
  protótipo roda offline com persistência local.

---

## 4. ÍNDICE DA DOCUMENTAÇÃO

| Documento | Conteúdo |
|---|---|
| `docs/00_MASTER.md` | Este arquivo |
| `docs/01_GDD.md` | Game Design Document completo |
| `docs/02_LORE.md` | **Lore do Mago Mestre + história do mundo** |
| `docs/03_WORLD.md` | Biomas, dungeons, bosses, inimigos, baús |
| `docs/04_SYSTEMS.md` | Captura, pets, inventário, progressão, combate |
| `docs/05_TECHNICAL.md` | Arquitetura Godot, cenas, scripts, dados |
| `docs/06_ROADMAP.md` | Fases de desenvolvimento e milestones |

---

## 5. ESTADO DO PROTÓTIPO

Não há projeto Godot demo em `Godot_projects` ainda (a pasta foi criada agora
com a documentação). O Forge já gera projetos Godot mínimos em
`MeuJogo/generated/JOB-*/godot/` — a base do jogo começará aqui nesta pasta.
