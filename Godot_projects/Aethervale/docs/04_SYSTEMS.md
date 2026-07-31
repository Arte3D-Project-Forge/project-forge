# SISTEMAS DE GAMEPLAY — AETHERVA

> Detalhes técnicos de design dos sistemas. Leia `01_GDD.md` primeiro.

---

## 1. SISTEMA DE CAPTURA DE MONSTROS

### 1.1 Fluxo completo
```
1. [Combate] Reduzir HP do monstro (≤ 30% ideal)
2. [Opcional] Aplicar status/marca do elemento fraco (aumenta vínculo)
3. [Ação] Usar Cristal de Captura (item consumível)
4. [Cálculo] chance = base_captura × (0.4 + HP_restante% × 0.6) × vínculo × bônus
5. [Sucesso] Essência capturada → escolha: Pet / Essência de evolução / Bestiário
6. [Falha] Monstro fica "enraivecido" (+25% dano por 10s); cristal consumido
```

### 1.2 Fórmula de captura
```
chance_final = base × (1 - hp_frac) × vinculo × status_bonus × item_bonus

base          = valor da espécie (ex.: Tola 0.60)
hp_frac       = HP atual / HP máximo
vinculo       = 1.0 normal; 1.15 com element fraco aplicado; 0.85 sem combate
status_bonus  = 1.3 se o monstro está queimado/congelado/etc.
item_bonus    = 1.0 cristal comum; 1.25 cristal raro; 1.5 cristal lendário
```

### 1.3 Tipos de essência capturada
| Tipo | Uso |
|---|---|
| **Essência de Pet** | Cria um pet daquela espécie |
| **Essência de Evolução** | Acumular N para evoluir pet/grimório |
| **Essência de Bestiário** | Registro de coleção (+ bônus de SOR) |

### 1.4 Itens de captura
| Item | Efeito | Onde |
|---|---|---|
| Cristal Comum | chance base | loja Aetherport |
| Cristal Raro | +25% | baús raros |
| Cristal Lendário | +50% | calabouços / bosses |
| Isca de Mana | atrai monstro raro por 30s | alquimista |

---

## 2. SISTEMA DE PETS

### 2.1 Estrutura de um pet
```
id (espécie)
nome
elemento
nivel_atual / exp
status: ATK, DEF, VEL, HP, MANA
habilidade_passiva
evolucao_atual (1..3)
proxima_evolucao: {requer: {essencia: N, item: X}}
```

### 2.2 Papéis do pet
| Papel | Comportamento |
|---|---|
| **Lutador** | Auto-ataca o alvo do jogador; tem ATK/DEF próprios |
| **Coletor** | Junta mana/essências/loot automaticamente |
| **Utilitário** | Ajuda em puzzles (peso, luz, escavar, voar) — por espécie |
| **Montaria (futuro)** | Velocidade no mapa |

### 2.3 Regras de troca/gerenciamento
- **1 pet ativo** (luta/coleta) + **estábulo** (na vila, até 20 slots).
- Pets acumulam EXP quando ativos; o jogador escolhe a forma de gastar.
- **Evolução:** junte `N` essências da espécie + item de evolução
  (ex.: Semente de Almaris para Terra). Evolução muda sprite e status.

### 2.4 Exemplo de evolução (Tola)
```
Tola (slime)  →  Tola de Cristal (lvl 10)  →  Tola Suprema (lvl 25, cor dourada)
```

---

## 3. SISTEMA DE COMBATE

### 3.1 Escolas elementais e interações
| Escola | Contra (efetivo) | Combo/status |
|---|---|---|
| Fogo | Terra, Gelo | queimadura (dano ao longo do tempo) |
| Gelo | Vento | congelado (parado, +dano) |
| Vento | Água | empurrão/velocidade |
| Água | Fogo | lentidão |
| Terra | Vento | escudo de pedra (absorve) |
| Trovão | Água | choque (paralisia) |
| Luz | Sombra | purifica (remove corrupção) |
| Sombra | Luz | drena mana |

### 3.2 Feitiços do Mago (exemplos iniciais)
| Feitiço | Escola | Custo | Efeito |
|---|---|---|---|
| Brasa | Fogo | 5 | projétil 10 de dano + queimadura |
| Lâmina de Vento | Vento | 5 | projétil rápido 9 |
| Pedra-Protetora | Terra | 8 | escudo 30% por 5s |
| Raio | Trovão | 8 | 12 de dano + paralisia curta |
| Corrente de Luz | Luz | 12 | 15 de dano, purifica |

