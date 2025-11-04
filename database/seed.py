# database/seed.py

from .connection import engine, Base, session
from .models import Usuario, Conta, Categoria, Transacao 
from .functions import criar_usuario, criar_conta, criar_categoria, adicionar_transacao
from .procedures_triggers import criar_procedures_e_triggers
import datetime

def seed_database():
    """
    Cria tabelas, procedures, triggers e insere dados iniciais no banco.
    """
    try:
        print("Iniciando o processo de seed do banco de dados...")


        Base.metadata.create_all(engine)
        print("Tabelas criadas com sucesso (ou já existentes).")


        criar_procedures_e_triggers()


        

        if session.query(Categoria).count() == 0:
            print("Populando categorias básicas...")

            criar_categoria("Alimentação", "Despesa")
            criar_categoria("Transporte", "Despesa")
            criar_categoria("Moradia", "Despesa")
            criar_categoria("Lazer", "Despesa")
            criar_categoria("Saúde", "Despesa")
            criar_categoria("Transferência Saída", "Despesa") 
            

            criar_categoria("Salário", "Receita")
            criar_categoria("Freelance", "Receita")
            criar_categoria("Investimentos", "Receita")
            criar_categoria("Transferência Entrada", "Receita") 
            print("Categorias básicas criadas.")
        else:
            print("Categorias já existem. Pulando...")


        if session.query(Usuario).count() == 0:
            print("Criando usuário de teste...")

            usuario_teste = criar_usuario(
                nome="Julius Rock", 
                email="julius@doisempregos.com", 
                senha_plana="senha123"
            )
            
            if usuario_teste:

                conta1 = criar_conta(
                    id_usuario=usuario_teste.id_usuario,
                    nome_conta="Carteira",
                    tipo_conta="Corrente",
                    saldo_inicial=50.0
                )
            if conta1:
                # (ID da Categoria 1 = Alimentação, 7 = Salário)
                adicionar_transacao(conta1.id_conta, 1, -15.50, "Lanche", "2025-11-01")
                print("Usuário de testes e dados de testes criados")
        else:
            print("Usuários já existem. Pulando...")

        print("\nProcesso de Seed concluído com sucesso!")

    except Exception as e:
        print(f"\nErro durante o processo de seed: {e}")
    finally:
        session.remove()