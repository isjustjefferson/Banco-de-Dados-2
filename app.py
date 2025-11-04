import argparse
from database import functions as db_func
from database import seed
from database.connection import session
import sys

def main():
    """Função principal da CLI."""
    

    parser = argparse.ArgumentParser(
        prog="julius_finance",
        description="CLI para Gerenciamento de Finanças Pessoais."
    )
    

    subparsers = parser.add_subparsers(dest="command", help="Comandos disponíveis")


    parser_initdb = subparsers.add_parser(
        "initdb", 
        help="Inicializa o banco de dados (cria tabelas, procs, triggers e dados iniciais)."
    )
    

    parser_adduser = subparsers.add_parser(
        "adduser", 
        help="Adiciona um novo usuário ao sistema."
    )
    parser_adduser.add_argument("nome", type=str, help="Nome completo do usuário.")
    parser_adduser.add_argument("email", type=str, help="E-mail de login (único).")
    parser_adduser.add_argument("senha", type=str, help="Senha de login.")
    

    parser_addtrans = subparsers.add_parser(
        "addtransaction", 
        help="Adiciona uma nova transação (receita ou despesa)."
    )
    parser_addtrans.add_argument("id_conta", type=int, help="ID da conta (origem/destino).")
    parser_addtrans.add_argument("id_categoria", type=int, help="ID da categoria.")
    parser_addtrans.add_argument("valor", type=float, help="Valor da transação (use - para despesa).")
    parser_addtrans.add_argument("descricao", type=str, help="Descrição da transação.")
    parser_addtrans.add_argument(
        "-d", "--data", 
        type=str, 
        help="Data da transação (Formato: AAAA-MM-DD). Opcional, usa hoje se omitido."
    )


    parser_getbalance = subparsers.add_parser(
        "getbalance", 
        help="Calcula e exibe o balanço total de um usuário."
    )
    parser_getbalance.add_argument("id_usuario", type=int, help="ID do usuário para calcular o balanço.")

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        return

    args = parser.parse_args()

 
    try:
        if args.command == "initdb":
            print("Executando comando 'initdb'...")
            seed.seed_database()
            
        elif args.command == "adduser":
            print(f"Executando 'adduser' para: {args.email}...")
            db_func.criar_usuario(args.nome, args.email, args.senha)
            
        elif args.command == "addtransaction":
            print(f"Executando 'addtransaction' de R${args.valor}...")
            db_func.adicionar_transacao(
                id_conta=args.id_conta,
                id_categoria=args.id_categoria,
                valor=args.valor,
                descricao=args.descricao,
                data_str=args.data 
            )
            
        elif args.command == "getbalance":
            print(f"Executando 'getbalance' para usuário {args.id_usuario}...")
            db_func.calcular_balanco_usuario(args.id_usuario)
            
        else:
            parser.print_help(sys.stderr)
            
    except Exception as e:
        print(f"\nOcorreu um erro durante a execução: {e}")
        session.rollback() 
    finally:

        db_func.fechar_sessao()
        print("Sessão do banco fechada.")



if __name__ == "__main__":
    main()