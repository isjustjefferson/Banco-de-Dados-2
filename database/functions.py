
from .connection import session 
from .models import Usuario, Conta, Categoria, Transacao, Tag
from utils.helpers import hash_senha, verificar_senha 
from sqlalchemy.orm import joinedload
from sqlalchemy import func
import datetime



def criar_usuario(nome, email, senha_plana):
    """Cria um novo usuário com senha hasheada."""
    try:
        
        if session.query(Usuario).filter_by(email=email).first():
            print(f"Erro: E-mail '{email}' já cadastrado.")
            return None
            
        
        senha_hasheada = hash_senha(senha_plana)
        
        
        novo_usuario = Usuario(
            nome=nome,
            email=email,
            senha_hash=senha_hasheada
        )
        
        
        session.add(novo_usuario)
        session.commit()
        
        print(f"Usuário '{nome}' criado com sucesso (ID: {novo_usuario.id_usuario}).")
        return novo_usuario
        
    except Exception as e:
        session.rollback() 
        print(f"Erro ao criar usuário: {e}")
        return None

def criar_conta(id_usuario, nome_conta, tipo_conta, saldo_inicial=0.0):
    """Cria uma nova conta para um usuário."""
    try:
        nova_conta = Conta(
            id_usuario=id_usuario,
            nome_conta=nome_conta,
            tipo_conta=tipo_conta,
            saldo_inicial=saldo_inicial
        )
        session.add(nova_conta)
        session.commit()
        print(f"Conta '{nome_conta}' criada para o usuário ID {id_usuario}.")
        return nova_conta
    except Exception as e:
        session.rollback()
        print(f"Erro ao criar conta: {e}")
        return None

def criar_categoria(nome, tipo):
    """Cria uma nova categoria (Receita ou Despesa)."""
    try:
        nova_categoria = Categoria(nome=nome, tipo=tipo)
        session.add(nova_categoria)
        session.commit()
        print(f"Categoria '{nome}' ({tipo}) criada.")
        return nova_categoria
    except Exception as e:
        session.rollback()
        print(f"Erro ao criar categoria: {e}")
        return None

def adicionar_transacao(id_conta, id_categoria, valor, descricao, data_str=None):
    """Adiciona uma nova transação (receita ou despesa)."""
    try:
        
        if data_str:
            data = datetime.datetime.strptime(data_str, '%Y-%m-%d').date()
        else:
            data = datetime.date.today()
            
        nova_transacao = Transacao(
            id_conta=id_conta,
            id_categoria=id_categoria,
            valor=valor,
            descricao=descricao,
            data=data
        )
        session.add(nova_transacao)
        session.commit()
        print(f"Transação de R${valor:.2f} ('{descricao}') adicionada.")
        return nova_transacao
    except Exception as e:
        session.rollback()
        print(f"Erro ao adicionar transação: {e}")
        return None

def calcular_balanco_usuario(id_usuario):
    """
    Calcula o balanço total de um usuário somando os saldos 
    de todas as suas contas e o valor de todas as transações.
    """
    try:
        
        saldo_inicial_total = session.query(func.sum(Conta.saldo_inicial))\
                                     .filter(Conta.id_usuario == id_usuario)\
                                     .scalar() or 0.0

       
        soma_transacoes = session.query(func.sum(Transacao.valor))\
                                 .join(Conta)\
                                 .filter(Conta.id_usuario == id_usuario)\
                                 .scalar() or 0.0

        balanco_total = saldo_inicial_total + soma_transacoes
        
        print(f"Balanço total do Usuário ID {id_usuario}: R${balanco_total:.2f}")
        return balanco_total
        
    except Exception as e:
        print(f"Erro ao calcular balanço: {e}")
        return None


def fechar_sessao():
    session.remove()