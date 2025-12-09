# ⏳ Kairós

> **Seu Assistente de Produtividade Inteligente.**

O **Kairós** é um sistema de gestão de tarefas projetado para eliminar a paralisia de decisão. Diferente de *to-do lists* comuns, ele utiliza um modelo de **Inteligência Artificial (Machine Learning)** para analisar suas tarefas e definir automaticamente o que deve ser feito primeiro, baseando-se em critérios de urgência, categoria e dificuldade.

---

## 🚀 Status do Projeto
✅ **MVP 100% Concluído**
- **Fase 1 (Infraestrutura):** Autenticação, CRUD e CI/CD.
- **Fase 2 (Inteligência):** Integração com PostgreSQL, Frontend interativo e Modelo de IA (Random Forest) treinado e ativo.

---

## 🛠️ Tecnologias e Arquitetura

O projeto foi construído seguindo uma arquitetura de microsserviços containerizados, garantindo isolamento e facilidade de deploy.

* **Backend:** Python 3.11 + **FastAPI** (Alta performance e tipagem forte).
* **Frontend:** **Streamlit** (Interface reativa e Data-Driven).
* **Banco de Dados:** **PostgreSQL 15** (Persistência robusta de dados).
* **Inteligência Artificial:** **Scikit-Learn** (Algoritmo Random Forest Classifier).
* **Infraestrutura:** **Docker** & **Docker Compose** (Orquestração dos containers).
* **Segurança:** Autenticação via **JWT** (JSON Web Tokens) e hash de senhas com **Bcrypt**.

---

## 🧠 Como a IA Funciona?

O diferencial do Kairós é o endpoint `/optimize-schedule`. Ele não apenas ordena por data, mas "entende" o contexto da tarefa:

1.  **Entrada:** A IA recebe o prazo (dias restantes), duração estimada, dificuldade (1-5) e categoria (ex: Saúde, Trabalho, Lazer).
2.  **Processamento:** Um modelo treinado (`kairos_model.pkl`) analisa esses fatores.
    * *Exemplo:* Uma tarefa de "Saúde" para daqui a 3 dias tem peso maior que "Lazer" para hoje.
3.  **Saída:** A tarefa é classificada em **Alta 🔥**, **Média ⚡** ou **Baixa 🌱** prioridade e a lista é reordenada automaticamente.

---

## 🐳 Como Rodar (Recomendado via Docker)

A maneira mais simples de rodar o projeto completo (Front, Back e Banco) é utilizando o Docker.

### Pré-requisitos
* Docker Desktop instalado e rodando.

### Passo a Passo

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/seu-usuario/kairos.git](https://github.com/seu-usuario/kairos.git)
    cd kairos
    ```

2.  **Suba os containers:**
    ```bash
    docker-compose up --build
    ```
    *Aguarde alguns instantes. O Docker irá baixar as imagens, configurar o PostgreSQL e treinar o modelo de IA na inicialização.*

3.  **Acesse o Sistema:**
    * 🖥️ **Frontend (Aplicação):** [http://localhost:8501](http://localhost:8501)
    * 📄 **Backend (Documentação API):** [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📂 Estrutura do Projeto

A organização segue os padrões de *Clean Architecture* simplificada para microsserviços.

```text
kairos/
├── frontend/               # Aplicação Streamlit
│   ├── app.py              # Código da interface e conexão com API
│   └── Dockerfile          # Configuração da imagem do Front
├── src/                    # Código Fonte do Backend
│   ├── api/                # Rotas (Endpoints) da API
│   ├── core/               # Configurações (Banco, Segurança)
│   ├── ia/                 # Módulo de Inteligência Artificial
│   │   ├── dataset_generator.py  # Gera dados sintéticos para treino
│   │   ├── train_model.py        # Treina e salva o modelo .pkl
│   │   └── tasks_dataset.csv     # Base de conhecimento
│   ├── models/             # Modelos do Banco (SQLAlchemy) e Schemas (Pydantic)
│   ├── services/           # Regras de Negócio (Auth, Task, IA)
│   └── main.py             # Entrypoint da API
├── tests/                  # Testes Automatizados (Pytest)
├── docker-compose.yml      # Orquestração dos serviços
└── requirements.txt        # Dependências do Python