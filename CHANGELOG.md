# Changelog

## 0.2.0 (31/07/2026)

### Novo: Jogo Aetherva (Godot) — pré-produção completa
- Criado `Godot_projects/Aethervale/` — novo jogo MMORPG 2D top-down na Godot 4.
- **Lore do Mago Mestre** (protagonista) + mundo Aetheria com 4 biomas
  (Vale Verdejante, Serraria de Brasas, Profundezas, Alta Coroa) + Torre Selada,
  inspirado em Zelda, Final Fantasy e Ragnarok Online.
- **GDD completo** (pilares, loops, progressão, combate, baús, quêtes).
- **Sistemas**: captura de monstros, pets com evolução, baús de recompensa
  (4 raridades), dungeons e bosses por bioma.
- **Projeto Godot funcional**: `project.godot`, 10 autoloads (GameState,
  PlayerStats, Grimoire, CaptureSystem, PetSystem, InventorySystem,
  QuestSystem, DialogueSystem, SaveSystem, DataStore), cena principal,
  player com movimento/casting, projétil.
- **Dados em JSON** (`data/`): monsters, magias, pets, items, quests,
  dialogue, biomes, loot_tables, dungeons — editáveis e geráveis pelo Forge.
- Documentação completa em `Godot_projects/Aethervale/docs/`
  (00_MASTER a 06_ROADMAP).

## 0.1.0 (31/07/2026)

### Interface em janela única (UI Redesign)
- Navegação por telas dentro da mesma janela (sidebar Início / Criar Asset / Galeria / Configurações), eliminando a abertura de guias novas a cada escolha.
- Tela inicial com cards de categoria (Personagem, Inimigo, Pet, Item, Mapa, Dungeon, Efeito) com hover e ícones.
- Estúdio de produção com presets rápidos de animação (Idle, Walk, Run, Attack, Hurt, Death) e de estilo (Pixel Retro, Anime, Cartoon, Dark Fantasy, Cyberpunk, etc.), inspirado em ferramentas como BrazilGPT Spritesheet AI e Spritesheets.ai.
- Indicador de status do ComfyUI na sidebar (online/offline), atualizado automaticamente.
- Camadas legadas (`ProductionWindow`, `SpriteViewer`, `SettingsWindow`) mantidas como wrappers de compatibilidade.

### Geração profissional (ComfyUI + Colab)
- Modelo **Pixel Art Diffusion XL — Sprite Shaper** (SDXL 1024x1024) no lugar do Dreamshaper 8, via ComfyUI no Google Colab.
- Download do modelo corrigido (Civitai exige token → espelhos HuggingFace).
- Túnel automático Colab → app com sincronização via jsonblob (`ComfyUISyncPoller`).
- Notebook do Colab reescrito: célula do túnel mata processos antigos ao re-rodar, ssh (localhost.run) como primário + cloudflared (http2) como fallback com timeout.

### Qualidade de pixel art garantida
- Pixelização + quantização de cor (≤256 cores) aplicadas pelo `SpriteWorker` em todos os geradores (resultado validado: 1024x1024, 254 cores, 100% blocos 8x8 uniformes).
- Normalização para 1024px antes da pixelização (upscale x4 do servidor deixava imagens de 4096px).
- Prompt negativo anti-pintura + sufixo 8-bit configurável.

### Estilos personalizados
- Cada preset de estilo agora tem **seu próprio sufixo de prompt** (`positive_suffix`), salvo no config ao clicar no chip.

### Correções e validação
- `find_upscale_model()` descobre o modelo de upscale disponível no servidor (Colab só tinha x4plus; config pedia x2plus → HTTP 400).
- Parsing do `/object_info` do ComfyUI 0.29 (`["COMBO", {...}]`).
- Config do .exe em APPDATA corrigido (apontava para túnel morto).
- Validação ponta-a-ponta real: slime, cavaleiro e goblin vermelho feroz (pipeline APPROVED + registro no banco).
- `.gitignore` corrigido (linha `.DS_Storetest_output/` concatenada) e pastas de artefatos de teste removidas do tracking.

### Documentação
- `docs/ESTADO_ATUAL.md` criado — documento master com estado, arquitetura viva, bugs conhecidos e próximos passos (para qualquer IA continuar).
- Imagens de teste centralizadas em `docs/imagens/`.
- README, ROADMAP, ARCHITECTURE atualizados.

## Versões anteriores

### 0.0.x (fase de fundação)
- Estrutura base, camadas legadas (wizard, dashboards, módulos), providers stubs, banco de assets JSON e pipeline inicial de produção.
