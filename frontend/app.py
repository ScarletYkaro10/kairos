import streamlit as st
import requests
import time
import os
import socket
from datetime import datetime, time as dt_time


def get_backend_url():
    env_url = os.getenv("BACKEND_URL")
    if env_url:
        return env_url

    try:
        socket.gethostbyname("backend")
        return "http://backend:8000"
    except:
        return "http://127.0.0.1:8000"


API_URL = get_backend_url()

st.set_page_config(page_title="Kairós", page_icon="⏳", layout="wide")

st.markdown(
    """
<style>
    .task-card {
        background-color: var(--secondary-background-color);
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        margin-bottom: 15px;
        border-left: 6px solid #ccc;
        transition: transform 0.2s;
    }
    .task-card:hover { transform: translateY(-2px); box-shadow: 0 4px 10px rgba(0,0,0,0.2); }
    div[data-testid="stMetric"] { background-color: var(--secondary-background-color); padding: 15px; border-radius: 10px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
    .stButton>button { border-radius: 8px; font-weight: 600; height: 3em; }
    .card-title { margin:0; color: var(--text-color); }
    .card-desc { margin: 5px 0 10px 0; color: var(--text-color); opacity: 0.8; font-size:0.95em; }
    .card-meta { display:flex; justify-content:space-between; font-size:0.85em; color: var(--text-color); opacity: 0.7; }
</style>
""",
    unsafe_allow_html=True,
)

if "token" not in st.session_state:
    st.session_state["token"] = None


def format_date_br(iso_str):
    if not iso_str:
        return "Sem data"
    try:
        return datetime.fromisoformat(iso_str.replace("Z", "")).strftime("%d/%m/%Y")
    except:
        return iso_str


def format_time_br(iso_str):
    if not iso_str:
        return ""
    try:
        return datetime.fromisoformat(iso_str.replace("Z", "")).strftime("%H:%M")
    except:
        return ""


def login_screen():
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown(
            "<h1 style='text-align: center;'>⏳ Kairós</h1>", unsafe_allow_html=True
        )
        st.markdown(
            "<p style='text-align: center; color: gray;'>Seu Assistente de Produtividade Inteligente!</p>",
            unsafe_allow_html=True,
        )

        with st.container(border=True):
            tab1, tab2 = st.tabs(["Entrar", "Criar Conta"])

            with tab1:
                email = st.text_input("E-mail", key="log_email")
                password = st.text_input("Senha", type="password", key="log_pass")
                if st.button("Acessar", type="primary", use_container_width=True):
                    token_recebido = None
                    erro_msg = None
                    try:
                        res = requests.post(
                            f"{API_URL}/auth/login",
                            json={"email": email, "password": password},
                        )
                        if res.status_code == 200:
                            token_recebido = res.json()["access_token"]
                        else:
                            erro_msg = "E-mail ou senha incorretos."
                    except:
                        erro_msg = f"Erro de conexão com {API_URL}"

                    if token_recebido:
                        st.session_state["token"] = token_recebido
                        st.rerun()
                    elif erro_msg:
                        st.error(erro_msg)

            with tab2:
                n_email = st.text_input("E-mail Cadastro", key="reg_email")
                n_pass = st.text_input(
                    "Senha (min 8 chars)", type="password", key="reg_pass"
                )
                if st.button("Criar Conta", use_container_width=True):
                    if len(n_pass) < 8:
                        st.warning("Senha muito curta.")
                    else:
                        sucesso_cadastro = False
                        msg_erro = None
                        try:
                            res = requests.post(
                                f"{API_URL}/auth/register",
                                json={"email": n_email, "password": n_pass},
                            )
                            if res.status_code == 201:
                                sucesso_cadastro = True
                            elif res.status_code == 422:
                                msg_erro = "E-mail inválido ou senha fraca."
                            else:
                                msg_erro = f"Erro: {res.text}"
                        except:
                            msg_erro = "Erro de conexão."

                        if sucesso_cadastro:
                            st.success("Conta criada! Vá para a aba 'Entrar'.")
                        elif msg_erro:
                            st.error(msg_erro)


def delete_task_callback(task_id, auth_headers):
    try:
        res = requests.delete(f"{API_URL}/tasks/{task_id}", headers=auth_headers)
        if res.status_code in [200, 204]:
            st.toast("Tarefa excluída com sucesso! 🗑️")
        else:
            st.toast(f"Erro ao excluir: {res.text}")
    except Exception as e:
        st.toast(f"Erro de conexão: {e}")


