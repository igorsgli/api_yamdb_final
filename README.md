### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/TimurKhasanov72/api_yamdb.git
```

```
cd yatube_api
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

1. Получаем список произведений

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


2. Создание публикации

```

```

```

```

Более подробнее можно ознакомиться в документации: /static/redoc.yaml