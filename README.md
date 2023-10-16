# File processing app

```Python```, ```Django```,  ```DRF```, ```Node```

## Docker
из корневой директории  
```docker-compose up --build ```
откройте новый терминал и запустить 
```docker ps ```
Захватить идентификатор контейнера file_web
после этого запускаем команду

```docker exec -it file_web_id /bin/sh ```
после этого запускаем команду
```celery -A base worker --loglevel=info ```

Также можно запускать тесты
```pytest ```
## Backend

```cd FileProcessor ```

```pip install --upgrade pip```

```pip install pipenv```

```pipenv install```

```pipenv shell```

```python manage.py runserver```



## Frontend


```cd front ```

```npm i ```

```npm start ```


## License

[MIT](https://choosealicense.com/licenses/mit/)# file
