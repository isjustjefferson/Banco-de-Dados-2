

import bcrypt

def hash_senha(senha_plana):
    """
    Gera um hash seguro para uma senha em texto plano.
    """

    senha_bytes = senha_plana.encode('utf-8')
    

    sal = bcrypt.gensalt()
    hash_gerado = bcrypt.hashpw(senha_bytes, sal)
    

    return hash_gerado.decode('utf-8')

def verificar_senha(senha_plana, hash_armazenado):
    """
    Verifica se a senha em texto plano corresponde ao hash salvo no banco.
    """
    try:
        senha_plana_bytes = senha_plana.encode('utf-8')
        hash_armazenado_bytes = hash_armazenado.encode('utf-8')
        

        return bcrypt.checkpw(senha_plana_bytes, hash_armazenado_bytes)
    except (ValueError, TypeError):
 
        return False