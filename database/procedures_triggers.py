# database/procedures_triggers.py

from sqlalchemy import text
from .connection import engine

# --- SQL para criar Tabelas de Log/Backup (necessárias para os triggers) ---

SQL_CREATE_LOG_USUARIOS = """
CREATE TABLE IF NOT EXISTS log_atualizacao_usuarios (
    id_log INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT,
    email_antigo VARCHAR(100),
    email_novo VARCHAR(100),
    data_modificacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

SQL_CREATE_CONTAS_BACKUP = """
CREATE TABLE IF NOT EXISTS contas_backup (
    id_conta INT PRIMARY KEY,
    nome_conta VARCHAR(100),
    tipo_conta VARCHAR(50),
    saldo_inicial FLOAT,
    id_usuario INT,
    data_exclusao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""


# --- SQL para os 4 Stored Procedures ---

# SP 1: Atualizar o valor de uma meta
SQL_SP_ATUALIZAR_META = """
CREATE PROCEDURE sp_atualizar_saldo_meta(IN meta_id INT, IN valor_adicionado FLOAT)
BEGIN
    UPDATE metas
    SET valor_atual = valor_atual + valor_adicionado
    WHERE id_meta = meta_id;
END
"""

# SP 2: Calcular gastos totais por categoria em um mês/ano
SQL_SP_GASTOS_CATEGORIA = """
CREATE PROCEDURE sp_calcular_gastos_categoria(
    IN p_id_usuario INT, 
    IN p_id_categoria INT, 
    IN p_mes INT, 
    IN p_ano INT
)
BEGIN
    SELECT 
        c.nome AS categoria,
        SUM(t.valor) AS total_gasto
    FROM transacoes t
    JOIN contas ct ON t.id_conta = ct.id_conta
    JOIN categorias c ON t.id_categoria = c.id_categoria
    WHERE ct.id_usuario = p_id_usuario
      AND t.id_categoria = p_id_categoria
      AND MONTH(t.data) = p_mes
      AND YEAR(t.data) = p_ano
      AND c.tipo = 'Despesa'
    GROUP BY c.nome;
END
"""

# SP 3: Obter todas as transações de uma conta específica
SQL_SP_OBTER_TRANSACOES_CONTA = """
CREATE PROCEDURE sp_obter_transacoes_conta(IN p_id_conta INT)
BEGIN
    SELECT 
        t.id_transacao, 
        t.descricao, 
        t.valor, 
        t.data, 
        c.nome AS categoria
    FROM transacoes t
    JOIN categorias c ON t.id_categoria = c.id_categoria
    WHERE t.id_conta = p_id_conta
    ORDER BY t.data DESC;
END
"""

# SP 4: Registrar uma transferência entre contas
SQL_SP_REGISTRAR_TRANSFERENCIA = """
CREATE PROCEDURE sp_registrar_transferencia(
    IN p_id_conta_origem INT,
    IN p_id_conta_destino INT,
    IN p_valor FLOAT,
    IN p_descricao VARCHAR(255)
)
BEGIN
    DECLARE id_cat_transferencia INT;
    
    -- Assume que existe uma categoria "Transferência" (tipo Despesa)
    -- Para uma implementação robusta, você criaria uma categoria específica
    -- Vamos usar a categoria 10 (genérica) para este exemplo.
    -- O ideal é buscar o ID da categoria "Transferência"
    SET id_cat_transferencia = (SELECT id_categoria FROM categorias WHERE nome = 'Transferência Saída' LIMIT 1);
    
    -- Se não existir, use uma categoria padrão (ex: ID 1, ajuste conforme seu seed)
    IF id_cat_transferencia IS NULL THEN
        SET id_cat_transferencia = 1; 
    END IF;

    -- Inserir transação de débito (saída)
    INSERT INTO transacoes (descricao, valor, data, id_conta, id_categoria)
    VALUES (CONCAT('Transferência para ', p_descricao), -ABS(p_valor), CURDATE(), p_id_conta_origem, id_cat_transferencia);
    
    -- Inserir transação de crédito (entrada)
    SET id_cat_transferencia = (SELECT id_categoria FROM categorias WHERE nome = 'Transferência Entrada' LIMIT 1);
    IF id_cat_transferencia IS NULL THEN
        SET id_cat_transferencia = 2; 
    END IF;
    
    INSERT INTO transacoes (descricao, valor, data, id_conta, id_categoria)
    VALUES (CONCAT('Transferência de ', p_descricao), ABS(p_valor), CURDATE(), p_id_conta_destino, id_cat_transferencia);
END
"""


# --- SQL para os 3 Triggers ---

# Trigger 1: Logar mudança de e-mail de usuário
SQL_TR_LOG_UPDATE_USUARIO = """
CREATE TRIGGER tr_antes_atualizar_email_usuario
BEFORE UPDATE ON usuarios
FOR EACH ROW
BEGIN
    IF OLD.email <> NEW.email THEN
        INSERT INTO log_atualizacao_usuarios (id_usuario, email_antigo, email_novo)
        VALUES (OLD.id_usuario, OLD.email, NEW.email);
    END IF;
END
"""

# Trigger 2: Fazer backup de conta antes de deletar
SQL_TR_BACKUP_DELETE_CONTA = """
CREATE TRIGGER tr_depois_deletar_conta
AFTER DELETE ON contas
FOR EACH ROW
BEGIN
    INSERT INTO contas_backup (id_conta, nome_conta, tipo_conta, saldo_inicial, id_usuario)
    VALUES (OLD.id_conta, OLD.nome_conta, OLD.tipo_conta, OLD.saldo_inicial, OLD.id_usuario);
END
"""

# Trigger 3: Impedir valor inválido na transação (Despesa > 0 ou Receita < 0)
SQL_TR_VALIDAR_VALOR_TRANSACAO = """
CREATE TRIGGER tr_antes_inserir_transacao
BEFORE INSERT ON transacoes
FOR EACH ROW
BEGIN
    DECLARE categoria_tipo VARCHAR(20);
    
    SELECT tipo INTO categoria_tipo 
    FROM categorias 
    WHERE id_categoria = NEW.id_categoria;
    
    IF categoria_tipo = 'Despesa' AND NEW.valor > 0 THEN
        SET NEW.valor = NEW.valor * -1;
    ELSEIF categoria_tipo = 'Receita' AND NEW.valor < 0 THEN
        SET NEW.valor = NEW.valor * -1;
    END IF;
END
"""


# --- Função Python para executar todo o SQL ---

def criar_procedures_e_triggers():
    """
    Executa o SQL puro para criar tabelas de log, procedures e triggers.
    """
    comandos_sql = [
        SQL_CREATE_LOG_USUARIOS,
        SQL_CREATE_CONTAS_BACKUP,
        SQL_SP_ATUALIZAR_META,
        SQL_SP_GASTOS_CATEGORIA,
        SQL_SP_OBTER_TRANSACOES_CONTA,
        SQL_SP_REGISTRAR_TRANSFERENCIA,
        SQL_TR_LOG_UPDATE_USUARIO,
        SQL_TR_BACKUP_DELETE_CONTA,
        SQL_TR_VALIDAR_VALOR_TRANSACAO
    ]
    
    try:
        with engine.connect() as connection:
            print("Iniciando criação de procedures e triggers...")
            
            for i, sql in enumerate(comandos_sql):
                # O MySQL não gosta de 'CREATE PROCEDURE'/'TRIGGER' se já existir.
                # Vamos remover antes de tentar criar.
                # Isso é uma forma simples de garantir que o script rode várias vezes.
                try:
                    if "PROCEDURE" in sql:
                        proc_name = sql.split(" ")[2].split("(")[0]
                        connection.execute(text(f"DROP PROCEDURE IF EXISTS {proc_name}"))
                    elif "TRIGGER" in sql:
                        trigger_name = sql.split(" ")[2]
                        connection.execute(text(f"DROP TRIGGER IF EXISTS {trigger_name}"))
                except Exception as e:
                    # Ignora erro se o item não existir (que é o esperado)
                    pass 
                
                # Executa o comando de criação
                connection.execute(text(sql))
                print(f"  -> Comando {i+1}/{len(comandos_sql)} executado com sucesso.")

            print("Procedures e triggers criados com sucesso!")
            
    except Exception as e:
        print(f"\nErro ao executar SQL puro: {e}")
        print("Verifique a sintaxe SQL e as permissões do usuário 'julius_user'.")
        print("O usuário 'julius_user' precisa de permissão para CREATE ROUTINE e TRIGGER.")