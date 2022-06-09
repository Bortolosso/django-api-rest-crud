__________________________________________________________________________________
### Django Rest-Framework CRUD, Authentication, Filters:
##### Pré-requisitos:
- Python **3** ou versão maior
- pip **20** ou versão maior
- Virtualenv
- PostgressSQL

##### Linux
- $ _sudo apt update_
- $ _sudo apt install postgresql postgresql-contrib_

1. ###### Faça o login como usuário postgressSQL:
- $ _sudo -i -u postgres_
- $ _psql_
- $ _\q_
- $ _exit_
#### Criando banco de dados e usuário

1. ###### Faça o login como usuário postgressSQL e abrir psql CLI:
- $ _sudo -u postgres psql_
2. ###### Crie um banco de dados com o seguinte comando contendo o respectivo nome:
- $ _create database products;_
3. ###### Crie um novo usuário com uma senha com o seguinte comando:
- $ _create user username with encrypted password 'password';_
4. ###### Por fim, dê ao usuário todos os privilégios no banco de dados:
- $ _grant all privileges on database products to username;_
5. ###### Adicione a permissão createdb ao usuário para rodar os testes:
- $ _ALTER USER username CREATEDB;_

#### Rodando o projeto
1. ###### Esteja no diretorio **raiz** do projeto.
2 .###### Inicialize e ative sua maquína virtual:

**Linux:**
1. Criar maquina virtual -> $ _virtualenv env_
2. Iniciar maquina virtual -> $ _source env/bin/activate_

3. ###### Instale todas as depedencias e bibliotecas do projeto com o comando:
- $ _pip install -r requirements.txt_
- $ _python manage.py runserver_

- Api Restfull -> [http://127.0.0.1:8000](http://127.0.0.1:8000)
- Documentação da API(SWAGGER) -> [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

- Rode os testes com o comando -> $ _python manage.py test_

1. ###### Crie um super-usuario para se autenticar e utilizar os serviços da API
- ###### Obs: essa aplicação usa o metodo **Basic Auth** 
- $ _python manage.py createsuperuser_

### Endpoints
##### Products:

**POST** _http://localhost:8000/api/v1/products/_
###### Body
```sh
{
    "name": "Camiseta Polo",
    "unity_value": 450,
    "quantity_product": 10
}
```

###### Retorna todos os PRODUTOS:
**GET** _http://localhost:8000/api/v1/products/_

###### Retorna os PRODUTOS com o filtro Disponivel ou Indisponivel com o parametro **status** na URL:
**GET** _http://localhost:8000/api/v1/products/?status=Indisponivel_

**GET by ID** _http://localhost:8000/api/v1/products/**id**_

**DELETE by ID** _http://localhost:8000/api/v1/products/**id**_

**PUT by ID** _http://localhost:8000/api/v1/products/**id**_
###### Body
```sh
{
    "name": "Camiseta Polo",
    "unity_value": 450,
    "quantity_product": 10
}
```

___________________________________________________________________________________
