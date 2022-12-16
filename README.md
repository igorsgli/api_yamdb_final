### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/igorsgli/api_yamdb_final.git
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

```
venv\Scripts\activate
```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

Примеры запросов:

1. Получение списка произведений

```
GET /api/v1/titles/

[
    {
        "count": 0,
        "next": "string",
        "previous": "string",
        "results": [
        {
            "id": 0,
            "name": "string",
            "year": 0,
            "rating": 0,
            "description": "string",
            "genre": [
                {
                    "name": "string",
                    "slug": "string"
                }
            ],
            "category": {
                    "name": "string",
                    "slug": "string"
                }
            }
        ]
    }
]
```

2. Добавление произведения

```
POST http://127.0.0.1:8000/api/v1/titles/

{
    "name": "string",
    "year": 0,
    "description": "string",
    "genre": [
        "string"
    ],
    "category": "string"
}
```

3. Получение списка отзывов

```
GET http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/

[
    {
        "count": 0,
        "next": "string",
        "previous": "string",
        "results": [
            {
                "id": 0,
                "text": "string",
                "author": "string",
                "score": 1,
                "pub_date": "2019-08-24T14:15:22Z"
            }
        ]
    }
]
```

4. Добавление отзыва

```
POST http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/

{
  "text": "string",
  "score": 1
}
```

5. Получение списка комментариев по отзыву

```
GET http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/

[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "id": 0,
        "text": "string",
        "author": "string",
        "pub_date": "2019-08-24T14:15:22Z"
      }
    ]
  }
]
```

6. Добавление комментария к отзыву

```
POST http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/

{
    "text": "string"
}
```

7. Регистрация нового пользователя

```
POST http://127.0.0.1:8000/api/v1/auth/signup/

{
  "email": "string",
  "username": "string"
}
```

8. Получение токена

```
POST http://127.0.0.1:8000/api/v1/auth/token/

{
  "username": "string",
  "confirmation_code": "string"
}
```

Более подробнее можно ознакомиться в документации: /static/redoc.yaml