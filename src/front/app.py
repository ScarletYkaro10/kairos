import streamlit as st
import requests
import time
from datetime import datetime, time as dt_time

st.set_page_config(page_title="Kairós", page_icon="⏳", layout="wide")
API_URL = "http://127.0.0.1:8000"

st.markdown(
    """
<style>
    /* Cards de Tarefas Adaptativos */
    .task-card {
        background-color: var(--secondary-background-color);
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        margin-bottom: 15px;
        border-left: 6px solid #ccc;
        transition: transform 0.2s;
    }
    .task-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }
    
    /* Métricas Adaptativas */
    div[data-testid="stMetric"] {
        background-color: var(--secondary-background-color);
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }

    /* Botões */
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
        height: 3em;
    }
    
    /* Textos dentro do Card */
    .card-title { margin:0; color: var(--text-color); }
    .card-desc { margin: 5px 0 10px 0; color: var(--text-color); opacity: 0.8; font-size:0.95em; }
    .card-meta { display:flex; justify-content:space-between; font-size:0.85em; color: var(--text-color); opacity: 0.7; }
</style>
""",
    unsafe_allow_html=True,
)

if "token" not in st.session_state:
    st.session_state["token"] = None


def format_date_br(iso_date_str):
    if not iso_date_str:
        return "Sem data"
    try:
        dt = datetime.fromisoformat(iso_date_str.replace("Z", ""))
        return dt.strftime("%d/%m/%Y")
    except:
        return iso_date_str


def format_time_br(iso_date_str):
    if not iso_date_str:
        return ""
    try:
        dt = datetime.fromisoformat(iso_date_str.replace("Z", ""))
        return dt.strftime("%H:%M")
    except:
        return ""


def login_screen():
    col1, col2, col3 = st.columns([1, 1.5, 1])

    with col2:
        st.markdown(
            "<h1 style='text-align: center;'>⏳ Kairós</h1>", unsafe_allow_html=True
        )
        st.markdown(
            "<p style='text-align: center; color: gray;'>Seu Assistente de Produtividade Inteligente</p>",
            unsafe_allow_html=True,
        )
        st.write("")

        with st.container(border=True):
            tab_login, tab_create = st.tabs(["Entrar", "Criar Conta"])

            with tab_login:
                email = st.text_input("E-mail", key="login_email")
                password = st.text_input("Senha", type="password", key="login_pass")

                if st.button(
                    "Acessar Sistema", type="primary", use_container_width=True
                ):
                    login_success = False
                    try:
                        res = requests.post(
                            f"{API_URL}/auth/login",
                            json={"email": email, "password": password},
                        )
                        if res.status_code == 200:
                            st.session_state["token"] = res.json()["access_token"]
                            login_success = True
                        else:
                            st.error("E-mail ou senha incorretos.")
                    except:
                        st.error("Erro ao conectar com o servidor.")

                    if login_success:
                        st.rerun()

            with tab_create:
                new_email = st.text_input("Seu E-mail", key="new_email")
                new_pass = st.text_input(
                    "Crie uma Senha (min 8 caracteres)", type="password", key="new_pass"
                )

                if st.button("Criar Minha Conta", use_container_width=True):
                    if len(new_pass) < 8:
                        st.warning("Senha muito curta.")
                    else:
                        create_success = False
                        try:
                            res = requests.post(
                                f"{API_URL}/auth/register",
                                json={"email": new_email, "password": new_pass},
                            )
                            if res.status_code == 201:
                                create_success = True
                            elif res.status_code == 422:
                                st.error("Dados inválidos (verifique o e-mail).")
                            else:
                                st.error(f"Erro: {res.text}")
                        except:
                            st.error("Erro de conexão.")

                        if create_success:
                            st.success("Conta criada! Acesse a aba 'Entrar'.")
                            time.sleep(1.5)
                            st.rerun()


