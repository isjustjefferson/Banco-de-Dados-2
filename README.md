# Banco-de-Dados-2
Repositório referente as atividades da disciplina de Banco de Dados 2 no curso de Análise e Desenvolvimento de Sistemas no IFPE - Campus Paulista, ministrada pelo prof. Antônio.

Para testar o projeto, siga os seguintes passos:

1 - Certifique-se que está utilizando uma versão Python 3.10+:

    python --version
    
-------------------------------------------------

Caso seja usuário Windows:

2 - Instale o MySQL Server no link: 

    https://dev.mysql.com/downloads/installer/

3 - No MySQL Workbench, execute o seguinte script: 
    
    CREATE DATABASE julius_finance;
    CREATE USER 'julius_user'@'localhost' IDENTIFIED BY 'senha_forte';
    GRANT ALL PRIVILEGES ON julius_finance.* TO 'julius_user'@'localhost';
    FLUSH PRIVILEGES;

4 - Instale o pacote:

    pip install SQLAlchemy PyMySQL

Caso ocorra algum erro de permissão, tente: 

    pip install SQLAlchemy PyMySQL --user

-------------------------------------------------

Caso seja usuário Linux:

2 - Instale o MySQL Server:

    sudo apt update
    sudo apt install mysql-server

3 - Ative o MySQL Server: 

    sudo systemctl enable mysql

4 - Configure o MySQL:

    #use y para todos os pedidos
    sudo mysql_secure_installation

5 - Acesse o MySQL: 

    sudo mysql -u root -p

6 - Crie o banco de dados (o script é o mesmo que o do usuário windows):

    CREATE DATABASE julius_finance;
    CREATE USER 'julius_user'@'localhost' IDENTIFIED BY 'senha_forte';
    GRANT ALL PRIVILEGES ON julius_finance.* TO 'julius_user'@'localhost';
    FLUSH PRIVILEGES;
    EXIT;

7 - Instale dependências Python:

    pip install sqlalchemy pymysql

Caso apareça um erro de permissão (como PEP 668) use o parâmetro "--break-system-packages": 

    pip install SQLAlchemy PyMySQL --break-system-packages
