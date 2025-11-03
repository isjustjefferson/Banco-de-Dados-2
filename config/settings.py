# config/settings.py

import os

# Define o caminho base do projeto
# Isso é útil para encontrar arquivos como o banco de dados SQLite (se usássemos) ou logs
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Configurações do Banco de Dados MySQL
DB_HOST = "localhost"
DB_NAME = "julius_finance"
DB_USER = "julius_user"
DB_PASS = "senha123"  

# String de Conexão do SQLAlchemy
# Formato: mysql+<driver>://<usuario>:<senha>@<host>/<banco_de_dados>
# Usamos 'mysql+mysqlconnector' porque instalamos 'mysql-connector-python'
DB_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

# Configuração de Logging (opcional, mas bom ter)
LOG_FILE = os.path.join(BASE_DIR, 'logs', 'app.log')