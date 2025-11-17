<div align="center">

# Kairos

[![CI](https://github.com/USERNAME/REPO/actions/workflows/main.yml/badge.svg)](https://github.com/USERNAME/REPO/actions/workflows/main.yml)

_"O momento certo" para entregar uma base solida antes de adicionar IA._

</div>

## Visao Geral

Kairos e o sistema de gestao de tarefas e otimizacao de agenda que estamos construindo em duas etapas:

- **MVP de Qualificacao (50%)** - infraestrutura completa (Seguranca, CRUD, CI/CD) e endpoint `/optimize-schedule` com logica mock.
- **MVP Final (100%)** - troca do mock por um modelo real (Scikit learn), mantendo a base pronta.

## Status do MVP 50

- Seguranca: endpoints protegidos via header `Authorization: Bearer <token>` (substituir por JWT real do modulo de seguranca).
- CRUD de Tarefas: criacao e listagem com validacoes, pronto para trocar para banco real.
- DevOps: pipeline GitHub Actions (`build` + `test-tasks`) garantindo testes verdes.
- IA Mock: `src/services/ia_service.py` reordena tarefas por prioridade e prazo, pronta para ser substituida pelo modelo real.
- Proximo 50: implementar treinamento e carregamento do modelo e substituir a logica mock no endpoint.

## Estrutura

- `src/models/schemas.py` - Schemas Pydantic de tarefas.
- `src/services/task_service.py` - CRUD em memoria e ponto unico para evoluir para DB.
- `src/services/ia_service.py` - Regra deterministica (mock) para ordenacao.
- `src/api/task_router.py` - Rotas `/tasks` e `/optimize-schedule`.
- `src/main.py` - Factory do FastAPI e registro das rotas.

## Como Rodar Localmente

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
uvicorn src.main:app --reload
```

Requests precisam enviar o header `Authorization: Bearer <uuid>` ate que o modulo de autenticacao esteja integrado.

## Testes e Pipeline

```bash
pytest tests/test_tasks.py
```

O workflow `.github/workflows/main.yml` executa:

1. `build`: instala dependencias.
2. `test-tasks`: roda `pytest tests/test_tasks.py`.

Atualize o badge com o nome real do repositorio quando o GitHub estiver configurado.

## Roadmap pos Qualificacao

1. Integrar autenticacao completa (registro, login, JWT) com os endpoints existentes.
2. Treinar e publicar o modelo de IA (Scikit learn) usado pelo `/optimize-schedule`.
3. Expandir CRUD (projetos, tarefas compartilhadas) e observabilidade.

Vamos continuar empilhando o "arroz com feijao" ate a fundacao ficar solida.
