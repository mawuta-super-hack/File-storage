### File-storage - файловое хранилище, которое позволяет хранить различные типы файлов — документы, фотографии, другие данные.

### Возможности API:


1. Статус активности связанных сервисов.

    ```
    GET /ping
    ```


2. Регистрация пользователя.

    ```
    POST /register
    ```


3. Авторизация пользователя.

    ```
    POST /auth
    ```


4. Информация о загруженных файлах.

    ```
    GET /files/
    ```

5. Загрузить файл в хранилище.

    ```
    POST /files/upload
    ```

6. Скачать загруженный файл.

    ```
    GET /files/download
    ```
 

### Пример наполнения .env-файла:
```
DATABASE_DSN=postgresql+asyncpg://postgres:postgres@db:5432/collection
POSTGRES_PASSWORD=postgres
POSTGRES_USER=postgres
POSTGRES_DB=collection
POSTGRES_HOST=db
DOCKER_API_PORT=8000
DOCKER_DB_PORT=5432
```

### Описание команд для запуска приложения локально:

Клонирование репозитория и переход в него в командной строке:

```
git clone https://git@github.com:mawuta-super-hack/File-storage.git
```

```
cd ./src
```


Установка и активация виртуального окружения:

```
python -m venv env
```

```
source venv/Scripts/activate
```


Установка зависимостей из файла requirements.txt:
```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```


Запуск сервера:
```
docker-compose up -d --build
```

Полный список эндпоинтов описан в документации.
Документация доступна после запуска проекта по [адресу](http://127.0.0.1:8080/api/openapi).


Автор проекта:
<br>
Клименкова Мария [Github](https://github.com/mawuta-super-hack)<br>