### 3.3 Interface de combate
- Clique = feitiço primário; Shift+clique = secundário; Q/E = troca de escola.
- Barra de mana visível; poções na hotbar (1-4).
- Inimigos têm barras de HP (top) e indicador de "capturável" (⚠ símbolo).

---

## 4. INVENTÁRIO E ECONOMIA

### 4.1 Inventário
- Slots limitados (24 no início; expande com mochila).
- Categorias: consumíveis, cristais, essências, equipamentos, chaves, grimório.

### 4.2 Moeda
- **Mana (M)** — moeda básica (derrota/captura/venda).
- **Prisma (P)** — moeda rara (baús épicos, Vozes) — futura moeda de loja.

### 4.3 Comércio
- NPCs de Aetherport: Tayla (cristais), Brom (equipamentos/chaves),
  Puck (pets/essências). Futuro: mercado entre jogadores.

---

## 5. BAÚS DE RECOMPENSA

### 5.1 Tipos
| Raridade | Cor | Conteúdo típico |
|---|---|---|
| Comum | cinza | 20-50 mana, 1-2 poções, cristal comum |
| Raro | azul | essência, página rara, cristal raro |
| Épico | roxo | página de grimório, item de evolução, prisma |
| Lendário | dourado | essência pura, chave-mestra, item de pet único |

### 5.2 Geração de loot (em `data/loot_tables.json`)
```
{ "bioma": "vale", "raridade": "raro",
  "itens": [ { "id": "essencia_fada_negra", "peso": 4 }, ... ] }
```

---

## 6. PROGRESSÃO (REVISÃO DETALHADA)

### 6.1 Níveis de EXP
- Derrotar inimigo: `EXP = nivel_inimigo × 10 × modificador_de_bioma`.
- Capturar: `EXP = nivel × 8` + bônus de primeira captura da espécie.
- Fórmula de nível: `EXP_prox = 50 × nivel^1.4`.

### 6.2 Grimório
- Escolas desbloqueadas por essências puras (1 por bioma + Torre).
- Páginas de grimório (loot de calabouço/Vozes) liberam versos.
- Cada verso tem 3 níveis (básico/médio/mestre) melhorando dano/custo.

### 6.3 Atributos e builds
- Pontos por nível (4 por nível + 1 extra a cada 5 níveis).
- Builds sugeridas: Dano (MAG+), Sobrevivência (VIT+), Coletor (SOR+),
  Ritmo (AGI+).

---

## 7. QUÊSTES E DIÁLOGO

### 7.1 Sistema
- Quêtes em `data/quests.json` (id, título, objetivo, recompensas).
- Tipos: coletar, capturar espécie, derrotar N, explorar local, lore.
- Diálogo em `data/dialogue.json` (falas por NPC com condição de quête).

### 7.2 NPCs principais (Aetherport)
- **Tayla** — cristais/gadgets (quêtes de captura).
- **Brom** — forja (quêtes de equipamento/chaves).
- **Seer Voss** — grimório/bestiário (quêtes de lore).
- **Puck** — mercado de pets/essências.

---

## 8. SAVE / CARREGAMENTO

- Arquivo `save_player.json` (posição, inventário, pets, grimório, quêtes,
  biomas purificados, coleção).
- Auto-save em pontos de descanso + save manual na vila.
- (Futuro MMO) conta de servidor sincronizada.

---

## 9. TABELAS DE DADOS (arquivos planejados em `data/`)

```
data/monsters.json     — espécies, stats, loot, captura
data/magias.json       — grimório (escolas, versos, custos)
data/biomes.json       — biomas, clima, inimigos, baús
data/dungeons.json     — calabouços, salas, puzzles, bosses
data/pets.json         — pets, evoluções, habilidades
data/items.json        — itens, raridades, efeitos
data/quests.json       — quêtes e objetivos
data/dialogue.json     — NPCs e falas
data/loot_tables.json  — tabelas de drop por bioma/raridade
```

Todos em JSON para fácil edição (e para o Project Forge gerar/balancear depois).
