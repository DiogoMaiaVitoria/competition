import streamlit as st
import pyodbc
import pandas as pd

def conectar():
    server = '192.168.20.103\\POWER_BI'
    database = 'Wyscout'
    try:
        conn = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        )
        return conn
    except Exception as e:
        st.error(f"Erro ao conectar: {e}")
        return None

def obter_logo_vitoria():
    conn = conectar()
    if conn:
        try:
            query = """
            SELECT team_logo 
            FROM [Wyscout].[dbo].[teams] 
            WHERE team_id = '9617'
            """
            df = pd.read_sql(query, conn)
            conn.close()
            if not df.empty:
                return df.iloc[0]['team_logo']
        except Exception as e:
            st.error(f"Erro ao buscar logo: {e}")
    return None

def obter_dados_teams():
    conn = conectar()
    if conn:
        try:
            df = pd.read_sql("SELECT * FROM [Wyscout].[dbo].[teams]", conn)
            conn.close()
            return df
        except Exception as e:
            st.error(f"Erro na consulta teams: {e}")
    return pd.DataFrame()

def obter_dados_players():
    conn = conectar()
    if conn:
        try:
            df = pd.read_sql("SELECT * FROM [Wyscout].[dbo].[players]", conn)
            conn.close()
            return df
        except Exception as e:
            st.error(f"Erro na consulta players: {e}")
    return pd.DataFrame()

def obter_dados_coaches():
    conn = conectar()
    if conn:
        try:
            df = pd.read_sql("SELECT * FROM [Wyscout].[dbo].[coaches]", conn)
            conn.close()
            return df
        except Exception as e:
            st.error(f"Erro na consulta coaches: {e}")
    return pd.DataFrame()

if "page" not in st.session_state:
    st.session_state.page = "entrada"

def mostrar_entrada():
    logo_url = obter_logo_vitoria()

    st.markdown("""
    <style>
        .card {
            background-color: #f0f2f6;
            border: 1px solid #ccc;
            border-radius: 15px;
            padding: 30px 20px;
            text-align: center;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
            transition: transform 0.2s ease-in-out;
            height: 100%;
        }
        .card:hover {
            transform: scale(1.03);
            background-color: #e0e7ff;
        }
        .emoji {
            font-size: 3rem;
            margin-bottom: 10px;
        }
        .card-title {
            font-size: 1.5rem;
            font-weight: bold;
        }
        .card-desc {
            color: #555;
            margin: 10px 0 15px;
        }
        .explore-btn button {
            width: 100%;
            border-radius: 8px;
            margin-top: 10px;
        }
    </style>
    """, unsafe_allow_html=True)

    # Cabeçalho com logo e título na mesma linha, alinhados horizontalmente
    st.markdown(
        f'''
        <div style="display: flex; align-items: center; justify-content: center; gap: 10px; margin-bottom: 40px;">
            <h1 style="margin: 0;">Welcome to Competition Report</h1>
            {'<img src="' + logo_url + '" style="height:50px;"/>' if logo_url else ''}
        </div>
        ''',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="card">
            <div class="emoji">👕</div>
            <div class="card-title">Teams</div>
            <div class="card-desc">Find all the teams you want</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Explore here", key="explore_teams"):
            st.session_state.page = "teams"
            st.rerun()

    with col2:
        st.markdown("""
        <div class="card">
            <div class="emoji">⚽</div>
            <div class="card-title">Players</div>
            <div class="card-desc">Find all the players you want</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Explore here", key="explore_players"):
            st.session_state.page = "players"
            st.rerun()

    with col3:
        st.markdown("""
        <div class="card">
            <div class="emoji">👔</div>
            <div class="card-title">Coaches</div>
            <div class="card-desc">Find all the coaches you want</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Explore here", key="explore_coaches"):
            st.session_state.page = "coaches"
            st.rerun()

def mostrar_teams():
    st.title("📋 Teams")
    df = obter_dados_teams()
    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("Nenhum dado encontrado em Teams.")
    if st.button("Voltar"):
        st.session_state.page = "entrada"
        st.rerun()

def mostrar_players():
    st.title("📋 Players")
    df = obter_dados_players()
    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("Nenhum dado encontrado em Players.")
    if st.button("Voltar"):
        st.session_state.page = "entrada"
        st.rerun()

def mostrar_coaches():
    st.title("📋 Coaches")
    df = obter_dados_coaches()
    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("Nenhum dado encontrado em Coaches.")
    if st.button("Voltar"):
        st.session_state.page = "entrada"
        st.rerun()

if st.session_state.page == "entrada":
    mostrar_entrada()
elif st.session_state.page == "teams":
    mostrar_teams()
elif st.session_state.page == "players":
    mostrar_players()
elif st.session_state.page == "coaches":
    mostrar_coaches()
