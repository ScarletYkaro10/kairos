import streamlit as st
import requests
import os
import socket

# Detecta automaticamente a URL do backend
def get_backend_url():
    """Detecta a URL do backend automaticamente."""
    env_url = os.getenv("BACKEND_URL")
    if env_url:
        return env_url
    
    # Tenta resolver o hostname 'backend' (funciona dentro do Docker)
    try:
        socket.gethostbyname("backend")
        return "http://backend:8000"
    except (socket.gaierror, socket.herror):
        # Se não conseguir resolver, usa localhost
        return "http://localhost:8000"

BACKEND_URL = get_backend_url()

# Log para debug (pode ser removido em produção)
if os.getenv("STREAMLIT_DEBUG"):
    print(f"[DEBUG] Backend URL configurada: {BACKEND_URL}")

st.set_page_config(page_title="Kairos", page_icon="⏰", layout="wide")

st.title("⏰ Kairos - Gerenciador de Tarefas")

# Sidebar para autenticação
st.sidebar.title("Autenticação")

# Inicializa variáveis de sessão
if "token" not in st.session_state:
    st.session_state.token = None
if "user_id" not in st.session_state:
    st.session_state.user_id = None

# Função para fazer requisições autenticadas
def make_authenticated_request(method, endpoint, **kwargs):
    """Faz uma requisição autenticada para o backend."""
    headers = kwargs.get("headers", {})
    if st.session_state.token:
        headers["Authorization"] = f"Bearer {st.session_state.token}"
    kwargs["headers"] = headers
    return requests.request(method, f"{BACKEND_URL}{endpoint}", **kwargs)

# Tabs para diferentes funcionalidades
tab1, tab2, tab3 = st.tabs(["Login/Registro", "Tarefas", "Sobre"])

with tab1:
    st.header("Login / Registro")
    
    login_tab, register_tab = st.tabs(["Login", "Registro"])
    
    with login_tab:
        st.subheader("Fazer Login")
        login_email = st.text_input("Email", key="login_email")
        login_password = st.text_input("Senha", type="password", key="login_password")
        
        if st.button("Login"):
            try:
                response = requests.post(
                    f"{BACKEND_URL}/auth/login",
                    json={"email": login_email, "password": login_password}
                )
                if response.status_code == 200:
                    data = response.json()
                    st.session_state.token = data["access_token"]
                    st.success("Login realizado com sucesso!")
                    st.rerun()
                else:
                    st.error(f"Erro: {response.json().get('detail', 'Erro desconhecido')}")
            except Exception as e:
                st.error(f"Erro ao conectar com o backend: {e}")
    
    with register_tab:
        st.subheader("Criar Conta")
        register_email = st.text_input("Email", key="register_email")
        register_password = st.text_input("Senha", type="password", key="register_password", help="Mínimo de 8 caracteres")
        
        if st.button("Registrar"):
            try:
                response = requests.post(
                    f"{BACKEND_URL}/auth/register",
                    json={"email": register_email, "password": register_password}
                )
                if response.status_code == 201:
                    st.success("Conta criada com sucesso! Faça login agora.")
                else:
                    st.error(f"Erro: {response.json().get('detail', 'Erro desconhecido')}")
            except Exception as e:
                st.error(f"Erro ao conectar com o backend: {e}")
    
    if st.session_state.token:
        st.info("✅ Você está logado!")
        if st.button("Logout"):
            st.session_state.token = None
            st.session_state.user_id = None
            st.rerun()

with tab2:
    st.header("Gerenciar Tarefas")
    
    if not st.session_state.token:
        st.warning("⚠️ Faça login para gerenciar suas tarefas.")
    else:
        # Criar nova tarefa
        with st.expander("➕ Criar Nova Tarefa"):
            new_title = st.text_input("Título", key="new_title")
            new_description = st.text_area("Descrição", key="new_description")
            new_priority = st.selectbox("Prioridade", ["low", "medium", "high"], key="new_priority")
            
            if st.button("Criar Tarefa"):
                try:
                    response = make_authenticated_request(
                        "POST",
                        "/tasks",
                        json={
                            "title": new_title,
                            "description": new_description,
                            "priority": new_priority
                        }
                    )
                    if response.status_code == 201:
                        st.success("Tarefa criada com sucesso!")
                        st.rerun()
                    else:
                        st.error(f"Erro: {response.json().get('detail', 'Erro desconhecido')}")
                except Exception as e:
                    st.error(f"Erro ao criar tarefa: {e}")
        
        # Listar tarefas
        st.subheader("Suas Tarefas")
        try:
            response = make_authenticated_request("GET", "/tasks")
            if response.status_code == 200:
                tasks = response.json()
                if tasks:
                    for task in tasks:
                        with st.container():
                            col1, col2 = st.columns([3, 1])
                            with col1:
                                st.write(f"**{task['title']}**")
                                if task.get('description'):
                                    st.write(task['description'])
                                st.caption(f"Prioridade: {task['priority']} | Status: {task['status']}")
                            with col2:
                                st.write(f"ID: {task['id'][:8]}...")
                else:
                    st.info("Você ainda não tem tarefas. Crie uma nova tarefa acima!")
            else:
                st.error(f"Erro ao buscar tarefas: {response.json().get('detail', 'Erro desconhecido')}")
        except Exception as e:
            st.error(f"Erro ao conectar com o backend: {e}")

with tab3:
    st.header("Sobre o Kairos")
    st.write("""
    **Kairos** é um gerenciador de tarefas inteligente que ajuda você a organizar 
    e otimizar seu tempo.
    
    ### Funcionalidades:
    - ✅ Autenticação segura
    - 📝 Criação e gerenciamento de tarefas
    - 🎯 Sistema de prioridades
    - 🤖 Otimização de agenda (em desenvolvimento)
    
    ### Tecnologias:
    - Backend: FastAPI + PostgreSQL
    - Frontend: Streamlit
    - Autenticação: JWT
    """)

