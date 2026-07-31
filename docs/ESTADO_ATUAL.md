# PROJECT FORGE — Estado Atual do Projeto (Master Doc)

> **LEIA ISTO PRIMEIRO.** Este documento é o mapa oficial do projeto.
> Qualquer IA ou desenvolvedor deve começar por aqui para entender
> o que o Project Forge é, o que funciona hoje, o que foi feito,
> o que está pendente e como continuar.
>
> Última atualização: **31/07/2026** (sessão completa de validação)
> Status geral: **FUNCIONANDO** (geração profissional ponta-a-ponta)
>
> **NOVO (31/07 tarde):** o projeto de jogo **Aetherva** (Godot) começou —
> pré-produção completa em `Godot_projects/Aethervale/docs/`.

---

## 1. O QUE É O PROJECT FORGE

**Project Forge é um Sistema Operacional de Desenvolvimento de Jogos
impulsionado por IA** (AI Game Development Operating System).

Ele não apenas gera assets: ele **orquestra uma pipeline de produção**
completa — do prompt até o asset pronto para a engine.

A missão (AGENTS.md): *"Project Forge deve se tornar o sistema
operacional definitivo para desenvolvimento de jogos assistido por IA."*

### O que ele faz hoje (funcional)
- Interface desktop (Python + CustomTkinter) em **janela única** com sidebar
  (Início / Criar Asset / Galeria / Configurações).
- Geração de sprites de jogo com **pixel art profissional**:
  - **ComfyUI no Google Colab** (GPU gratuita) com o modelo
    **Pixel Art Diffusion XL — Sprite Shaper** (SDXL 1024x1024).
  - Túnel automático + sincronização de URL (o app descobre sozinho).
  - Fallback para Pollinations / HuggingFace quando o ComfyUI está offline.
- Pipeline de produção completa: package, manifest, prompts, lore,
  sprites, tiles, animações, áudio, Godot, quality check, banco de dados.

---

## 2. CAMINHO VIVO DO CÓDIGO (o que importa)

Este é o fluxo real da aplicação. **Só edite/modifique o que está neste caminho.**

```
run.py
  └── app/main.py                       (ForgeApp — janela única + sidebar)
        ├── app/ui/home_view.py         (HomeView — cards de categoria)
        ├── app/ui/forge_view.py        (ForgeView base + paleta de cores)
        ├── app/modules/production/ui/production_window.py
        │     └── ProductionView        (ESTÚDIO — tela principal de criação)
        ├── app/ui/sprite_viewer.py     (GalleryView — galeria de sprites)
        └── app/ui/settings_window.py   (SettingsView — config ComfyUI/túnel)

create_job() (no ProductionView)
  └── ProductionJob (app/production/production_job.py)
        └── PipelineRunner (app/production/pipeline/pipeline_runner.py)
              ├── PackageBuilder / ManifestBuilder / PromptBuilder / ReadmeBuilder
              └── SpriteWorker (app/ai/workers/sprite_worker.py)
                    └── ImageProviderManager (app/ai/manager/image_provider_manager.py)
                          ├── ComfyUIProvider (app/ai/providers/images/comfyui_provider.py)  ← QUALIDADE MÁXIMA
                          ├── PollinationsProvider (fallback)
                          └── HuggingFaceProvider (fallback)

Sincronização do túnel:
  app/services/comfyui_sync.py → ComfyUISyncPoller (8s) → atualiza config
  app/main.py → _start_status_poller (10s) → indicador sidebar
```

**Arquivos de configuração importantes:**
- `config/forge_config.json` — TODA a configuração (modelos, prompts, túnel).
- `config/workflows/comfyui_sprite_workflow.json` — workflow básico.
- `config/workflows/comfyui_sprite_upscale_workflow.json` — workflow com upscale.
- `colab/ComfyUI_Forge_Notebook.ipynb` — notebook do Colab (modelo + servidor + túnel).
- `ProjectForge.spec` — build do .exe (PyInstaller, entry = run.py).

---

## 3. SISTEMA DE GERAÇÃO PROFISSIONAL (como funciona)

