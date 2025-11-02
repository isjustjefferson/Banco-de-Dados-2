# Banco-de-Dados-2
Repositório referente as atividades da disciplina de Banco de Dados 2 no curso de Análise e Desenvolvimento de Sistemas no IFPE - Campus Paulista, ministrada pelo prof. Antônio.

Para testar o projeto, siga os seguintes passos:
Caso seja usuário Windows instale o MySQL Server no seguinte link: https://dev.mysql.com/downloads/installer/
No MySQL Workbench, execute o seguinte script: 
    CREATE DATABASE julius_finance;
    CREATE USER 'julius_user'@'localhost' IDENTIFIED BY 'senha_forte';
    GRANT ALL PRIVILEGES ON julius_finance.* TO 'julius_user'@'localhost';
    FLUSH PRIVILEGES;
