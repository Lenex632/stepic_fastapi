У себя проек собирал через uv с python3.14, поэтому нужно было отдельно прописывать некоторые зависимости\
Всё должно быть в requirements.txt, так что и через обычный venv должно сработать


[.env]
есть штуки, которые я добавил в .env, для работы шифрования, авторизации и тд.


[alembic]
```
alembic revision --autogenerate -m "message"
alembic upgrade head
```

[celery]
```
celery -A celery_main.celery worker --loglevel=info
```
