# Changelog

## 0.5.0 (01/08/2026)

### Novo: Notebook Kaggle — GPU GRÁTIS com quota semanal (~30h)
- **`colab/ComfyUI_Forge_Kaggle.ipynb`**: versão do notebook adaptada pro
  Kaggle (paths `/kaggle/working`, Internet + GPU habilitadas).
- **Vantagem sobre o Colab**: quota de ~30h de GPU por semana (Colab
  derruba em 12h). Sessão ~9h, cache do modelo preservado entre sessões.
- Pipeline completo: instala ComfyUI → baixa o modelo SDXL Pixel Art
  (Sprite Shaper) → instala o workflow Studio Pro → sobe servidor →
  túnel automático + sincronização com o Forge.
- **Botão "Kaggle grátis" na tela de Configurações** (ao lado do Colab)
  + `kaggle_url` na config.
- Exe recompilado.

## 0.4.1 (01/08/2026)

### Novo: Provider Gemini (Nano Banana) — pixel art GRÁTIS sem GPU
- **Integração com a Gemini API** (`gemini_image_provider.py`): modelo
  `gemini-2.5-flash-image` (Nano Banana) no **tier gratuito** (~10
  imagens/dia, sem cartão).
- **Sem GPU, sem túnel, sem Colab** — chamada REST direta do Forge,
  imagem retornada em base64.
- Prompt mestre Studio Pro + sufixo pixel art injetado automaticamente.
- Campo **Gemini API key** na tela de Configurações + hint.
- Registrado no manager, na cadeia de fallback e no seletor da UI.
- Chave via `config/.env` (GEMINI_API_KEY) — nunca versionada.
- Exe recompilado.

### Fix: Provider SpriteCook
- Modelo padrão trocado para `gemini-3.1-flash-lite-image` (8 créditos,
  vs 12 do flash-image).
- `quality` removido do payload quando o modelo não suporta (corrige 422).
- Chave movida para `config/.env` (segurança).

## 0.4.0 (01/08/2026)

### Novo: Provider SpriteCook — pixel art profissional com API
- **Provider SpriteCook integrado** (`spritecook_provider.py`): geração de
  sprites pixel art em grid com fundo transparente **nativo**, paleta de
  cores e consistência.
- **40 créditos grátis por mês** (~5 sprites) para validar a qualidade
  antes de pagar (US$8/mês = 800 créditos ≈ 100 sprites).
- Parametrização completa: `pixel`, `pixel_perfect`, `bg_mode`,
  `resolution`, `quality`, `theme`, `colors`, `variations`.
- Campo de **API key na tela de Configurações** + hint por provider.
- Registrado no manager, na cadeia de fallback e no seletor da UI.
- Exe recompilado.

### Diagnóstico: Stable Horde não é ideal para pixel art
- Testes reais: "AIO Pixel Art" gera qualidade inconsistente (é SD 1.5,
  CFG 5.5 do SDXL não se aplica bem). Os bons modelos do Horde são
  anime/realista, não pixel art.
- Conclusão documentada: para pixel art de qualidade, usar Colab+SDXL,
  ComfyUI local ou SpriteCook. Stable Horde fica como fallback grátis.

## 0.3.1 (01/08/2026)

### Novo: Workflow Studio Pro v1 — qualidade nível estúdio
- **Workflow ComfyUI profissional** (`forge_studio_v1_workflow.json`): prompt
  mestre + negative fixo + batch de 4 variações + sampler otimizado
  (DPM++ 2M Karras, CFG 5.5, steps 28).
- **Prompt Mestre Studio Pro** integrado: estilo inspirado em Ragnarok
  Online, Zelda LttP, FF VI e Digimon, paleta harmoniosa, dithering e
  cel-shading — consistência entre todos os assets.
- **Preset "Studio Pro"** adicionado ao Forge (primeiro da lista).
- **Resoluções por categoria** (`category_specs.py`): Character 64x64,
  Mob/Pet/Item 32x32, Tiles/Dungeon 16x16 — com hint na UI.
- **Seletor de variações (batch)** na UI: 1 / 2 / 4 variações por job.
- **Stable Horde** agora usa o prompt mestre + negative do Studio Pro.
- **Notebook Colab**: nova célula baixa o workflow Studio Pro do GitHub
  automaticamente antes de iniciar o servidor.
- Config: `comfyui.steps=28`, `cfg=5.5`, `workflow=forge_studio_v1_workflow.json`,
  `batch_size=4`; seção `studio_pro` com prompts mestre/negative.

## 0.3.0 (01/08/2026)

### Novo: Stable Horde — geracao de sprites GRATIS sem Colab
- **Provider Stable Horde (AI Horde) integrado** — rede distribuida de GPUs
  comunitarias, 100% gratis, sem login (chave anonima), sem limite de GPU.
- Modelo **"AIO Pixel Art"** disponivel (pixel art dedicado) — ideal para
  o estilo Aetherva (Zelda/FF/Sea of Stars).
- **Seletor de gerador na UI de Configuracoes** — menu dropdown para trocar
  entre ComfyUI / Stable Horde / Pollinations / HuggingFace / OpenAI.
- Provider decodifica URL de imagem (API Horde retorna URL, nao base64).
- Auto-fallback em 512x512 se 1024 exigir kudos anonimo.
- **Bug #1 corrigido**: ComfyUI remoto morto nao returningEarly; agora cai
  para a cadeia de fallback (Stable Horde incluido) em vez de erro.
- Teste real: Tola gerada em 63s via Stable Horde, 0 custo.
- Exe recompilado.

## 0.2.1 (01/08/2026)

### Protótipo Aetherva — captura e pets funcionais
- Exe do Forge recompilado com o preset **"Aetherva (Zelda/FF/Sea)"**.
- `enemy_base.gd`/`.tscn`: AI de perseguição, HP, dano, `enraged()`, loot.
- Captura real: tecla **C** usa cristal e chama `CaptureSystem` (fórmula validada:
  56/100 em HP 20%, cristal raro captura em HP 5%).
- Sucesso → pet adicionado (`PetSystem`) + pet ativo **segue o jogador** (`pet_base.gd`).
- Bug corrigido: `enemy.has()` inexistente em Node → `get()` com null-check.
- Teste de captura automatizado rodado na Godot 4.7.1 (zero erros).

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
