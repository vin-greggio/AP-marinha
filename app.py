import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import joblib
import numpy as np


def transform_data(lista,df):
    lista_nv = {}
    #idade
    for age in df['IDade']:
        if lista[0] == age:
            #agrupar as idades em faixas etárias de 5 em 5 anos
            lista_nv[0] = age // 5
    #sexo
    if lista[1] == 'Masculino':
        lista_nv[1] = 1
    else:
        lista_nv[1] = 0

    #quantidade
    lista_nv[2] = lista[2]
    #evento
    eventos = ['Evento', 'Consulta', 'Hon Medico', 'Exame Simples', 'Exames Especiais', 'Desp Hospitalar', 'Clinica Especializada', 'Sin Man', 'Ter Inf']
    lista_nv[3] = eventos.index(lista[3]) + 1
    #fouj
    if lista[4] == 'Pessoa Jurídica':
        lista_nv[4] = 0
    else:
        lista_nv[4] = 1
    #cidade
    cid_path = 'municipios.csv'
    municipios_info = pd.read_csv(cid_path)
    
    cid_ddd = municipios_info[['nome','ddd']]
    novo_nome = {'nome':'cid'}
    cid_ddd.rename(columns= novo_nome, inplace=True)
    cid_ddd['cid'] = cid_ddd['cid'].str.upper()
    for city in cid_ddd['cid']:
        if lista[6] == city:
            lista_nv[5] = cid_ddd.loc[cid_ddd['cid'] == city, 'ddd'].values[0]

    #procedimento
    df['proced_num'] = df.DescricaoProced.astype('category').cat.codes
    dicio_proced = df.set_index('proced_num')['DescricaoProced'].to_dict()
    keys = list(dicio_proced.keys())
    values = list(dicio_proced.values())
    for i in range(len(values)):
        if lista[7] == values[i]:
            lista_nv[6] = keys[i]
            break

    #pegar os valores da lista_nv e transformar em uma lista
    r = list(lista_nv.values())
    return r


def main():
    st.set_page_config(page_title='Previsão de Custos', layout='wide')

    df = pd.read_csv('Dados_Para_B2.csv',sep=';')
    
    with st.sidebar:
        st.image('b2 logo.png', width=150)
        st.title('Previsão de Custos')
        selected = option_menu(
            "Menu",
            ["Fazer Previsão", 'Informações'],
            icons=['calculator', 'info'],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "#f0f0f0"},
                "icon": {"color": "orange", "font-size": "25px"},
                "nav-link": {
                    "font-size": "16px",
                    "text-align": "left",
                    "margin": "0px",
                    "--hover-color": "#eee",
                },
                "nav-link-selected": {"background-color": "#02ab21"},
            },
        )

    if selected == 'Fazer Previsão':
        st.title('Fazer Previsão')
        st.subheader('Insira os parâmetros para a previsão')
        parametros = []
        col1, col2 = st.columns(2)
        
        with col1:
            idade = st.number_input('Idade', value=0)
            sexo = st.selectbox('Sexo', ['Masculino', 'Feminino'])
            quantidade = st.number_input('Quantidade', value=1,min_value=1)
            evento = st.selectbox('Evento', ['Evento','Consulta', 'Hon Medico', 'Exame Simples','Exames Especiais', 'Desp Hospitalar', 'Clinica Especializada','Sin Man', 'Ter Inf'])

        with col2:
            fouj = st.selectbox('Pessoa Jurídica ou Física', ['Pessoa Jurídica', 'Pessoa Física'])
            estados = ['SP', 'RJ', 'MG', 'ES', 'PR', 'SC', 'RS', 'AM', 'PA', 'AC', 'RO', 'RR', 'TO', 'MT', 'MS', 'GO', 'DF', 'BA', 'SE', 'AL', 'PE', 'PB', 'RN', 'CE', 'PI', 'MA', 'PA', 'AP']
            #deixar a lista estados em ordem alfabética
            estados.sort()
            uf = st.selectbox('UF', estados)
            cidade = st.text_input('Cidade', value='')
            cidade = cidade.upper()

            if cidade != '' and cidade not in df['CidadePrestador'].unique():
                st.warning('Cidade não encontrada na base de dados')

            procedimento = st.text_input('Procedimento', value='')
            procedimento = procedimento.upper()

            if procedimento != '' and procedimento not in df['DescricaoProced'].unique():
                st.warning('Procedimento não encontrado na base de dados')

        parametros.append(idade)
        parametros.append(sexo)
        parametros.append(quantidade)
        parametros.append(evento)
        parametros.append(fouj)
        parametros.append(uf)
        parametros.append(cidade)
        parametros.append(procedimento)

        

        st.markdown('---')

        if 'previsao' not in st.session_state:
            st.session_state.previsao = False
        load = st.button('Fazer Previsão')
        if load or st.session_state.previsao:
            st.session_state.previsao = True

            X_0 = transform_data(parametros,df)

            #transformar a lista em um array 2D
            X = np.array(X_0).reshape(1,-1)
            
            model = joblib.load('model.pkl')
            prev = model.predict(X)
            st.success('Previsão realizada com sucesso!')
            st.write('O custo do procedimento é de R$ {:.2f}'.format(prev[0]))

        reset = st.button('Fazer Nova Previsão')
        if reset:
            del st.session_state.previsao

    elif selected == 'Informações':
        st.title('Informações sobre o Projeto')
        st.markdown(
            """
            - **Feito por**: [Quanta Júnior](https://quanta.org.br/)
            """
        )
        st.image("Logo Azul Horizontal (1).png", width=400)
        st.markdown(
            """
            - **Modelo Utilizado**: Random Forest
            """
        )
        #explicação do modelo detalhado
        st.write(
            "Para esse projeto utilizamos o modelo Random Forest, que é um algoritmo de aprendizado de máquina usado para tomar decisões e fazer previsões. Ele cria várias \"árvores de decisão\" com base em diferentes partes dos dados e combina suas respostas para obter um resultado final mais preciso e confiável. Isso ajuda a reduzir erros e melhorar a precisão das previsões."
        )

if __name__ == '__main__':
    main()
