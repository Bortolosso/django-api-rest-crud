__________________________________________________________________________________
### Django Rest-Framework CRUD, Authentication, Filters:
##### Pré-requisitos:
- Python **3** ou versão maior
- pip **20** ou versão maior
- Virtualenv
- PostgressSQL

##### Linux
1. ###### Rode os seguintes comandos:
- $ _sudo apt update_
- $ _sudo apt install postgresql postgresql-contrib_
2. ###### Faça o login como usuário postgressSQL:
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
2. ###### Inicialize e ative sua maquína virtual:
**Linux:**
1. Criar maquina virtual:
- $ _virtualenv env_
2. Iniciar maquina virtual: 
- $ _source env/bin/activate_
3. ###### Instale todas as depedencias e bibliotecas do projeto com o comando:
- $ _pip install -r requirements.txt_
- $ _python manage.py runserver_
4. ###### Api Restfull: 
- [http://127.0.0.1:8000](http://127.0.0.1:8000)
5. ###### Documentação da API(SWAGGER):
- [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
6. ###### Rode os testes automatizados com o comando:  
- $ _python manage.py test_
1. ###### Crie um super-usuario para se autenticar e utilizar os serviços da API
- ###### Obs: essa aplicação usa o metodo **Basic Auth** 
- $ _python manage.py createsuperuser_
### Endpoints
##### Products:
###### Retorna todos os PRODUTOS:
**GET** _http://localhost:8000/api/v1/products/_
###### Retorna os PRODUTOS com os filtros "Disponivel" ou "Indisponivel" com o parametro "status" na URL:
**GET** _http://localhost:8000/api/v1/products/?param=filter_

**POST** _http://localhost:8000/api/v1/products/_
###### Body exemplo:
```sh
{
    "name": "Camiseta Polo Branca",
    "unity_value": 450,
    "quantity_product": 10
}
```

**GET by ID** _http://localhost:8000/api/v1/products/id_

**DELETE by ID** _http://localhost:8000/api/v1/products/id_

**PUT by ID** _http://localhost:8000/api/v1/products/id_
###### Body exemplo:
```sh
{
    "name": "Camiseta Polo Preta",
    "unity_value": 450,
    "quantity_product": 10
}
```

___________________________________________________________________________________

##### Request/Solicitação de pedidos de produtos:
###### Retorna todos os PEDIDOS:
**GET** _http://localhost:8000/api/v1/request/products/_
###### Retorna os PRODUTOS com os filtros "Pendente", "Enviado" e "Entregue" com o parametro "order_status" na URL:
**GET** _http://localhost:8000/api/v1/request/products/?param=filter_

**POST** _http://localhost:8000/api/v1/request/products/_
###### Body exemplo:
```sh
{
    "product":"Camiseta da Juventus",
    "unity_value_request":500,
    "quantity_product_request":40,
    "requester":"User",
    "forwarding_agent":"Correios",
    "address":"Avenida Paulista, 4093 São Paulo-SP",
    "order_status":"Enviado"
}
```

**GET by ID** _http://localhost:8000/api/v1/request/products/id_

**DELETE by ID** _http://localhost:8000/api/v1/request/products/id_

___________________________________________________________________________________

###### Considerações finais:
Esse sistema segue um fluxo aonde precisa ser cadastrado um **produto** antes de solicitar um **pedido** para vizualizar todo o funcionamento dos respectivos CRUD.