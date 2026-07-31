# GAME DESIGN DOCUMENT — AETHERVA

> GDD central do jogo. Leia `00_MASTER.md` e `02_LORE.md` primeiro.
> Status: **pré-produção**. Este documento é o contrato de design.

---

## 1. VISÃO DO PRODUTO

**Aetherva: O Juramento do Mago** é um **MMORPG 2D top-down** em pixel art
onde o jogador é um **Mago Mestre** que explora 4 biomas, captura monstros
como pets, enfrenta bosses e calabouços temáticos, e reúne as essências
dos Weavers para curar o mundo de Aetheria.

**Um parágrafo (elevator pitch):**
> "Em um mundo cujo mana está corrompido, o último Mago Mestre parte para
> purificar quatro biomas. Ele não mata os monstros — ele os compreende,
> captura suas essências e as torna seus aliados. Mas cada bioma guarda um
> segredo sombrio: uma Voz da Eclípsia, e um Guardião ancestral que precisa
> ser libertado."

**Inspirações explícitas:**
- **Zelda (ALTTP/ALBW):** exploração, calabouços com puzzles, mapas temáticos.
- **Final Fantasy (clássicos):** jornada épica, magias elementais, bosses memoráveis.
- **Ragnarok Online:** captura/evolução de pets, economia viva, classes e cidades.

---

## 2. EXPERIÊNCIA ALVO (o jogador deve sentir)

| Momento | Sensação | Inspiração |
|---|---|---|
| Primeiros passos no Vale | Maravilha + mistério | Zelda (abrir o mundo) |
| Capturar o primeiro pet | Descoberta + vínculo | RO (MVP de pet) |
| Primeiro boss (Vassalo de Almaris) | Tensão + vitória épica | FF (chefes) |
| Achar um baú raro | Emoção de loot | Zelda/RO |
| Abrir o calabouço do bioma | Aventura + desafio | Zelda dungeons |
| Purificar o Guardião | Catarse narrativa | FF/RO |

---

## 3. LOOP DE JOGO

### Loop minuto a minuto (single-player)
```
Explorar bioma
  ├─ Enfrentar/evitar inimigos
  ├─ Coletar mana, essências, baús
  ├─ Enfraquecer monstro → tentar captura
  ├─ Resolver mini-puzzles (opcional)
  └─ Falar com NPCs (quêtes, lore, comerciantes)
```

### Loop de sessão (30-60 min)
```
Entrar na vila (Aetherport)
  ├─ Pegar quêtes / vender loot / evoluir magias / gerenciar pets
  └─ Escolher destino: bioma X
Entrar no bioma → explorar → capturar/coletar → mini-boss (Voz) → calabouço
  └─ Boss do bioma (Guardião) → essência pura + loot de calabouço
```

### Loop de longo prazo (MMO)
```
Progressão de personagem → desbloqueio de grimório → pets evoluídos
  → equipamentos de calabouço → raids na Torre Selada
  → economia (mercado de pets/essências entre jogadores)
```

---

## 4. PILARES DE JOGABILIDADE (traduzidos para mecânicas)

1. **Magia compreensiva** — 6 escolas elementais; cada feitiço tem:
   - custo de mana, dano, efeito de status, animação própria.
   - "versos" ganhos em eventos do bioma (não só por nível).
2. **Captura é diálogo** — captura NÃO é aleatória pura:
   - `chance = base × (1 - HP%) × fator de vínculo` +
     bônus por usar o elemento fraco / reduzir vida / item.
   - monstrinha enfraquecida e "cantada" (mini-interação) rende mais.
3. **Mundo semântico** — cada bioma tem clima, inimigos, baús, mini-boss,
   calabouço e Guardião; explorar é recompensado com lore + grimório.
4. **Ritmo de recompensas** — baús por explorar, essências por captura,
   loot de calabouço por desafio. Curva crescente.

---

## 5. PROGRESSÃO DO PERSONAGEM

### 5.1 Níveis (como em RO: base + classe)
- **Nível de Experiência (EXP)** — sobe derrotando/capturando; dá pontos de
  atributo (MAG, VIT, AGI, SOR, ESP).
- **Nível do Grimório** — sobe com essências purificadas; libera novas
  escolas e versos (feitiços).

### 5.2 Atributos
| Atributo | Efeito |
|---|---|
| **MAG** | Dano mágico e cura |
| **VIT** | Vida máxima e defesa |
| **AGI** | Velocidade de ataque e esquiva |
| **SOR** | Sorte: chance de loot, baús e captura crítica |
| **ESP** | Mana máxima e regen de mana |

### 5.3 Grimório (árvore de magias)
```
Por escola elemental:
  Verso 1 (básico) → Verso 2 (médio) → Verso 3 (mestre) + variações (status)
Desbloqueio: essências do bioma + páginas do grimório (loot de calabouço)
```

---

## 6. COMBATE

- **Tempo real, top-down.** Mira na direção do movimento/apontada pelo mouse.
- **Ações:** 1 feitiço primário (clique), 1 secundário (shift) e 1 item (tecla).
- **Câmera:** segue o jogador; inimigos atacam ao alcance.
- **Status:** dano, cura, queimadura, congelado, choque, lentidão, envenenado.
- **Mana:** regen lento + poções; gerenciar mana é central (Mago é frágil).

