import streamlit as st
import hashlib
import json
import os
import pandas as pd
from PyPDF2 import PdfFileReader
from streamlit_option_menu import option_menu

#INICIO DAS FUNÇOES
#########################################################################################

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    if os.path.exists("users.json"):
        with open("users.json", "r") as file:
            return json.load(file)
    return {}

def save_users(users):
    with open("users.json", "w") as file:
        json.dump(users, file)

users_db = load_users()

def authenticate(username, password):
    if username in users_db and users_db[username]['password'] == hash_password(password):
        return True
    return False

def create_user(username, password, role):
    if username in users_db:
        return False
    users_db[username] = {"password": hash_password(password), "role": role}
    save_users(users_db)
    return True

def change_password(username, old_password, new_password):
    if authenticate(username, old_password):
        users_db[username]['password'] = hash_password(new_password)
        save_users(users_db)
        return True
    return False

def has_permission(username, role):
    return users_db.get(username, {}).get("role") == role

#FIM DAS FUNCOES
####################################################################################

st.title("Sistema de Planilhas AP Marinha")
create_user('miguel', '12345', 'viewer')
st.sidebar.image('i.png')
st.sidebar.header("Login")
username = st.sidebar.text_input("Usuário")
password = st.sidebar.text_input("Senha", type="password")
login_button = st.sidebar.button("Login")

if login_button:
    if authenticate(username, password):
        st.sidebar.success(f"Bem-vindo {username}!")
        st.session_state['authenticated'] = True
        st.session_state['username'] = username
        st.session_state['role'] = users_db[username]['role']
    else:
        st.sidebar.error("Usuário ou senha incorretos.")
####################################################################################


# COMEÇA AQUI A PARTIR DE LOGADO


####################################################################################
if 'authenticated' in st.session_state and st.session_state['authenticated']:
    st.write(f"Usuário logado: {st.session_state['username']} ({st.session_state['role']})")


    #CASO EDITOR:
    if st.session_state['role'] == 'editor':

        with st.sidebar:
            selected = option_menu(
                    "Menu",
                    ["Planilhas", 'Empréstimo', 'Alterar Senha', 'Criar Usuário'],
                    icons=['info', 'calculator'],)

        if selected=='Empréstimo':
            with st.form("Formulário de empréstimo"):
                st.write("Insira as informações do novo empréstimo")
                nome_emprestimo = st.text_input('Nome')
                valor_emprestimo = st.text_input('Valor')
                tempo_meses = st.text_input('Meses')
                st.form_submit_button('Criar empréstimo')

        elif selected=='Planilhas':
            st.title('Planilhas')
            xls = pd.ExcelFile('big planilha.xlsx')
            planilha_selecionada = st.selectbox('Selecione a planilha desejada', ['BP_Pagamento','Condomínio Papem', 'Taxa_de_Condomínio', 'Despesas', 'ReceitasxDespesas', 'Previsão orçamentaria', 'Taxa complementar', 'Empréstimo'])
            df = pd.read_excel(xls, sheet_name=planilha_selecionada)
            df = st.data_editor(df, num_rows='dynamic')

        elif selected=='Alterar Senha':
                st.subheader("Alterar senha")
                old_password = st.text_input("Senha antiga", type="password")
                new_password = st.text_input("Nova senha", type="password")
                change_password_button = st.button("Alterar senha")

                if change_password_button:
                    if change_password(st.session_state['username'], old_password, new_password):
                        st.success("Senha alterada com sucesso!")
                    else:
                        st.error("Senha antiga incorreta.")
        elif selected == 'Criar Usuário':
            st.subheader("Criar novo usuário")
            new_username = st.text_input("Novo usuário")
            new_password = st.text_input("Primeira Senha", type="password")
            new_role = st.selectbox("Função", ["editor", "viewer"])
            create_user_button = st.button("Criar usuário")

            if create_user_button:
                if create_user(new_username, new_password, new_role):
                    st.success("Usuário criado com sucesso!")
                else:
                    st.error("Usuário já existe.")
    #CASO NÃO EDITOR:
    else:
        with st.sidebar:
            selected = option_menu(
                    "Menu",
                    ["Planilhas", 'Empréstimo', 'Alterar Senha', 'Criar Usuário'],
                    icons=['info', 'calculator'],)

        if selected=='Empréstimo':
            with st.form("Formulário de empréstimo"):
                st.write("Insira as informações do novo empréstimo")
                nome_emprestimo = st.text_input('Nome')
                valor_emprestimo = st.text_input('Valor')
                tempo_meses = st.text_input('Meses')
                st.form_submit_button('Criar empréstimo')

        elif selected=='Planilhas':
            st.title('Planilhas')
            xls = pd.ExcelFile('big planilha.xlsx')
            planilha_selecionada = st.selectbox('Selecione a planilha desejada', ['BP_Pagamento','Condomínio Papem', 'Taxa_de_Condomínio', 'Despesas', 'ReceitasxDespesas', 'Previsão orçamentaria', 'Taxa complementar', 'Empréstimo'])
            df = pd.read_excel(xls, sheet_name=planilha_selecionada)
            df = st.dataframe(df)
                    
        elif selected=='Alterar Senha':
            st.subheader("Alterar senha")
            old_password = st.text_input("Senha antiga", type="password")
            new_password = st.text_input("Nova senha", type="password")
            change_password_button = st.button("Alterar senha")

            if change_password_button:
                if change_password(st.session_state['username'], old_password, new_password):
                    st.success("Senha alterada com sucesso!")
                else:
                    st.error("Senha antiga incorreta.")



else:
    st.write("Por favor, faça login para continuar.")
