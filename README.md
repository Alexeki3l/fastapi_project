Ejecución

Ejecutar el docker compose con todo el ecosistema(aplicacion con base de datos y gestor de base de datos).

```
$ docker-compose up --build
```

Ejecucion de la aplicacion.
```
$ uvicorn app.main:app --reload  
```

Documentacion:
```
http://localhost:8000/redoc
```

y

```
http://localhost:8000
```
