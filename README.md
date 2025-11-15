# Kairós: Seu Assistente de Produtividade com IA

![Status do Pipeline](https-placeholder-para-o-badge) 

**Status do Projeto: Em Desenvolvimento Ativo**

Projeto Integrador do curso de Análise e Desenvolvimento de Sistemas, focado em aplicar os pilares de **Estrutura de Dados**, **Inteligência Artificial** e **Segurança da Informação** em uma aplicação funcional, construída sob uma esteira de **CI/CD (DevOps)**.

---

## 📖 Índice

- [1. Sobre o Projeto](#1-sobre-o-projeto)
- [2. Pilares e Requisitos do Projeto](#2-pilares-e-requisitos-do-projeto)
  - [🧠 Inteligência Artificial](#-inteligência-artificial)
  - [🧱 Estrutura de Dados](#-estrutura-de-dados)
  - [🛡️ Segurança da Informação](#️-segurança-da-informação)
  - [⚙️ DevOps e CI/CD](#️-devops-e-cicd)
- [3. Arquitetura e Tecnologias](#3-arquitetura-e-tecnologias)
- [4. Como Executar o Projeto](#4-como-executar-o-projeto)
- [5. Equipe](#5-equipe)

---

## 1. Sobre o Projeto

**Kairós** (do grego: *καιρός*) representa o "momento certo" ou "tempo oportuno". Este projeto é um assistente de produtividade que vai além de uma simples lista de tarefas.

Enquanto a maioria das ferramentas de produtividade é passiva, o **Kairós** atua como um **assistente proativo**. Utilizando Inteligência Artificial, o sistema analisa seus compromissos e tarefas para sugerir o **plano diário mais eficiente**, ajudando o usuário a encontrar o "momento certo" para cada atividade, maximizando o foco e otimizando o tempo.

## 2. Pilares e Requisitos do Projeto

O desenvolvimento do Kairós é guiado pelos 4 pilares definidos no Documento Norteador da disciplina.

### 🧠 Inteligência Artificial
O "cérebro" do Kairós. O objetivo é criar um modelo de classificação (provavelmente usando **Scikit-learn**) que analise as tarefas do usuário (considerando complexidade, prazo, energia) para priorizá-las e ordená-las de forma inteligente, entregando a agenda otimizada do dia.

### 🧱 Estrutura de Dados
Para cumprir o requisito de uma estrutura de dados não-trivial, o núcleo do sistema (o gerenciamento de tarefas) será construído sobre uma **Tabela de Hash** (implementada através de um Dicionário Python). Isso garante a performance de busca, inserção e deleção de tarefas em tempo constante, O(1).

### 🛡️ Segurança da Informação
A segurança dos dados do usuário é um pilar não-negociável. A aplicação é construída seguindo práticas de "Código Seguro" baseadas no OWASP Top 10:
-   **Validação de Dados de Entrada:** Utilização de schemas **Pydantic** para validar rigorosamente todos os dados que chegam na API.
-   **Armazenamento Seguro de Senhas:** Nenhuma senha é armazenada em texto plano. Usamos **hashing com salt** através da biblioteca `passlib[bcrypt]`.
-   **Gerenciamento Seguro de Sessões:** Implementação de autenticação via **Tokens JWT** (`python-jose`) para proteger os endpoints da aplicação.

### ⚙️ DevOps e CI/CD
A "fábrica" do Kairós. Utilizamos **GitHub Actions** para automatizar nosso ciclo de desenvolvimento. O pipeline está configurado em `.github/workflows/main.yml` para executar, no mínimo, dois estágios a cada *push*:
1.  **`build`**: Instala as dependências e garante que o ambiente está correto.
2.  **`test`**: Executa a suíte de testes unitários (escritos com **Pytest**) para garantir que novas mudanças não quebraram a funcionalidade existente.

## 3. Arquitetura e Tecnologias

A aplicação segue uma **Arquitetura Limpa (Clean Architecture)** em camadas (API, Serviços, Modelos, Núcleo) para garantir "Código Limpo" e separação de preocupações.

**Stack Tecnológica Oficial:**
-   **Linguagem:** Python 3.9+
-   **Framework Backend:** FastAPI
-   **Servidor:** Uvicorn
-   **Segurança (Validação):** Pydantic
-   **Segurança (Hashing):** Passlib (com Bcrypt)
-   **Segurança (Tokens):** Python-JOSE (para JWT)
-   **Testes:** Pytest
-   **Inteligência Artificial:** Scikit-learn
-   **Plataforma de DevOps:** GitHub Actions

## 4. Como Executar o Projeto

O projeto é uma API backend. Para executá-lo localmente, siga os passos:

**Pré-requisitos:**
-   Python 3.9 ou superior
-   Git

```bash
# 1. Clone o repositório
git clone [https://github.com/ScarletYkaro10/kairos.git](https://github.com/ScarletYkaro10/kairos.git)

# 2. Navegue para a pasta do projeto
cd kairos

# 3. (Recomendado) Crie e ative um ambiente virtual
python -m venv venv
source venv/bin/activate  # No Windows: .\venv\Scripts\activate

# 4. Instale as dependências
pip install -r requirements.txt

# 5. Inicie o servidor de desenvolvimento
# O --reload faz o servidor reiniciar automaticamente a cada mudança no código
uvicorn src.main:app --reload
