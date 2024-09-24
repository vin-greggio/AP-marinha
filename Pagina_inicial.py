import streamlit as st
import hashlib
import json
import os
import pandas as pd
from PyPDF2 import PdfFileReader
import matplotlib.pyplot as plt
import matplotlib
import plotly_express as px
from streamlit_option_menu import option_menu
from supabase import create_client, Client

#INICIO DATAFRAMES

matplotlib.use('TkAgg')

@st.cache_resource
def init_connection():
    url = "https://fudwcyqizyszfqgwvmik.supabase.co"
    key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZ1ZHdjeXFpenlzemZxZ3d2bWlrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjU5ODU2NDIsImV4cCI6MjA0MTU2MTY0Mn0.OfjRY2WeMZLlxgMJzYuTOLM390FWBrnOY9kGKp3oYgA'
    return create_client(url, key)

supabase = init_connection()
rows,count = supabase.table('ReceitasxDespesas').select('*').execute()
df = pd.DataFrame(rows[1])

fig = px.bar(df.sort_values('SALDO'), x='CONDOMINIO',y='SALDO', color='CONDOMINIO')
st.plotly_chart(fig)

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
st.sidebar.image('imgmar.jpeg')
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
        if selected=='Planilhas':

            restituicoes_file = st.file_uploader("Insira o CSV da planilha restituições", type="csv")
            desocupados_file = st.file_uploader("Insira o CSV da planilha desocupados", type="csv")
            isolados_file = st.file_uploader("Insira o CSV da planilha isolados", type="csv")
            taxaextra_file = st.file_uploader("Insira o CSV da planilha taxa extra", type="csv")

            if restituicoes_file is not None:
                restituicoes_df = pd.read_csv(restituicoes_file)
                st.write("Insira o arquivo CSV:", restituicoes_df)
                
                table_name = "restituicoes"
                
                data_to_insert = restituicoes_df.to_dict(orient='records')

                response = supabase.table(table_name).insert(data_to_insert).execute()
                st.write(response)
            
            if desocupados_file is not None:
                desocupados_df = pd.read_csv(desocupados_file)
                st.write("Insira o arquivo CSV:", desocupados_df)
                
                table_name = "desocupados"
                
                data_to_insert = desocupados_df.to_dict(orient='records')

                response = supabase.table(table_name).insert(data_to_insert).execute()
                st.write(response)
            
            if isolados_file is not None:
                isolados_df = pd.read_csv(isolados_file)
                st.write("Insira o arquivo CSV:", isolados_df)
                
                table_name = "isolados"
                
                data_to_insert = isolados_df.to_dict(orient='records')

                response = supabase.table(table_name).insert(data_to_insert).execute()
                st.write(response)

            if taxaextra_file is not None:
                taxaextra_df = pd.read_csv(taxaextra_file)
                st.write("Insira o arquivo CSV:", taxaextra_df)
                
                table_name = "taxa_extra"
                
                data_to_insert = taxaextra_df.to_dict(orient='records')

                response = supabase.table(table_name).insert(data_to_insert).execute()
                st.write(response)
        
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
            
        if selected=='Alterar Senha':
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
