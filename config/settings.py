import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DB_HOST = "localhost"
DB_NAME = "julius_finance"
DB_USER = "Seu_user" #Deve colocar o seu USER (Geralmente "root")
DB_PASS = "Sua_Senha" #Deve colocar a sua senha do Banco de Dados 

DB_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

LOG_FILE = os.path.join(BASE_DIR, 'logs', 'app.log')