### 3.1 Visão geral
O Forge usa um modelo SDXL profissional especializado em pixel art rodando
num servidor ComfyUI no Google Colab. O app se conecta via túnel HTTPS.

### 3.2 Modelo profissional
| Item | Valor |
|---|---|
| Nome | **Pixel Art Diffusion XL — Sprite Shaper** |
| Arquivo | `pixelArtDiffusionXL_spriteShaper.safetensors` (~6.9 GB) |
| Base | SDXL 1.0 |
| Resolução de geração | 1024x1024 |
| Upscale | RealESRGAN (x4plus disponível no servidor; o provider descobre sozinho) |
| Output final | 1024x1024, ≤256 cores, 100% blocos 8x8 uniformes (pixel art real) |

**URLs de download (Civitai NÃO funciona — exige token e retorna HTML):**
```
https://huggingface.co/AIWorksMD/pixelArtDiffusionXL/resolve/main/pixelArtDiffusionXL_spriteShaper.safetensors
https://huggingface.co/nncyberpunk/SDXL1.0_PixelArtDiffusionXL_SpriteShaper/resolve/main/SDXL1.0_PixelArtDiffusionXL_SpriteShaper.safetensors
```
Upscale: `https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.1/RealESRGAN_x2plus.pth`

### 3.3 Workflow ComfyUI (o que roda no servidor)
```
CheckpointLoaderSimple → pixelArtDiffusionXL_spriteShaper.safetensors
EmptyLatentImage → 1024x1024
CLIPTextEncode (positive / negative)
KSampler → 28 steps, CFG 7, sampler dpmpp_2m, scheduler karras, seed=hash(prompt)
VAEDecode
UpscaleModelLoader → RealESRGAN (descoberto automaticamente via /object_info)
ImageUpscaleWithModel (x4)
SaveImage
```
O provider (`ComfyUIProvider.build_workflow`) preenche placeholders
(`__CHECKPOINT__`, `__PROMPT__`, etc.) e envia para `/prompt`.
Se o workflow de upscale falhar (ex.: modelo não existe no servidor),
**cai para o workflow básico automaticamente**.

### 3.4 Túnel automático (Colab → app)
1. O Colab roda a **célula 8** do notebook: sobe túnel e **publica a URL**
   num blob do jsonblob.com (o link é fixo/hardcoded nos dois lados).
2. O app vigia o blob a cada 8s (`ComfyUISyncPoller`); quando a URL muda
   e está viva, grava em `comfyui.server_url` da config.
3. Ordem de tentativa do túnel no Colab:
   **ssh localhost.run (lhr.life) → serveo.net → cloudflared (trycloudflare)**.
   - O cloudflared puro costuma falhar no Colab (QUIC/UDP bloqueado);
     usa-se `--protocol http2` quando tentado.
   - Na prática, **localhost.run via ssh é o que funciona** no Colab do usuário.

### 3.5 Cadeia de fallback de imagem
`ImageProviderManager.generate()`:
1. Se `server_url` é remota (não 127.0.0.1/localhost) → **ComfyUI obrigatório**.
2. Senão, se ComfyUI acessível localmente → tenta ComfyUI.
3. Senão → provider ativo da config (padrão: `pollinations`).
4. Se erro → tenta `pollinations`, depois `huggingface` (se configurado).
5. Tudo falhou → retorna erro.

> ⚠️ **Bug conhecido:** se a URL remota do ComfyUI está **morta**, o manager
> retorna erro **sem fallback** (linha ~101-102 de image_provider_manager.py).
> Ver seção 8 — BUGS.

### 3.6 Pixelização automática (garantia de pixel art real)
`SpriteWorker._pixelate()` (app/ai/workers/sprite_worker.py):
- Reduz para no máx. **1024px** (se a imagem veio maior, ex.: 4096 do upscale x4).
- Redimensiona para grid 48–192 e volta com NEAREST.
- **Quantiza para 256 cores** (MEDIANCUT) preservando alpha.
- Resultado validado: 1024x1024, 254 cores, 100% blocos 8x8 uniformes.

---

