# Roadmap do Project Forge

> Mantido conforme o AGENTS.md: toda feature nova atualiza este documento.
> Detalhes operacionais e estado atual: `docs/ESTADO_ATUAL.md`.

## Concluído ✅

### v0.1.0 — Fundação da geração profissional (31/07/2026)
- Interface em janela única com sidebar e navegação por telas.
- Modelo profissional **Pixel Art Diffusion XL — Sprite Shaper** (SDXL 1024)
  no ComfyUI/Colab com túnel automático e sincronização via jsonblob.
- Pixel art garantido: pixelização + quantização (≤256 cores) em todos os geradores.
- Presets rápidos de animação/estilo com sufixo de prompt por estilo.
- Validação ponta-a-ponta real (slime, cavaleiro, goblin — 1024x1024, 100% blocos 8x8).

## Em andamento 🔄

- [ ] Fallback automático quando o túnel ComfyUI remoto está morto
      (`image_provider_manager` — hoje retorna erro em vez de cair para Pollinations).
- [ ] Sprites dentro do pacote do job (`generated/JOB-.../sprites` fica vazio hoje).
- [ ] Respeitar `job.tasks` no `PipelineRunner` (hoje gera todos os workers sempre).
- [ ] Animação selecionada no estúdio virar frames reais (hoje só `idle`).

## Próximas versões 🎯

### v0.2.0 — Animações e pacotes completos
- Geração de animações reais (walk/attack/hurt/death) com frames consistentes.
- Spritesheet com grid e metadata para Godot.
- Sprites dentro do pacote do job (galeria lê do pacote).

### v0.3.0 — Pipeline inteligente
- Respeitar `job.tasks` (gerar só o que foi pedido).
- GPT real para lore/prompts (provider de texto ativo hoje é mock).
- Remover/gaveta de dead code legado (wizard, módulos, dashboards antigos).

### v1.0 — Release
- Build estável, instalador, onboarding do usuário final ("baixar → executar → ver pronto").
- Limite de GPU do Colab documentado no app (cota free).

### v2.0+ — Multi-mídia
- Áudio procedural, tilesets, spritesheets animadas, exportação para múltiplas engines.

## Ideias (backlog)
- Perfil de estilo salvo por projeto.
- Galeria com preview de animação (fps) e zoom.
- Histórico de jobs e re-geração com mesma seed.
- Modo "explorar" para o usuário final sem configuração.