def dashboard_screen():
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/4296/4296463.png", width=50)
        st.markdown("### Menu")
        if st.button("Sair", use_container_width=True):
            st.session_state["token"] = None
            st.rerun()

    headers = {"Authorization": f"Bearer {st.session_state['token']}"}

    c1, c2 = st.columns([3, 1])
    c1.title("Minha Agenda")
    c2.write("")
    c2.write("")
    if c2.button("🔄 Atualizar"):
        st.rerun()

    tasks = []
    try:
        r = requests.get(f"{API_URL}/tasks", headers=headers)
        if r.status_code == 200:
            tasks = r.json()
    except:
        st.error("Backend offline.")

    if tasks:
        high = sum(1 for t in tasks if t.get("priority") == "high")
        med = sum(1 for t in tasks if t.get("priority") == "medium")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total", len(tasks))
        col2.metric("Alta 🔥", high)
        col3.metric("Média ⚡", med)
        col4.metric("Baixa 🌱", len(tasks) - high - med)

    st.divider()

    with st.expander("➕ Nova Tarefa", expanded=False):
        with st.form("new_task", clear_on_submit=True):
            t_title = st.text_input("Título")
            t_cat = st.selectbox(
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
            t_desc = st.text_area("Descrição", height=60)
            cc1, cc2, cc3 = st.columns(3)
            t_dif = cc1.slider("Dificuldade", 1, 5, 3)
            t_date = cc2.date_input("Data")
            t_time = cc2.time_input("Hora", value=dt_time(9, 0))
            t_min = cc3.number_input("Duração (min)", 15, 480, 60)

            if st.form_submit_button("Salvar", type="primary"):
                dt_full = datetime.combine(t_date, t_time).isoformat()
                payload = {
                    "title": t_title,
                    "description": t_desc,
                    "category": t_cat,
                    "difficulty": t_dif,
                    "estimated_minutes": t_min,
                    "due_date": dt_full,
                    "priority": "medium",
                }

                sucesso_save = False
                try:
                    res = requests.post(
                        f"{API_URL}/tasks", json=payload, headers=headers
                    )
                    if res.status_code in [200, 201]:
                        sucesso_save = True
                    else:
                        st.error(f"Erro: {res.text}")
                except:
                    st.error("Erro conexão.")

                if sucesso_save:
                    st.toast("Tarefa Salva! ✅")
                    time.sleep(1)
                    st.rerun()

    st.write("")
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
                time.sleep(1)
                st.rerun()

    st.write("")
    if not tasks:
        st.info("Nenhuma tarefa.")
    else:
        for t in tasks:
            prio = t.get("priority", "medium")
            colors = {"high": "#ff4b4b", "medium": "#ffa421", "low": "#09ab3b"}
            icons = {"high": "🔥 ALTA", "medium": "⚡ MÉDIA", "low": "🌱 BAIXA"}
            bg_icons = {"high": "#ffebeb", "medium": "#fff8e6", "low": "#e6f9e6"}

            c = colors.get(prio, "gray")
            icon = icons.get(prio, "")
            bg = bg_icons.get(prio, "#eee")

            with st.container():
                c_info, c_del = st.columns([0.9, 0.1])

                with c_info:
                    st.markdown(
                        f"""
                    <div class="task-card" style="border-left: 6px solid {c};">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <h4 class="card-title">{t['title']}</h4>
                            <span style="background-color:{bg}; color:{c}; padding:4px 10px; border-radius:15px; font-weight:bold; font-size:0.8em;">{icon}</span>
                        </div>
                        <p class="card-desc">{t.get('description') or ''}</p>
                        <div class="card-meta">
                            <span>📂 {t.get('category')}</span>
                            <span>⏱ {t.get('estimated_minutes')} min</span>
                            <span>📅 {format_date_br(t.get('due_date'))} {format_time_br(t.get('due_date'))}</span>
                        </div>
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )

                with c_del:
                    st.write("")
                    st.write("")
                    st.button(
                        "🗑️",
                        key=f"del_{t['id']}",
                        help="Excluir",
                        on_click=delete_task_callback,
                        args=(t["id"], headers),
                    )


if st.session_state["token"]:
    dashboard_screen()
else:
    login_screen()
