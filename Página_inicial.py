import streamlit as st
import hashlib

# Função para criptografar senhas
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Base de dados inicial (em memória) para usuários
users_db = {
    "admin": {"password": hash_password("adminpass"), "role": "editor"},
    "viewer": {"password": hash_password("viewerpass"), "role": "viewer"}
}

# Função para verificar se um usuário e senha estão corretos
def authenticate(username, password):
    if username in users_db and users_db[username]['password'] == hash_password(password):
        return True
    return False

# Função para criar um novo usuário
def create_user(username, password, role):
    if username in users_db:
        return False
    users_db[username] = {"password": hash_password(password), "role": role}
    return True

# Função para alterar a senha de um usuário
def change_password(username, old_password, new_password):
    if authenticate(username, old_password):
        users_db[username]['password'] = hash_password(new_password)
        return True
    return False

# Função para verificar a permissão do usuário
def has_permission(username, role):
    return users_db.get(username, {}).get("role") == role

st.title("Sistema de Perfis com Streamlit")

# Interface de autenticação
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

# Verifica se o usuário está autenticado
if 'authenticated' in st.session_state and st.session_state['authenticated']:
    st.write(f"Usuário logado: {st.session_state['username']} ({st.session_state['role']})")

    if st.session_state['role'] == 'editor':
        st.header("Editor Dashboard")
        st.write("Aqui os editores podem modificar os dashboards.")

        # Opção para criar novo usuário
        st.subheader("Criar novo usuário")
        new_username = st.text_input("Novo usuário")
        new_password = st.text_input("Primeira senha", type="password")
        new_role = st.selectbox("Função", ["editor", "viewer"])
        create_user_button = st.button("Criar usuário")

        if create_user_button:
            if create_user(new_username, new_password, new_role):
                st.success("Usuário criado com sucesso!")
            else:
                st.error("Usuário já existe.")

    if st.session_state['role'] in ['editor', 'viewer']:
        st.header("Visualização de Dashboard")
        st.write("Aqui os usuários podem visualizar os dashboards.")

        # Opção para alterar a senha
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