def dashboard_screen():
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/4296/4296463.png", width=50)
        st.markdown("### Menu")
        st.caption(f"Usuário Conectado")
        if st.button("Sair", use_container_width=True):
            st.session_state["token"] = None
            st.rerun()

    headers = {"Authorization": f"Bearer {st.session_state['token']}"}

    c_title, c_btn = st.columns([3, 1])
    with c_title:
        st.title("Minha Agenda")
    with c_btn:
        st.write("")
        refresh = st.button("🔄 Atualizar Lista", use_container_width=True)

    tasks = []
    try:
        res = requests.get(f"{API_URL}/tasks", headers=headers)
        if res.status_code == 200:
            tasks = res.json()
    except:
        st.error("Servidor offline.")

    if tasks:
        total = len(tasks)
        high = sum(1 for t in tasks if t.get("priority") == "high")
        medium = sum(1 for t in tasks if t.get("priority") == "medium")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total de Tarefas", total)
        m2.metric("Alta Prioridade 🔥", high)
        m3.metric("Média Prioridade ⚡", medium)
        m4.metric("Baixa Prioridade 🌱", total - high - medium)

    st.divider()

    with st.expander("➕ Nova Tarefa", expanded=False):
        with st.form("task_form", clear_on_submit=True):
            c_title, c_cat = st.columns([2, 1])
            title = c_title.text_input("Título")
            category = c_cat.selectbox(
                "Categoria",
                [
                    "Trabalho",
                    "Saúde",
                    "Estudo",
                    "Casa",
                    "Lazer",
                    "Projetos",
                    "Finanças",
                ],
            )
            desc = st.text_area("Descrição", height=70)

            c1, c2, c3 = st.columns(3)
            diff = c1.slider("Dificuldade", 1, 5, 3)
            d_date = c2.date_input("Data")
            d_time = c2.time_input("Horário", value=dt_time(9, 0))
            mins = c3.number_input("Duração (min)", value=60, step=15)

            if st.form_submit_button("Salvar Tarefa", type="primary"):
                full_date = datetime.combine(d_date, d_time).isoformat()
                payload = {
                    "title": title,
                    "description": desc,
                    "category": category,
                    "difficulty": diff,
                    "estimated_minutes": mins,
                    "due_date": full_date,
                    "priority": "medium",
                }

                task_saved = False
                try:
                    res = requests.post(
                        f"{API_URL}/tasks", json=payload, headers=headers
                    )
                    if res.status_code in [200, 201]:
                        task_saved = True
                    else:
                        st.error(f"Erro ao salvar: {res.text}")
                except:
                    st.error("Erro de conexão.")

                if task_saved:
                    st.toast("Tarefa criada com sucesso!", icon="✅")
                    time.sleep(1)
                    st.rerun()

    st.markdown("###")
    if st.button("✨ Otimizar Agenda com IA", type="primary", use_container_width=True):
        with st.spinner("A IA está analisando a melhor rota para o seu dia..."):
            ia_success = False
            try:
                res = requests.post(f"{API_URL}/optimize-schedule", headers=headers)
                if res.status_code == 200:
                    tasks = res.json()
                    ia_success = True
                else:
                    st.error("Erro na IA.")
            except:
                st.error("Erro de conexão.")

            if ia_success:
                st.toast("Agenda reorganizada com sucesso!", icon="🤖")

    st.markdown("###")
    if not tasks:
        st.info("Sua lista está vazia. Adicione uma tarefa acima!")
    else:
        for task in tasks:
            prio = task.get("priority", "medium")
            if prio == "high":
                border_color, icon, bg_icon = "#ff4b4b", "🔥 ALTA", "#ffebeb"
            elif prio == "medium":
                border_color, icon, bg_icon = "#ffa421", "⚡ MÉDIA", "#fff8e6"
            else:
                border_color, icon, bg_icon = "#09ab3b", "🌱 BAIXA", "#e6f9e6"

            st.markdown(
                f"""
            <div class="task-card" style="border-left: 6px solid {border_color};">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <h4 class="card-title">{task['title']}</h4>
                    <span style="background-color:{bg_icon}; color:{border_color}; padding: 4px 10px; border-radius:15px; font-size:0.8em; font-weight:bold;">
                        {icon}
                    </span>
                </div>
                <p class="card-desc">
                    {task.get('description') or '<i>Sem descrição</i>'}
                </p>
                <hr style="margin: 5px 0 10px 0; opacity: 0.2;">
                <div class="card-meta">
                    <span>📂 <b>{task.get('category')}</b></span>
                    <span>⏱ {task.get('estimated_minutes')} min</span>
                    <span>🏋️ Nível {task.get('difficulty')}</span>
                    <span>📅 {format_date_br(task.get('due_date'))} às {format_time_br(task.get('due_date'))}</span>
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )


if st.session_state["token"]:
    dashboard_screen()
else:
    login_screen()