### Balanço base (exemplos)
| Inimigo | HP | Dano | Fraco contra | Captura base |
|---|---|---|---|---|
| Tola (slime) | 20 | 3 | Fogo | 60% |
| Corvo de Cinza | 35 | 5 | Gelo | 45% |
| Caranguejo de Maré | 45 | 6 | Trovão | 40% |
| Anemone Sussurrante | 30 | 4 | Vento | 50% |

---

## 7. CAPTURA DE MONSTROS (sistema central)

> Ver `04_SYSTEMS.md` para fórmulas e fluxo completo.

1. Enfraqueça o monstro (HP ≤ 30% ideal).
2. (Opcional) use o elemento fraco para "marcar" o vínculo.
3. Use um **Cristal de Captura** (item consumível, vendedor/baú).
4. Sucesso → a essência vira um **Pet** (ou vira essência de evolução).
5. Falha → o monstro recua/fica enraivecido (sobe dano um pouco).

**Tipos de captura:**
- **Pet comum** — companheiro de luta/coleta.
- **Essência de evolução** — usada no grimório ou para fundir pets.
- **Essência de bestiário** — coleta (registro).

---

## 8. SISTEMA DE PETS

> Ver `04_SYSTEMS.md`.

- Cada pet tem: nível, espécie, 1 elemento, 3 status de lutador,
  evolução (forma 1 → 2 → 3), habilidade passiva.
- **Ações do pet:** lutar ao lado (auto-ataque), coletar (minérios/essências),
  ajudar em puzzles (peso, luz, escavar).
- **Lar de pets:** o jogador pode ter 1 ativo + até N guardados (estábulo na vila).
- **Evolução:** acumule essências do mesmo tipo + item de evolução.

---

## 9. BIOMAS, DUNGEONS E BOSSES (resumo)

> Mundo completo (mapa, inimigos, loot): `docs/03_WORLD.md`.

| Bioma | Weaver | Guardião (Boss) | Calabouço | Voz da Eclípsia |
|---|---|---|---|---|
| Vale Verdejante | Terra (Almaris) | **Vassalo de Almaris** (treant) | Tumba de Almaris | Cobiça |
| Serraria de Brasas | Fogo (Kelvin) | **Forjado de Kelvin** (colosso de lava) | Forja Perdida | Raiva |
| Profundezas | Água (Maralda) | **Maralda Relembrada** (leviatã) | Cripta do Coral | Esquecimento |
| Alta Coroa | Vento (Zephyrion) | **Zephyrion Cindido** (tempestade) | Ninho da Tempestade | Medo |
| (Final) | — | **Séria Corrompida** | Torre Selada | — |

---

## 10. BAÚS DE RECOMPENSA

- **Categorias:** comum (cinza), raro (azul), épico (roxo), lendário (dourado).
- **Onde:** espalhados por biomas, dentro de calabouços, após bosses e Vozes.
- **Itens:** mana, cristais de captura, poções, páginas de grimório,
  equipamentos, essências, chaves de calabouço.
- **Chave do baú:** alguns exigem chave (forjada por Brom / drops de Vozes).

---

## 11. QUÊSTES E DIÁLOGOS

- **Quête principal:** purificar 4 biomas → 4 Vozes → Torre Selada.
- **Quêtes secundárias:** NPCs da vila (coleta, captura específica, explorar,
  derrotar mini-boss, lore).
- **Diálogo:** janela de texto simples com retrato (pixel art), tecla Enter/Espaço.

---

## 12. MONETIZAÇÃO / MODELO (futuro, fora do escopo MVP)

- Grátis para jogar, cosméticos (pet skins, montarias), sem pay-to-win.
- Servidor próprio ou hospedado; loja via tokens obtidos por jogo.

---

## 13. RISCOS E DECISÕES ABERTAS

| Risco | Mitigação |
|---|---|
| Escopo grande demais | MVP: 1 bioma completo + sistemas de captura/pets |
| Multiplayer complexo | Protótipo offline primeiro; servidor simples depois |
| Conteúdo procedural vs manual | Manual para bosses/calabouços; aleatório para loot/baús |
| Balanço de captura | Fórmulas em dados JSON, facilmente ajustáveis |

---

## 14. DEFINITION OF DONE (MVP)

- [ ] Personagem jogável (movimento 8 direções, câmera, colisão).
- [ ] 1 bioma jogável (Vale Verdejante) com 6+ inimigos.
- [ ] Grimório com 3 escolas e 9 feitiços.
- [ ] Captura funcional (cristais, vínculo, falha/sucesso).
- [ ] Pet ativo (segue, luta, coleta) + 1 evolução.
- [ ] 1 mini-boss (Voz da Cobiça) e 1 boss (Vassalo de Almaris).
- [ ] 1 calabouço (Tumba de Almaris) com 3 salas + baús.
- [ ] Baús (4 raridades) e inventário.
- [ ] Quêtes básicas (NPC de Aetherport) e diálogo.
- [ ] Save/load local (JSON).
