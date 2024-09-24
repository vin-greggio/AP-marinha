import streamlit as st
import hashlib
import json
import os
import pandas as pd
from PyPDF2 import PdfFileReader
import matplotlib.pyplot as plt
import matplotlib
import plotly.express as px
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

fig = px.bar(df.sort_values('Saldo'), x='CONDOMINIO',y='Saldo', color='CONDOMINIO')
fig.show()