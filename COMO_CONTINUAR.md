# Project Forge — Como Continuar

## Onde me encontrar amanhã

1. Abra o **PowerShell**
2. Digite o comando abaixo e pressione ENTER:

```
opencode
```

3. Quando a conversa começar, pergunte: **"Continue de onde paramos"**
4. Se eu não lembrar de algo, é só me mostrar este arquivo

---

## PONTO ATUAL (31/07/2026 — Final de sessão)

**Executável atualizado:**
```
C:\Users\Fábio\Projects\project-forge\dist\ProjectForge.exe
```
(125MB, build 31/07 com: menu de criação, workflow profissional, fundo transparente + pixelização automática para TODOS os geradores, sincronização automática do túnel)

**MODELO PROFISSIONAL (31/07):** `Pixel Art Diffusion XL - Sprite Shaper` (SDXL, do Civitai)
- Download direto SEM token: `https://civitai.com/api/download/models/364043` (6.6GB)
- Resolução base 1024x1024 (SDXL nativo) → upscale RealESRGAN_x2plus → 2048x2048
- Pixelização automática no worker garante pixels quadrados nítidos (anti-"pintura a pincel")
- Fallback offline continua Pollinations imagegen3 (agora com pixelização tb)

**Arquitetura final de geração (31/07):**
1. **Qualidade máxima (padrão):** Colab + ComfyUI. O notebook tem célula de "túnel automático" que mantém o túnel vivo e publica a URL em um link jsonblob.com PRE-CONFIGURADO (hardcoded no app e no notebook — zero cola-cola). O Forge vigia o link a cada 8s e se conecta sozinho.
2. **Fallback offline:** Pollinations (imagegen3) quando o Colab não está rodando — o app nunca trava sem internet.

**Link de sincronização compartilhado:** `https://jsonblob.com/api/jsonBlob/019fb890-6c80-7896-88e3-14ac5bf3ca7c`
- Notebook celula 8 tem `SYNC_URL` com este link
- App config `comfyui.sync_url` tem o mesmo link
- ATENÇÃO: para distribuição em produção, cada usuário deve criar o SEU link (botão "Criar link" nas Configurações) — link compartilhado pode colidir entre usuários.

**Bugs importantes corrigidos nesta sessão:**
- Workflow do ComfyUI tinha chave `description` no topo → ComfyUI retornava 500. Corrigido com `workflow.pop("description")`.
- URL do túnel não era salva sem clicar em Testar → agora salva automaticamente ao digitar/colar.
- Manager caía no mock (quadrado colorido) silenciosamente → mock removido do fallback automático; erros honestos mostrados.
- Fundo transparente (rembg) só rodava no caminho ComfyUI → agora roda no worker para todos os geradores.

**O app foi reformulado como um app de menu para o cliente final.**

```
PROJECT FORGE (tela inicial)
├── O QUE VOCÊ QUER CRIAR?
│   ├── Personagem | Inimigo (Mob) | Pet | Item | Mapa (Tiles) | Dungeon | Efeito
├── VER SPRITES GERADOS | Configurações | Sair
└── Nota: "Geração automática, sem configuração necessária"
```

Fluxo do cliente: abrir app → escolher o que criar → descrever → gerar.
Sem console, sem Colab, sem T4, sem editar arquivos, sem saber programar.

**ComfyUI/Colab ficou escondido em "Configurações"** (só para quem quiser). O fluxo principal não mostra nada técnico.

**Notebook publicado no GitHub:** `Arte3D-Project-Forge/project-forge`
URL: `https://colab.research.google.com/github/Arte3D-Project-Forge/project-forge/blob/main/colab/ComfyUI_Forge_Notebook.ipynb`

---

## O que foi feito nesta sessão

### 1. App virou um menu de criação (cliente final)
- `app/main.py` reescrito: tela inicial com categorias (Personagem, Mob, Pet, Item, Mapa, Dungeon, Efeito)
- Cada botão abre o Production Studio já com a categoria selecionada
- Projeto padrão "Meu Jogo" criado automaticamente em `%APPDATA%\ProjectForge\MeuJogo` (no .exe) ou `MeuJogo/` (dev)
- Indicador de status do ComfyUI na tela inicial

### 2. Ativação guiada do ComfyUI grátis (sem interação técnica)
- Botão **⚡ ATIVAR GPU GRÁTIS** abre o notebook no Colab direto no navegador
- **Detecção automática da URL via área de transferência**: quando o usuário copia a URL do túnel (Ctrl+C), o Forge detecta, salva na config e conecta sozinho
- Notebook atualizado: instruções apontam para o app, fallback de download do modelo (CivitAI → HuggingFace)

### 3. Workflow de qualidade pronto para jogo
- `config/workflows/comfyui_sprite_workflow.json` — workflow API-format com placeholders
- Config `comfyui`: steps 28, cfg 7, sampler dpmpp_2m, scheduler karras
- Prompt positivo/negativo otimizados para sprite de jogo (evita distorção, fundo sujo, multi-subject)
- Resolução da tela agora é respeitada (512/1024) → salva em `generation.default_resolution`

### 4. Sprites prontos para o jogo (fundo transparente)
- `app/services/background_remover.py` — remove fundo via `rembg` (u2net)
- ComfyUI provider aplica transparência automaticamente → PNG RGBA
- `requirements.txt` atualizado: `rembg[cpu]`, `httpx`

