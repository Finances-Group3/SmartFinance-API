# SmartFinanceAPI

## Instrucciones

Crear un entorno virtual para el proyecto:

``` bash
python -m venv venv
```

Activar el entorno virtual:

``` bash
venv\Scripts\activate
```

Se puede desactivar con:
```bash
venv\Scripts\deactivate
```
Crear una archivo .env y agregar las credenciales como se requiera

Instalar las dependencias con el siguiente comando:

``` bash
pip install -r requirements.txt
```

Para ejecutar el servidor:

``` bash
uvicorn main:app --reload
```
