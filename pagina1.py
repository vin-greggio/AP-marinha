import pandas as pd
import streamlit as st
from PyPDF2 import PdfFileReader

xls = pd.ExcelFile('big planilha.xlsx')
planilha = st.selectbox('Selecione a planilha desejada', ['BP_Pagamento','Condomínio Papem', 'Taxa_de_Condomínio', 'Despesas', 'ReceitasxDespesas', 'Previsão orçamentaria', 'Taxa complementar',
                                                          'Empréstimo'])
df = pd.read_excel('big planilha.xlsx', sheet_name=planilha)
df = st.data_editor(df, num_rows='dynamic')

if planilha == 'Condomínio Papem':
    pdf_ata = st.file_uploader('Coloque aqui o arquivo PDF (ata)')
    if pdf_ata == None:
        st.write('Arquivo ainda não selecionado')
    else:
        try:
          with open(pdf_ata) as input_pdf:
            pdf_reader = PdfFileReader(input_pdf)
          if pdf_reader == False:
              st.write('Arquivo ainda não selecionado')
          else:
            pdf_reader
        except:
           st.warning('Arquivo não compatível')



