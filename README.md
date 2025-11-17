<div align="center">

# Kairos

_"O momento certo" para entregar uma base solida antes de adicionar IA._

</div>

## Visao Geral

Kairos e o sistema de gestao de tarefas e otimizacao de agenda que estamos construindo em duas etapas:

- **MVP de Qualificacao (50%)** - infraestrutura completa (Seguranca, CRUD, CI/CD) e endpoint `/optimize-schedule` com logica mock.
- **MVP Final (100%)** - troca do mock por um modelo real (Scikit learn), mantendo a base pronta.

## Status do MVP 50

- Seguranca: autenticacao JWT implementada (`/auth/register`, `/auth/login`) e endpoints de tarefas protegidos via header `Authorization: Bearer <token>`.
- CRUD de Tarefas: criacao e listagem com validacoes, pronto para trocar para banco real.
- DevOps: pipeline GitHub Actions (`build` + `test-tasks`) garantindo testes verdes.
- IA Mock: `src/services/ia_service.py` reordena tarefas por prioridade e prazo, pronta para ser substituida pelo modelo real.
- Proximo 50: implementar treinamento e carregamento do modelo e substituir a logica mock no endpoint.

## Estrutura

- `src/models/schemas.py` - Schemas Pydantic de usuarios, tokens e tarefas.
- `src/services/task_service.py` - CRUD em memoria e ponto unico para evoluir para DB.
- `src/services/auth_service.py` - Servico de autenticacao com JWT e hash de senhas.
- `src/services/ia_service.py` - Regra deterministica (mock) para ordenacao.
- `src/api/task_router.py` - Rotas `/tasks` e `/optimize-schedule`.
- `src/api/auth_router.py` - Rotas `/auth/register` e `/auth/login`.
- `src/core/security.py` - Funcoes de hash de senha e JWT.
- `src/main.py` - Factory do FastAPI e registro das rotas.

## Como Rodar Localmente

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
uvicorn src.main:app --reload
```

## Testes e Pipeline

```bash
pytest tests/test_tasks.py
```

O workflow `.github/workflows/main.yml` executa:

1. `build`: instala dependencias.
2. `test-tasks`: roda `pytest tests/test_tasks.py`.

## Roadmap pos Qualificacao

1. Integrar autenticacao completa com os endpoints de tarefas (usar JWT real ao inves de UUID mock).
2. Treinar e publicar o modelo de IA (Scikit learn) usado pelo `/optimize-schedule`.
3. Expandir CRUD (projetos, tarefas compartilhadas) e observabilidade.

Vamos continuar empilhando o "arroz com feijao" ate a fundacao ficar solida.