## 4. O QUE FOI FEITO NA SESSÃO DE 31/07/2026

### 4.1 Modelo profissional (qualidade de estúdio)
- Selecionado **Pixel Art Diffusion XL Sprite Shaper** (substitui Dreamshaper 8).
- Resolvido download: Civitai bloqueia sem token → **espelhos HuggingFace**.
- Notebook atualizado (célula 4) com as URLs corretas + fallback entre 2 espelhos.
- Workflows ComfyUI validados; placeholders preenchidos corretamente.

### 4.2 Pixel art garantido
- `_apply_transparency` / `_make_transparent` / `_pixelate` criados/corrigidos.
- Prompt negativo anti-pintura + sufixo 8-bit (`positive_suffix`).
- **Pixelização + quantização de cor** aplicadas em TODOS os geradores via worker.

### 4.3 Interface em janela única (UI Redesign)
- Antes: cada clique abria uma janela nova (Toplevel).
- Agora: **janela única com sidebar** (Início/Criar/Galeria/Configurações).
- Telas são `ForgeView` (frames) trocadas no mesmo container via `show_view()`.
- Home com cards de categoria (emoji + hover).
- Estúdio com **presets rápidos** de animação e estilo (inspirado em BrazilGPT
  Spritesheet AI e Spritesheets.ai).
- **Sufixo de estilo por preset** (novo): cada estilo (Anime, Cyberpunk, Chibi...)
  tem seu próprio `positive_suffix`, salvo no config ao clicar no chip.
- Indicador de status ComfyUI na sidebar (verde/offline, atualiza a cada 10s).
- Wrappers legados (`ProductionWindow`, `SpriteViewer`, `SettingsWindow`)
  mantidos para compatibilidade.

### 4.4 Validação ponta-a-ponta REAL (testado de verdade)
- Servidor ComfyUI online via túnel (HTTP 200, ComfyUI 0.29.0, ~12.6 GB RAM).
- Modelo `pixelArtDiffusionXL_spriteShaper.safetensors` confirmado no servidor.
- Geração real: slime, cavaleiro e **goblin vermelho feroz** (pixel art final
  1024x1024, 254 cores, 100% blocos 8x8 uniformes).
- Pipeline completo: PACKAGE STATUS APPROVED + registro no banco.
- Fix: `find_upscale_model()` descobre o upscale disponível no servidor
  (o Colab só tinha x4plus; a config pedia x2plus → 400).
- Fix: parsing do `/object_info` do ComfyUI 0.29 (`["COMBO", {...}]`).
- Fix: config do .exe em APPDATA apontava para túnel morto (corrigido).

### 4.5 Infra de túnel corrigida
- Notebook célula 8 reescrita: mata processos antigos ao re-rodar
  (`stop_old_tunnels()` + `pkill`), usa ssh como primário + cloudflared fallback
  com timeout, e publica a URL no jsonblob.

---

## 5. COMANDOS ÚTEIS

```powershell
# Rodar o app em desenvolvimento
.\venv\Scripts\python.exe run.py

# Recompilar o .exe (depois de mudanças no código)
.\venv\Scripts\python.exe -m PyInstaller ProjectForge.spec --noconfirm

# Validar sintaxe
.\venv\Scripts\python.exe -m py_compile app\main.py app\ui\forge_view.py

# Teste rápido de navegação (sem abrir janela persistente)
.\venv\Scripts\python.exe -c "import os; os.environ['TK_SILENCE_DEPRECATION']='1'; from app.main import ForgeApp; a=ForgeApp(); a.update(); a.destroy(); print('OK')"

# Verificar status do túnel
.\venv\Scripts\python.exe -c "from app.services.comfyui_sync import ComfyUISync; print(ComfyUISync.read_link('https://jsonblob.com/api/jsonBlob/019fb890-6c80-7896-88e3-14ac5bf3ca7c'))"
```

**Link de sincronização (não trocar sem motivo):**
`https://jsonblob.com/api/jsonBlob/019fb890-6c80-7896-88e3-14ac5bf3ca7c`

