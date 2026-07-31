# PROJECT FORGE ARCHITECTURE


## Arquitetura principal


PROJECT FORGE CORE


        CORE SYSTEM

             |

--------------------------------

PROJECT MANAGER

DOCUMENT SYSTEM

PRODUCTION SYSTEM

ART STUDIO

AUDIO STUDIO

NARRATIVE STUDIO

AI AGENTS

BUILD SYSTEM

PLUGIN SYSTEM

ENGINE CONNECTORS


--------------------------------


## Filosofia

Cada módulo deve funcionar isoladamente.

Nunca criar dependências desnecessárias.


---

# Core

Responsável:

- inicialização
- configuração
- registro de módulos
- comunicação interna


---

# Module System

Base:

ForgeModule


Cada módulo possui:

- name
- version
- lifecycle
- services


---

# Document System

Responsável:

- Game Design Document
- Lore
- Roadmap
- Documentation


Formato:

Markdown


---

# Production System

Responsável:

- tarefas
- jobs
- pipeline
- status


Objeto principal:

ProductionJob


---

# AI Layer

Responsável:

Integração com:

- OpenAI
- modelos locais
- ComfyUI
- futuros providers