# PokeAPI

Создайте в корне проекта файл .env и запишите в нем:
```
POSTGRES_USER=myuser
POSTGRES_PASSWORD=mypassword
POSTGRES_DB=myapp_db
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

Для запуска нужно собрать контейнера:
```
sudo docker compose build
```
и запустить
```
sudo docker compose up
```