**Notebook Colab publicado:**
`https://colab.research.google.com/github/Arte3D-Project-Forge/project-forge/blob/main/colab/ComfyUI_Forge_Notebook.ipynb`

---

## 6. ESTRUTURA DAS PASTAS (o que é o quê)

### Em uso (NÃO remover)
| Pasta/Arquivo | Função |
|---|---|
| `app/main.py` | Entry point real (janela única) |
| `app/ui/forge_view.py` | Base das telas + paleta de cores |
| `app/ui/home_view.py` | Tela inicial (cards de categoria) |
| `app/modules/production/ui/production_window.py` | **ProductionView** (estúdio) + wrapper legado |
| `app/ui/sprite_viewer.py` | **GalleryView** (galeria) + wrapper legado |
| `app/ui/settings_window.py` | **SettingsView** (config) + wrapper legado |
| `app/ai/providers/images/*.py` | Providers de imagem (comfyui, pollinations, huggingface, openai, mock) |
| `app/ai/manager/image_provider_manager.py` | Seleção/fallback de providers |
| `app/ai/workers/sprite_worker.py` | Geração de sprites + pixelização |
| `app/production/pipeline/*.py` | Pipeline de produção |
| `app/services/comfyui_sync.py` | Sincronização do túnel |
| `app/services/background_remover.py` | Fundo transparente (rembg) |
| `app/database/asset_database.py`, `app/database/versioning/version_manager.py` | Banco de assets JSON |
| `app/core/config_manager.py` | Leitura/escrita da config |
| `app/quality/asset_quality_manager.py` | Validação do pacote |
| `app/utils/encoding.py` | Normalização UTF-8 |
| `config/`, `config/workflows/` | Configuração e workflows |
| `colab/ComfyUI_Forge_Notebook.ipynb` | Notebook do Colab |
| `docs/imagens/` | Galeria central de imagens de teste |
| `docs/PROJECT_FORGE_BIBLE.md` | Bíblia do projeto (visão) |
| `Godot_projects/Aethervale/` | **Jogo Aetherva (pré-produção)** — docs + projeto Godot inicial |
| `COMO_CONTINUAR.md` | Guia operacional resumido |
| `run.py`, `ProjectForge.spec` | Entry + build |

### Dead code / legado (NÃO usado pelo app atual — pode arquivar ou apagar depois)
| Pasta/Arquivo | Por quê é morto |
|---|---|
| `main.py` (raiz) | Entry antigo; o real é `run.py` → `app/main.py` |
| `app/ui/project_wizard.py`, `project_dashboard.py`, `project_workspace.py`, `workspace.py`, `art_studio.py`, `document_viewer.py`, `production_dashboard.py` | Cadeia de UI antiga (Toplevel), não importada pelo app atual |
| `app/core/module.py`, `module_loader.py`, `module_manager.py`, `module_registry.py`, `project_context.py`, `project_runtime.py`, `workspace_controller.py` | Sistema de módulos antigo (só a cadeia legada usa) |
| `app/modules/documents/*` | Módulo documents legado |
| `app/modules/production/module.py` | ProductionModule legado (ProductionView está vivo no mesmo pacote) |
| `app/ai/providers/{abacus,openai,comfyui,mock}_provider.py` | Stubs antigos (BaseProvider); os reais estão em `providers/images/` |
| `app/ai/provider_manager.py` | Manager antigo (só Mock), mantido pelo pipeline de texto |
| `app/production/production_runner.py`, `production_queue.py`, `production_dashboard.py`, `ui/production_monitor.py` | Pipeline/jobs antigos |
| `app/models/project.py`, `app/services/project_creator.py`, `project_manager.py`, `app/data/projects.json` | Só usados pela cadeia legada |
| `experiments/` | Protótipo Art Studio abandonado (referencia módulos que não existem mais) |
| `templates/`, `resources/`, `scripts/`, `app/config/` | Vazias |

> **Regra (AGENTS.md):** "Never delete existing functionality."
> Por isso os arquivos legados foram **mantidos**, apenas documentados aqui.

---

## 7. BUGS CONHECIDOS (prioridade)

