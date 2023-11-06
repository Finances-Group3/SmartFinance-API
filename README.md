# SmartFinanceAPI

## Instrucciones

Instalar las dependencias con el siguiente comando:

``` bash
pip install fastapi uvicorn sqlalchemy pymysql
```

Tener instalado mysql y revisar el db.py para configurar la conexión a la base de datos.

Para ejecutat el servidor:

``` bash
uvicorn main:app --reload
```

En URL_DATABASE pueden cambiar el puerto, contrasene, usuario y nombre de la base de datos 