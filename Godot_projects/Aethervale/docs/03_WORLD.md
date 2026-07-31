# O MUNDO — BIOMAS, DUNGEONS, BOSSES E INIMIGOS

> Documento de conteúdo do mundo. Leia `02_LORE.md` e `01_GDD.md` primeiro.

---

## 1. MAPA GERAL DE AETHERIA

```
                ┌─────────────┐
                │  A COROA    │  (Vento / Zephyrion)
                │  picos      │  cidade: Zephyra
                └──────┬──────┘
   ┌─────────┐        │        ┌─────────────┐
   │ BRASAS  │──────  AETHERPORT (vila central) ──────│ PROFUNDEZAS │
   │ vulcão  │        │        │ costas/abismo│  (Água)
   │ Brasil. │        │        │ cidade: Marenna
   └─────────┘        │        └─────────────┘
                ┌──────┴──────┐
                │   O VALE    │  (Terra / Almaris)
                │ florestas   │  início do jogo
                └─────────────┘
   Torre de Aether → centro do mapa (conteúdo final)
```

**Vila central:** **Aetherport** — onde o jogador começa, NPCs, lojas,
estábulo de pets, estação de grimório.

---

## 2. BIOMA 1 — O VALE VERDEJANTE (Weaver Terra: Almaris)

### Atmosfera
Floresta dourada ao amanhecer, ruínas de pedra cobertas de musgo,
luz filtrando pela copa. Melancolia suave (Zelda Lost Woods + Silent Forest).

### Inimigos (ecossistema)
| Inimigo | HP | Dano | Elemento | Fraco a | Loot | Captura |
|---|---|---|---|---|---|---|
| Tola (slime) | 20 | 3 | Terra | Fogo | essência Tola, mana | 60% |
| Vaga-lume Corrompido | 15 | 2 | Luz | Sombra/Vento | brilho de mana | 65% |
| Raposa Musgo | 32 | 5 | Terra | Gelo | pele, essência | 45% |
| Tronco Andarilho | 48 | 7 | Terra | Fogo | madeira dura | 35% |
| Fada Negra | 28 | 6 | Sombra | Luz | pó de fada | 50% |
| Coruja de Folhas (raro) | 40 | 5 | Vento | Fogo | essência rara | 30% |

### Mini-boss (Voz da Cobiça)
**O Alquimista Voss** (ex-aprendiz da Torre) — deseja a essência eterna.
Mecânica: invoca 2 totens que o curam; quebre os totens primeiro.
Recompensa: **Fragmento Puro (Cobiça)** + chave do calabouço.

### Calabouço — A TUMBA DE ALMARIS
- **Tema:** ruínas subterrâneas, tumba do Weaver.
- **Salas:** ① pátio com armadilhas de espinhos → ② câmara dos espelhos
  (puzzle de luz) → ③ sala do Guardião.
- **Baús:** 1 comum, 1 raro, 1 épico (final) — itens e página de grimório.
- **Boss: VASSALO DE ALMARIS** (treant colosso)
  - Mecânicas: arremessa tocos (dano em área), cria raízes que prendem
    o jogador; fraco contra Fogo. Liberta uma **essência pura de Terra**.

### Recompensas-chave do bioma
- Grimório: **Verso de Fogo (1)** e **Verso de Luz (1)**.
- Item de pet: **Semente de Almaris** (evolução de pets de Terra).

---

## 3. BIOMA 2 — A SERRARIA DE BRASAS (Weaver Fogo: Kelvin)

### Atmosfera
Vulcões escuros, fornalhas ancestrais, cidade-forja **Brasilume** com ferreiros.
Tom quente, tenso (FF Mt. Ordeals + RO Morroc).

### Inimigos
| Inimigo | HP | Dano | Elemento | Fraco a | Loot | Captura |
|---|---|---|---|---|---|---|
| Corvo de Cinza | 35 | 5 | Fogo | Gelo | cinza-viva | 45% |
| Salamandra | 42 | 7 | Fogo | Água | escama ígnea | 40% |
| Golem de Brasa | 60 | 9 | Fogo | Água | brasa-núcleo | 30% |
| Espectro de Fornalha | 38 | 8 | Sombra | Luz | cinza-essência | 45% |
| Elemental de Lava (raro) | 70 | 10 | Fogo | Água | essência rara | 25% |

### Mini-boss (Voz da Raiva)
**O Ferreiro Caído, Garva** — culpa a forja pela ruína de sua linhagem.
Mecânica: alterna entre ataque de braço de lava e escudo de calor (fique
em água/gelo). Recompensa: **Fragmento Puro (Raiva)** + chave.

### Calabouço — A FORJA PERDIDA
- **Tema:** fundições subterrâneas com rios de lava.
- **Salas:** ① passarela de lava (plataformas) → ② forja-gigante (mini-puzzle
  de válvulas) → ③ câmara do Guardião.
- **Boss: FORJADO DE KELVIN** (colosso de rocha derretida)
  - Mecânicas: onda de lava, socos em área, fica vulnerável ao esfriar
    (após receber Água). Fraco contra Água/Gelo.
- **Recompensa:** essência pura de Fogo; página de grimório de Fogo (2).

---

