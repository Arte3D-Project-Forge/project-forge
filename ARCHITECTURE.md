# Arquitetura do Project Forge

> Documento técnico. Para o estado atual completo (bugs, próximos passos),
> veja `docs/ESTADO_ATUAL.md`. Para a visão do projeto, veja
> `docs/PROJECT_FORGE_BIBLE.md`.

## Visão geral

Aplicação desktop (Python 3.13 + CustomTkinter) de **janela única** que
orquestra a geração de assets de jogo via IA, com pipeline de produção
completa e banco de assets em JSON.

```
┌────────────────────────────────────────────────────────────┐
│                        ForgeApp (CTk)                      │
│  ┌──────────────┐  ┌────────────────────────────────────┐  │
│  │ Sidebar      │  │ Content (troca de telas)           │  │
│  │ Início       │  │  HomeView | ProductionView |       │  │
│  │ Criar Asset  │  │  GalleryView | SettingsView        │  │
│  │ Galeria      │  │                                    │  │
│  │ Configurações│  │                                    │  │
│  │ ● ComfyUI    │  │                                    │  │
│  └──────────────┘  └────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────┘
```

## Camadas

### 1. UI (`app/ui/`, `app/main.py`)
- `ForgeApp` — janela única com sidebar e `show_view()` que troca as telas.
- `ForgeView` — base das telas (paleta de cores + navegação).
- Telas: `HomeView`, `ProductionView`, `GalleryView`, `SettingsView`.

### 2. Produção (`app/production/`)
- `ProductionJob` — representa um job (projeto + pedido + tasks).
- `PipelineRunner` — orquestra: Package → Manifest → Prompts → README →
  workers (sprites, lore, tiles, animação, áudio, godot) → quality check → banco.

### 3. IA (`app/ai/`)
- `ImageProviderManager` — seleção de provider com fallback.
- `providers/images/` — `ComfyUIProvider` (principal), `PollinationsProvider`,
  `HuggingFaceProvider`, `OpenAIImageProvider`, `MockImageProvider`.
- `workers/` — `SpriteWorker` (gera imagem + transparência + pixelização),
  além dos workers de lore/tiles/animação/áudio/godot (metadata/estrutura).

### 4. Serviços (`app/services/`)
- `ComfyUISync` / `ComfyUISyncPoller` — lê a URL do túnel publicada no
  jsonblob pelo Colab e atualiza a config sozinho.
- `BackgroundRemover` — remoção de fundo (rembg) para PNG transparente.

### 5. Dados (`app/database/`, `database/`)
- `AssetDatabase` / `VersionManager` — assets, registro, versões, changelog em JSON.
- Config: `config/forge_config.json` (ConfigManager com lock de escrita).

## Fluxo principal

```
Usuário digita prompt → ProductionView.create_job()
  → ProductionJob.save() → PipelineRunner.run()
    → PromptBuilder (docs) → SpriteWorker
      → ImageProviderManager.generate()
        → ComfyUIProvider (via túnel) [ou Pollinations/HF fallback]
        → remove fundo + pixelização/quantização
    → AssetQualityManager.validate() → AssetDatabase.register_asset()
  → GalleryView mostra o sprite em project/sprites/<asset>/
```

## Geração via ComfyUI (Colab)

O Colab roda ComfyUI com o modelo SDXL **Sprite Shaper** (1024x1024). O app
envia um workflow API (`config/workflows/*.json`) com placeholders que o
`ComfyUIProvider.build_workflow()` preenche. O túnel HTTPS publica a URL num
blob jsonblob; o `ComfyUISyncPoller` (8s) sincroniza no app.

## Convenções

- `app/core` = negócio (sem UI). `app/services` = integrações.
- `app/ui` = só visual. `app/models` = DTOs. `app/config` = configuração.
- Configuração sempre em `config/forge_config.json`, nunca hardcoded em código.
- Nenhum `__init__.py` no pacote (namespace packages) — manter consistência.
