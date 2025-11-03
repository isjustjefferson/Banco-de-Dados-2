# database/seed.py

from .connection import engine, Base, session
from .models import Usuario, Conta, Categoria, Transacao # Importamos os modelos
from .functions import criar_usuario, criar_conta, criar_categoria, adicionar_transacao
from .procedures_triggers import criar_procedures_e_triggers
import datetime

def seed_database():
    """
    Cria tabelas, procedures, triggers e insere dados iniciais no banco.
    """
    try:
        print("Iniciando o processo de seed do banco de dados...")

        # --- 1. Criar todas as tabelas ---
        # Base.metadata.drop_all(engine) # Descomente para deletar tudo e recomeçar
        Base.metadata.create_all(engine)
        print("Tabelas criadas com sucesso (ou já existentes).")

        # --- 2. Criar Stored Procedures e Triggers ---
        # (A função já imprime seu próprio progresso)
        criar_procedures_e_triggers()

        # --- 3. Popular com dados iniciais (se necessário) ---
        
        # Verifica se as categorias já existem antes de criar
        if session.query(Categoria).count() == 0:
            print("Populando categorias básicas...")
            # Categorias de Despesa
            criar_categoria("Alimentação", "Despesa")
            criar_categoria("Transporte", "Despesa")
            criar_categoria("Moradia", "Despesa")
            criar_categoria("Lazer", "Despesa")
            criar_categoria("Saúde", "Despesa")
            criar_categoria("Transferência Saída", "Despesa") # Importante para SP
            
            # Categorias de Receita
            criar_categoria("Salário", "Receita")
            criar_categoria("Freelance", "Receita")
            criar_categoria("Investimentos", "Receita")
            criar_categoria("Transferência Entrada", "Receita") # Importante para SP
            print("Categorias básicas criadas.")
        else:
            print("Categorias já existem. Pulando...")

        # Verifica se já existe algum usuário antes de criar
        if session.query(Usuario).count() == 0:
            print("Criando usuário de teste...")
            # Criar usuário de teste
            usuario_teste = criar_usuario(
                nome="Julius Rock", 
                email="julius@doisempregos.com", 
                senha_plana="senha123"
            )
            
            if usuario_teste:
                # Criar contas para o usuário de teste
                conta1 = criar_conta(
                    id_usuario=usuario_teste.id_usuario,
                    nome_conta="Carteira",
                    tipo_conta="Corrente",
                    saldo_inicial=50.0
                )
                
                conta2 = criar_conta(
                    id_usuario=usuario_teste.id_usuario,
                    nome_conta="Banco Principal",
                    tipo_conta="Corrente",
                    saldo_inicial=1000.0
                )
                
                # Adicionar transações de exemplo
                if conta1 and conta2:
                    # (ID da Categoria 1 = Alimentação, 7 = Salário)
                    adicionar_transacao(conta1.id_conta, 1, -15.50, "Lanche", "2025-11-01")
                    adicionar_transacao(conta2.id_conta, 7, 3000.00, "Salário", "2025-11-05")
                    print("Usuário de teste e dados iniciais criados.")
        else:
            print("Usuários já existem. Pulando...")

        print("\nProcesso de Seed concluído com sucesso!")

    except Exception as e:
        print(f"\nErro durante o processo de seed: {e}")
    finally:
        session.remove()