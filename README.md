# Teste Codigo

Para executar o teste

+ Inicie o venv
    + python -m venv teste
    + source ./teste/bin/activate

+ Instale as dependencias
    + pip install -r requirements.txt

+ Execute o software
    + FLASK_APP=teste.py flask run

+ teste o software
    + curl http://localhost:5000/properties/1
    + curl -v -XPOST http://localhost:5000/properties/ -H 'Content-Type: application/json' -d @json_de_criacao
    + curl 'http://localhost:5000/properties/?ax=100&bx=120&ay=957&by=1000'
