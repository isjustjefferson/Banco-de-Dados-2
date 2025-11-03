# Projeto Julius Finance (Banco de Dados 2)

Repositório referente as atividades da disciplina de Banco de Dados 2 no curso de Análise e Desenvolvimento de Sistemas no IFPE - Campus Paulista, ministrada pelo prof. Antônio.

Este é um projeto de CLI (Command Line Interface) para gerenciamento de finanças pessoais, utilizando Python, SQLAlchemy e MySQL.

### Tecnologias Utilizadas
* Python 3.10+
* SQLAlchemy (ORM)
* MySQL (Banco de Dados Relacional)
* mysql-connector-python (Driver)
* bcrypt (Hash de Senhas)

---

## Requisitos
Para rodar este projeto, você precisará ter instalados:
1.  [Python 3.10+](https://www.python.org/downloads/)
2.  [Git](https://git-scm.com/downloads/)
3.  [MySQL Server](https://dev.mysql.com/downloads/installer/) (Recomendamos o MySQL Workbench para facilitar)

---

## 1. Configuração do Banco de Dados

Antes de rodar o script, você precisa criar o banco de dados e o usuário que a aplicação irá usar.

1.  Abra seu cliente MySQL (MySQL Workbench, DBeaver, etc.) como **usuário root**.
2.  Execute o script SQL abaixo. Ele fará o seguinte:
    * Cria o banco `julius_finance`.
    * Cria o usuário `julius_user` (com a senha `senha123`).
    * Dá as permissões que a aplicação precisa (incluindo para criar Procedures e Triggers).

```sql
CREATE DATABASE julius_finance;

CREATE USER 'julius_user'@'localhost' IDENTIFIED BY 'senha123';

/* Dá permissões básicas */
GRANT ALL PRIVILEGES ON julius_finance.* TO 'julius_user'@'localhost';

/* Dá permissões para criar e executar Procedures e Triggers (Requisito da Atividade) */
GRANT CREATE ROUTINE, ALTER ROUTINE ON julius_finance.* TO 'julius_user'@'localhost';
GRANT TRIGGER ON julius_finance.* TO 'julius_user'@'localhost';

FLUSH PRIVILEGES;
