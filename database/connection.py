# database/connection.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from config.settings import DB_URL  # Importa nossa string de conexão

# 1. Engine (Motor)
# A 'engine' é o ponto de entrada principal para o banco de dados.
# Ela gerencia as conexões com o banco.
# echo=False desliga os logs SQL no terminal. Mude para True se quiser ver as queries.
engine = create_engine(DB_URL, echo=False)

# 2. Base Declarativa
# Esta é uma classe base da qual todos os nossos modelos (tabelas) irão herdar.
Base = declarative_base()

# 3. Session (Sessão)
# A 'session' é a nossa "área de trabalho" para interagir com o banco.
# Nós criamos uma 'fábrica' de sessões (sessionmaker) ligada à nossa engine.
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Usamos scoped_session para garantir que cada thread tenha sua própria sessão,
# o que é uma boa prática para evitar problemas de concorrência.
# No nosso caso de CLI simples, não é estritamente necessário, mas é robusto.
session = scoped_session(SessionLocal)