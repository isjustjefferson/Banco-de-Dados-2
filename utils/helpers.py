# utils/helpers.py

import bcrypt

def hash_senha(senha_plana):
    """
    Gera um hash seguro para uma senha em texto plano.
    """
    # Converte a senha (string) para bytes
    senha_bytes = senha_plana.encode('utf-8')
    
    # Gera o "sal" e cria o hash
    sal = bcrypt.gensalt()
    hash_gerado = bcrypt.hashpw(senha_bytes, sal)
    
    # Retorna o hash como uma string para salvar no banco
    return hash_gerado.decode('utf-8')

def verificar_senha(senha_plana, hash_armazenado):
    """
    Verifica se a senha em texto plano corresponde ao hash salvo no banco.
    """
    try:
        senha_plana_bytes = senha_plana.encode('utf-8')
        hash_armazenado_bytes = hash_armazenado.encode('utf-8')
        
        # O bcrypt faz a verificação
        return bcrypt.checkpw(senha_plana_bytes, hash_armazenado_bytes)
    except (ValueError, TypeError):
        # Se o hash for inválido ou ocorrer outro erro, retorna Falso
        return False