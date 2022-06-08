# django-api-rest

__________________________________________________________________________________

### (Backend)Api run:
##### Pre-requisitos:
- Python **3** ou acima
- pip **20** ou acima
- Virtualenv
- PostgressSQL

## Linux

- sudo apt update
- sudo apt install postgresql postgresql-contrib

1. Faça o login como usuario postgres
- sudo -i -u postgres

2. Acesse o postgress psql
- psql
    para sair basta digitar
- \q
    e finalmente
- exit

### Criando banco de dados e usuario

1. Faça o login como usuario postgres e abrir psql CLI
- sudo -u postgres psql

2. Crie um banco de dados com o seguinte comando contendo o respectivo nome
- create database products;

3. Crie um novo usuário com uma senha com o seguinte comando:
- create user username with encrypted password 'password';

4. Por fim, dê ao usuário todos os privilégios no banco de dados:
- grant all privileges on database products to username;

5. Adicione a permissão createdb ao usuário
- ALTER USER username CREATEDB;

### Rodando o projeto

1. Esteja no diretorio **raiz** do projeto.

2. Inicialize e ative sua maquína virtual:

**Windows:**
- (Cria maquina virtual) Rode o comando -> $ **_python -m venv env_**
- (Inicia maquina virtual) Rode o comando -> $ **_.\env\Scripts\activate_**

**Macos:** 
- (Cria maquina virtual) Rode o comando -> $ **_python -m venv env_**
- (Inicia maquina virtual) Rode o comando -> $ **_source env/bin/activate_**

**Linux:**
- (Cria maquina virtual) Rode o comando -> $ **_virtualenv env_**
- (Inicia maquina virtual) Rode o comando -> $ **_source env/bin/activate_**

3. Instale todas as depedencias e bibliotecas do projeto com o comando:

- **Windowns, MacOs, Linux** -> $ **_pip install -r requirements.txt_**

4. Rode a API com o comando -> $ **_python app/main.py_**

Api Restfull -> [http://127.0.0.1:8000](http://127.0.0.1:8000)

Documentação da API(SWAGGER) -> [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

___________________________________________________________________________________