## 4. BIOMA 3 — AS PROFUNDEZAS SUSSURRANTES (Weaver Água: Maralda)

### Atmosfera
Costas enevoadas, cavernas abissais, cidade-coral **Marenna**. A música é
lenta e profunda (FF BGM submerso + RO comércio portuário).

### Inimigos
| Inimigo | HP | Dano | Elemento | Fraco a | Loot | Captura |
|---|---|---|---|---|---|---|
| Caranguejo de Maré | 45 | 6 | Água | Trovão | carapaça | 40% |
| Anemone Sussurrante | 30 | 4 | Água | Vento | tentáculo | 50% |
| Alga-Presa | 50 | 8 | Água | Fogo | essência de lodo | 35% |
| Leviatã-Mirim | 65 | 9 | Água | Trovão | escama abissal | 30% |
| Fantasma de Afogado | 40 | 7 | Sombra | Luz | essência de névoa | 45% |
| Sereia de Maré Negra (raro) | 75 | 10 | Água | Trovão | essência rara | 25% |

### Mini-boss (Voz do Esquecimento)
**O Bardo Perdido, Lian** — esqueceu a canção que selava a maré.
Mecânica: canta para invocar ondas; interrompa com Trovão. Recompensa:
**Fragmento Puro (Esquecimento)** + chave.

### Calabouço — A CRIPTA DO CORAL
- **Tema:** templo submerso parcialmente acima d'água.
- **Salas:** ① salão de marés (puzzle de elevar/abaixar água) →
  ② corredor de estátuas (atalhos) → ③ câmara do Guardião.
- **Boss: MARALDA RELEMBRADA** (leviatã de coral)
  - Mecânicas: bolhas que explodem, cauda de espinhos; muda de fase quando
    a água sobe. Fraco contra Trovão.
- **Recompensa:** essência pura de Água; grimório de Água (1).

---

## 5. BIOMA 4 — A ALTA COROA (Weaver Vento: Zephyrion)

### Atmosfera
Picos gelados acima das nuvens, santuários suspensos, cidade-águia **Zephyra**.
Tom de vento, movimento, liberdade (Zelda Sky + FF BGM aéreo).

### Inimigos
| Inimigo | HP | Dano | Elemento | Fraco a | Loot | Captura |
|---|---|---|---|---|---|---|
| Harpia Jovem | 40 | 6 | Vento | Gelo | pena de vento | 45% |
| Elemental de Tempestade | 50 | 8 | Vento | Terra | faísca pura | 40% |
| Yeti de Cume | 70 | 10 | Gelo | Fogo | pelo de yeti | 30% |
| Fantasma de Queda | 45 | 7 | Sombra | Luz | essência de névoa | 45% |
| Águia Zephyr (raro) | 80 | 11 | Vento | Gelo | essência rara | 25% |

### Mini-boss (Voz do Medo)
**A Sacerdotisa Sombria, Elar** — temia o céu e se trancou na tormenta.
Mecânica: invoca raios; use Terra para erguer um escudo de pedra.
Recompensa: **Fragmento Puro (Medo)** + chave.

### Calabouço — O NINHO DA TEMPESTADE
- **Tema:** torre vertical com correntes de ar (vento ajuda a subir).
- **Salas:** ① base com correntes de ar (plataformas) → ② câmara dos relâmpagos
  (puzzle de condução) → ③ câmara do Guardião.
- **Boss: ZEPHYRION CINDIDO** (tempestade viva)
  - Mecânicas: teletransporte de correntes, raios em alvo, ciclone central.
    Fraco contra Terra.
- **Recompensa:** essência pura de Vento; grimório de Vento (1).

---

## 6. CONTENTE FINAL — A TORRE SELADA

- **Requisito:** 4 Fragmentos Puros (Vozes) + 4 essências puras (Guardiões).
- **Boss final: MESTRA SÉRIA CORROMPIDA**
  - Mecânicas: alterna entre as 4 escolas que o jogador aprendeu (usa contra
    ele). O jogador deve mudar de elemental defensivamente; quando a essência
    pura é devolvida, ela é **purificada** (não derrotada).
- **Resolução:** fim do arco do Juramento; libera modo pós-jogo/MMO.

---

## 7. TIPOS DE BAÚS E LOOT (por bioma)

| Raridade | Cor | Conteúdo | Onde |
|---|---|---|---|
| Comum | cinza | mana, poção, cristais | bioma (espalhado) |
| Raro | azul | essência, grimório (página rara), equipamento | calabouço |
| Épico | roxo | página de grimório (mestre), item de evolução | após Vozes |
| Lendário | dourado | essência pura, chave-mestra, item de pet único | após Guardiões |

---

## 8. TEMAS DE MISSÃO POR BIOMA (quêtes secundárias)

| Bioma | Quêtes típicas |
|---|---|
| Vale | coletar 5 essências de Tola; capturar uma Coruja de Folhas; achar 3 baús |
| Brasas | resgatar minerador; coletar brasa-núcleo; derrotar 10 salamandras |
| Profundezas | limpar a maré-negra (5 alga-presa); encontrar a canção perdida |
| Alta Coroa | escalar e coletar pena de vento; acalmar 3 elementais |
| Aetherport | conectar NPCs, vender essências, evoluir 1 pet |
