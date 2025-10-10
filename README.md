# OptimaTask: Assistente Pessoal de Produtividade com IA

![Project Banner](https://i.imgur.com/your-banner-image.png) **Status do Projeto: Em fase de Concepção**

Projeto integrador desenvolvido para o módulo **IA e DevOps**, com o objetivo de aplicar de forma prática os conhecimentos adquiridos nas disciplinas de:
* `Processos de Software e Gerência de Configuração com DevOps`
* `Inteligência Artificial Aplicada`
* `Estrutura de Dados Orientada a Objeto`
* `Segurança da Informação`

---

## 📖 Índice

- [1. Sobre o Projeto](#1-sobre-o-projeto)
- [2. Features Principais](#2-features-principais)
- [3. Integração com as Disciplinas do Módulo](#3-integração-com-as-disciplinas-do-módulo)
  - [🧠 Inteligência Artificial Aplicada](#-inteligência-artificial-aplicada)
  - [🧱 Estrutura de Dados Orientada a Objeto](#-estrutura-de-dados-orientada-a-objeto)
  - [🛡️ Segurança da Informação](#️-segurança-da-informação)
  - [⚙️ Processos de Software e DevOps](#️-processos-de-software-e-devops)
- [4. Arquitetura e Tecnologias](#4-arquitetura-e-tecnologias)
- [5. Como Executar o Projeto (Planejado)](#5-como-executar-o-projeto-planejado)
- [6. Equipe](#6-equipe)

---

## 1. Sobre o Projeto

O **OptimaTask** nasce da necessidade de transformar a maneira como gerenciamos nossas tarefas diárias. Enquanto as listas de tarefas tradicionais são passivas, exigindo que o usuário organize e priorize seu próprio fluxo de trabalho, o OptimaTask atua como um **assistente proativo**.

Utilizando inteligência artificial, a plataforma aprende com os hábitos do usuário para não apenas listar tarefas, mas também para **sugerir o plano diário mais eficiente**, otimizando a produtividade e ajudando a evitar o esgotamento (burnout). A aplicação visa ser uma solução completa para estudantes e profissionais que buscam maximizar seu tempo e foco.

## 2. Features Principais

-   **🤖 Agendamento Inteligente:** Cria uma agenda diária otimizada, alocando tarefas nos melhores horários com base no histórico de produtividade do usuário.
-   **⏱️ Previsão de Duração de Tarefas:** Utiliza um modelo de Machine Learning para estimar o tempo necessário para completar novas tarefas, tornando o planejamento mais realista.
-   **📊 Priorização Dinâmica:** Calcula uma "pontuação de urgência" para cada tarefa, considerando prazo, complexidade e energia necessária.
-   **🔄 Reagendamento Adaptativo:** Se um imprevisto ocorre, o sistema recalcula e sugere um novo plano para o restante do dia em tempo real.
-   **📈 Dashboard de Produtividade:** Apresenta relatórios visuais sobre o desempenho do usuário, ajudando a identificar padrões e a melhorar continuamente.

## 3. Integração com as Disciplinas do Módulo

Este projeto foi desenhado para ser um ecossistema onde os conceitos das quatro disciplinas do módulo são aplicados de forma sinérgica.

### 🧠 Inteligência Artificial Aplicada

A IA é o **cérebro** do OptimaTask, responsável por toda a inteligência e automação da plataforma.
-   **Modelo de Regressão:** Será treinado para prever a duração de tarefas com base em dados históricos (tipo de tarefa, complexidade, hora do dia, etc.).
-   **Algoritmo de Otimização/Heurística:** Será desenvolvido para resolver o "problema do agendamento", distribuindo as tarefas ao longo do dia para maximizar a eficiência.
-   **Sistema de Recomendação:** Sugerirá pausas estratégicas (ex: técnica Pomodoro) e o agrupamento de tarefas similares.

### 🧱 Estrutura de Dados Orientada a Objeto

A ED-OO é a **espinha dorsal** que garante que o sistema seja robusto, escalável e de fácil manutenção.
-   **Modelagem de Classes:** O domínio do problema será modelado com classes como `Usuario`, `Tarefa`, `Projeto` e `AgendaDiaria`, utilizando conceitos de encapsulamento, herança e polimorfismo.
-   **Estruturas de Dados Eficientes:**
    -   `Priority Queue (Fila de Prioridade)`: Para gerenciar a ordem de execução das tarefas com base na pontuação de urgência calculada pela IA.
    -   `Graph (Grafo)`: Para mapear dependências entre tarefas (A precisa ser concluída antes de B).
    -   `Hash Table`: Para armazenamento e consulta rápida do histórico de tarefas concluídas.

### 🛡️ Segurança da Informação

A segurança é o **guardião** dos dados do usuário, garantindo privacidade e integridade.
-   **Autenticação e Autorização Segura:** Implementação de sistema de login com senhas armazenadas com **hashing e salting (bcrypt)**. O controle de sessão será feito via **JSON Web Tokens (JWT)**.
-   **Criptografia de Dados:** Todo o tráfego de rede será criptografado com **HTTPS (SSL/TLS)**. Dados sensíveis no banco de dados poderão ser criptografados em repouso.
-   **Prevenção a Ataques:** Validação e sanitização de todas as entradas do usuário para prevenir vulnerabilidades comuns como **SQL Injection** e **Cross-Site Scripting (XSS)**.

### ⚙️ Processos de Software e DevOps

DevOps define a **fábrica** que nos permitirá construir, testar e entregar o OptimaTask de forma ágil e confiável.
-   **Controle de Versão com Git:** Todo o código-fonte será versionado com Git e hospedado em um repositório no GitHub, utilizando um fluxo de trabalho com branches (ex: Git Flow).
-   **Metodologia Ágil (Scrum):** O projeto será dividido em Sprints, com planejamento, execuções e revisões periódicas para garantir entregas de valor contínuas.
-   **CI/CD (Integração e Entrega Contínua):** Uma esteira automatizada com **GitHub Actions** será configurada para:
    -   **CI:** Rodar testes automatizados a cada novo commit.
    -   **CD:** Fazer o deploy da aplicação em um ambiente de nuvem (ex: Vercel, Heroku, AWS) após a aprovação nos testes.
-   **Containerização com Docker:** A aplicação e seus serviços serão encapsulados em contêineres Docker, garantindo a padronização dos ambientes de desenvolvimento e produção.

## 4. Arquitetura e Tecnologias

A arquitetura planejada seguirá um modelo de microsserviços ou um monolito bem modularizado, com a seguinte stack tecnológica:

| Camada | Tecnologia Sugerida |
| :--- | :--- |
| **Frontend** | React.js ou Vue.js |
| **Backend** | Python (com Flask/Django) ou Node.js (com Express/NestJS) |
| **Banco de Dados** | PostgreSQL |
| **IA / Machine Learning**| Python com bibliotecas Scikit-learn, Pandas e NumPy |
| **DevOps** | Git, GitHub Actions, Docker |

## 5. Como Executar o Projeto (Planejado)

*Este é um guia preliminar de como o projeto será executado quando as primeiras versões estiverem disponíveis.*

**Pré-requisitos:**
-   Node.js (v18+)
-   Python (v3.9+)
-   Docker

```bash
# 1. Clone o repositório
git clone [https://github.com/SEU-USUARIO/optimatask.git](https://github.com/SEU-USUARIO/optimatask.git)

# 2. Navegue para a pasta do projeto
cd optimatask

# 3. Suba os contêineres Docker (Backend, DB, etc.)
docker-compose up -d

# 4. Instale as dependências e execute o Frontend
cd frontend
npm install
npm run dev