| # | Bug | Onde | Impacto |
|---|---|---|---|
| 1 | Se a URL remota do ComfyUI está morta, **não cai para fallback** (retorna erro) | `app/ai/manager/image_provider_manager.py:101-102` | Usuário vê erro em vez de gerar via Pollinations |
| 2 | Sprites são salvos em `project/sprites/` e **não no pacote** `generated/JOB-.../sprites` (que fica vazio) | `sprite_worker.run()` ignora `package_path` | Pacote incompleto; galeria lê de `project/sprites/` |
| 3 | `PipelineRunner` executa TODOS os workers, ignorando `job.tasks` | `app/production/pipeline/pipeline_runner.py` | Gera lore/tiles/áudio/godot mesmo quando só sprites são pedidos |
| 4 | `_log_workflow_error` usa `self.logger` que nunca é definido | `comfyui_provider.py` | Log silencioso em falha de workflow |
| 5 | Se `providers.image.active="openai"` sem `OPENAI_API_KEY`, o app quebra no init | `image_provider_manager.py:15` | Crash |
| 6 | `hash(prompt)` como seed não é determinístico entre execuções | providers de imagem | Seeds variam |
| 7 | `settings_window._on_url_change` grava o JSON a cada tecla | `settings_window.py` | I/O excessivo |
| 8 | `config/forge_config.json` contém URL de túnel fixa e `sync_url` hardcoded | config + notebook | Se o blob expirar, config velha para todos |
| 9 | `.env` com `OPENAI_API_KEY` real (não versionado, mas sensível) | `config/.env` | Recomenda-se rotacionar |
| 10 | Seletor "Animação" no estúdio só aparece no detalhe; worker gera só `["idle"]` | `production_window.py` / `sprite_worker` | Animação selecionada não vira frames |
| 11 | `app/core/module_loader.py` tem **dois `__init__`** (o 1º é sobrescrito) | `module_loader.py` | Bug latente (arquivo morto) |
| 12 | `production_queue.clear_completed()` conta mas não apaga | `production_queue.py` | Funcionalidade errada (arquivo morto) |
| 13 | `huggingface_provider` usa modelo hardcoded, ignora o da config | `huggingface_provider.py` | Config sem efeito |

---

## 8. PRÓXIMOS PASSOS SUGERIDOS (priorizados)

1. **Fix Bug #1** — fallback quando o túnel ComfyUI está morto (maior impacto UX).
2. **Fix Bug #2** — sprites dentro do pacote do job (ou galeria lendo do pacote).
3. **Fix Bug #3** — respeitar `job.tasks` no PipelineRunner.
4. **Fix Bug #10** — animação selecionada no estúdio virar frames reais.
5. **Limpeza opcional** — mover dead code para `legacy/` (depois de confiar no app novo).
6. **GPU Colab** — limite de uso do free; considerar instruções de conta alternativa/Pro no README.

---

## 9. NOTA DE LIMITE DE GPU (Colab free — 31/07/2026)

- O usuário esgotou a cota gratuita de GPU do Colab (erro "não é possível conectar
  a uma GPU devido ao limite de uso").
- Isso NÃO é bug do Forge. A cota reseta em algumas horas, ou usar outra conta Google,
  ou Colab Pro.
- Enquanto offline, o Forge cai para Pollinations (qualidade boa, sem o modelo SDXL).

---

## 10. PADRÕES E CONVENÇÕES (resumo do AGENTS.md)

- **Arquitetura limpa**: `app/core` (negócio, sem UI), `app/services` (integrações),
  `app/ui` (visual), `app/models` (DTOs), `app/utils`, `app/config`.
- **Documentação first**: toda feature nova atualiza README, ROADMAP, CHANGELOG,
  ARCHITECTURE (se necessário) e este documento.
- **Commits**: `feat:`, `fix:`, `refactor:`, `docs:`, `test:`.
- **Nunca deletar funcionalidade existente**; nunca gerar código temporário.
- **Testes antes de release**; cada sprint entrega versão funcional.
- Sem magic numbers; configuração separada do código (em `config/forge_config.json`).
