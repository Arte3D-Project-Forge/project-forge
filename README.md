# Project Forge

**AI Game Development Operating System** — uma plataforma desktop que orquestra
toda a pipeline de produção de jogos: do prompt ao asset pronto para a engine,
com geração de **sprites de pixel art profissional**.

> 📖 **LEIA `docs/ESTADO_ATUAL.md` primeiro** — é o documento master com o
> estado completo do projeto, o que funciona, bugs conhecidos e próximos passos.

---

## ✨ O que faz

- **Janela única** com sidebar (Início / Criar Asset / Galeria / Configurações).
- **Sprites de pixel art profissional** com modelo SDXL especializado
  (*Pixel Art Diffusion XL — Sprite Shaper*) rodando no ComfyUI (Google Colab),
  com túnel automático e fallback para geradores gratuitos.
- **Pixelização garantida**: toda saída vira pixel art real (≤256 cores,
  blocos uniformes), com fundo transparente.
- **Pipeline de produção completa**: package, prompts, lore, sprites, tiles,
  animações, áudio, estrutura Godot, quality check e banco de assets.
- **Presets rápidos**: animação (Idle, Walk, Attack...) e estilo (Pixel Retro,
  Anime, Cyberpunk, Chibi...) com sufixo de prompt por estilo.

## 🚀 Como rodar

```powershell
# Desenvolvimento
.\venv\Scripts\python.exe run.py

# Recompilar o .exe
.\venv\Scripts\python.exe -m PyInstaller ProjectForge.spec --noconfirm
```

O executável fica em `dist\ProjectForge.exe`.

## 🎓 Como gerar com qualidade máxima (grátis)

1. Abra o notebook: `colab/ComfyUI_Forge_Notebook.ipynb`
   (ou o link publicado no README do próprio notebook).
2. Rode as células em ordem (GPU T4). A célula 4 baixa o modelo profissional,
   a 8 sobe o túnel automático.
3. O Forge **descobre a URL sozinho** (a cada 8s) e mostra "ComfyUI: conectado".

> **Nota de limite:** o Colab gratuito tem cota de GPU. Ao esgotar, espere
> algumas horas, use outra conta Google ou Colab Pro. Sem o ComfyUI, o Forge
> usa fallback (Pollinations) automaticamente.

## 🧱 Estrutura (resumo)

```
app/main.py                      Entry point (janela única)
app/ui/                          Telas (Home, Studio, Gallery, Settings)
app/ai/providers/images/         Providers de imagem (ComfyUI, Pollinations, HF)
app/ai/workers/                  Workers de geração (sprite, lore, tiles, ...)
app/production/pipeline/         Pipeline de produção
app/services/comfyui_sync.py     Sincronização do túnel Colab
config/forge_config.json         Toda a configuração
config/workflows/                Workflows ComfyUI (JSON com placeholders)
colab/                           Notebook do Colab
docs/                            Documentação (master em ESTADO_ATUAL.md)
```

## 📚 Documentação

| Documento | Conteúdo |
|---|---|
| `docs/ESTADO_ATUAL.md` | **Master**: estado, arquitetura viva, bugs, próximos passos |
| `docs/PROJECT_FORGE_BIBLE.md` | Visão e filosofia do projeto |
| `ARCHITECTURE.md` | Arquitetura técnica |
| `ROADMAP.md` | Roadmap |
| `CHANGELOG.md` | Histórico de mudanças |
| `AGENTS.md` | Guia de engenharia para agentes de IA |