### 5. Configuração persistente no .exe
- `ConfigManager._resolve_frozen_path`: no .exe, config é copiada para `%APPDATA%\ProjectForge` na 1ª execução e salva lá
- `ConfigManager.set()` criado (salva alterações no JSON)

### 6. Auto-detecção de ComfyUI
- `ImageProviderManager.comfyui_available()`: testa o servidor configurado (timeout 3s)
- Se ComfyUI acessível → usa ele. Senão → Pollinations → HuggingFace → Mock

---

## O que falta fazer (próximos passos)

### Prioridade Alta
1. **Testar o fluxo completo no Colab** — o túnel via SSH (localhost.run) foi corrigido; validar geração de sprite de verdade via GPU
2. **Testar o .exe novo** — abrir, conectar ComfyUI, gerar (o .exe foi recompilado em 31/07)

### Prioridade Média
4. **Animações (múltiplos frames)** — gerar idle_001, idle_002... para animação
5. **Tilesets/dungeons** — gerar mapas completos
6. **SpriteViewer melhorado** — zoom, categoria, fundo xadrez (ver transparência)
7. **Estrutura de saída pronta para engine** — `assets/characters/hero/idle/hero_idle_001.png`

### Prioridade Baixa
8. **Testes unitários** — rodar todos e corrigir falhas
9. **Documentação** — README, ROADMAP, CHANGELOG
10. **Instalador** — distribuir como .msi ou .zip (com o notebook já incluído)

---

## Comandos úteis

### Rodar o app (modo desenvolvimento)
```powershell
cd C:\Users\Fábio\Projects\project-forge
.\venv\Scripts\python.exe run.py
```

### Gerar .exe
```powershell
cd C:\Users\Fábio\Projects\project-forge
Get-Process ProjectForge -ErrorAction SilentlyContinue | Stop-Process -Force
Remove-Item -Recurse -Force build, dist -ErrorAction SilentlyContinue
.\venv\Scripts\pyinstaller --onefile --name "ProjectForge" --add-data "config;config" --add-data "app;app" --hidden-import "PIL._tkinter_finder" --hidden-import "customtkinter" --hidden-import "openai" --hidden-import "rembg" --hidden-import "onnxruntime" --collect-submodules "rembg" --collect-data "rembg" run.py
```

> **Importante:** no `.exe`, a configuração é copiada para `%APPDATA%\ProjectForge` na primeira execução. Alterações feitas no app (URL do ComfyUI, resolução) ficam salvas lá, não dentro do executável.

### Testar provider direto
```powershell
cd C:\Users\Fábio\Projects\project-forge
.\venv\Scripts\python.exe -c "
from app.ai.manager.image_provider_manager import ImageProviderManager
mgr = ImageProviderManager()
r = mgr.generate('fire dragon pixel art', 'test', '.')
print(r)
"
```

---

## Estrutura atual (resumo)

```
project-forge/
├── app/
│   ├── main.py                                   # MENU DE CRIAÇÃO (cliente final)
│   ├── ai/
│   │   ├── manager/image_provider_manager.py   # ComfyUI (se vivo) + fallback pollinations
│   │   ├── providers/images/                   # comfyui, pollinations, huggingface, mock, openai
│   │   └── workers/                            # sprite, lore, tile, animation, audio, godot
│   ├── core/config_manager.py                  # config persistente (APPDATA no .exe)
│   ├── modules/production/ui/production_window.py  # Studio de criação
│   ├── services/
│   │   ├── background_remover.py               # fundo transparente (rembg)
│   │   └── comfyui_sync.py                     # vigia o link e atualiza URL sozinho
│   ├── production/                             # job, pipeline, builders
│   └── ui/                                     # wizard, workspace, sprite viewer, settings
├── config/
│   ├── forge_config.json                       # comfyui (workflow, steps, prompts, sync_url)
│   └── workflows/
│       ├── comfyui_sprite_workflow.json        # workflow básico
│       └── comfyui_sprite_upscale_workflow.json# workflow + upscale RealESRGAN 4x
├── colab/ComfyUI_Forge_Notebook.ipynb          # PUBLICADO no GitHub (túnel automático)
├── dist/ProjectForge.exe                       # executável (ATUALIZADO 31/07)
└── COMO_CONTINUAR.md                           # este arquivo
```

---

## Importante

- O `.exe` em `dist/` está **ATUALIZADO** (31/07). Regerar sempre que o código mudar:
  `.\venv\Scripts\pyinstaller --onefile --name "ProjectForge" --add-data "config;config" --add-data "app;app" --hidden-import "PIL._tkinter_finder" --hidden-import "customtkinter" --hidden-import "openai" --hidden-import "rembg" --hidden-import "onnxruntime" --collect-submodules "rembg" --collect-data "rembg" run.py`
- **Qualidade máxima grátis:** ComfyUI via Colab (notebook publicado). O túnel se mantém vivo sozinho e o Forge descobre a URL sozinho (link compartilhado pre-configurado).
- **Fallback offline:** Pollinations imagegen3 (funciona sem nada, qualidade média).
- Para distribuição real, cada usuário cria seu link de sincronização (Configurações > Criar link).
- O usuário quer um app simples: abrir → digitar prompt → ver sprites. Foco nisso.

---

## Amanhã

Basta digitar no PowerShell:
```
opencode
```

E dizer: **"Continue de onde paramos no Project Forge"**
