import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv('meme.env')

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

user = supabase.auth.sign_in_with_password({ "email": 'vinicius.greggio@gmail.com', "password": 'Coxinha!1809' })

data = supabase.table("restituicoes").select('*').execute()
print(data)
