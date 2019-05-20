## Запуск
```
docker-compose up --build
```

## Запуск тестов
из контейнера:
```
python -m pytest tests/
```

через докер:
```
docker-compose run --rm app make test
docker-compose run --rm app make test arg="-k test_some_name"
```

## Эндпоинты
Получение списка серверов.
 * Возможные GET параметры:
   - sortByFate - Опционально. Вернуть отсортирвоанным по дате
   - includeDeleted - Опционально. Включить сервера в статусе Deleted
 * Возвращает список серверов
```
GET 0.0.0.0:8000/api/v1/servers
```

Создание сервера
 * Возвращает id созданного сервера
```
POST 0.0.0.0:8000/api/v1/servers
```

Изменение статуса
 * Возвращает id созданного сервера
 * Вернёт ok если успешно, иначе ошибку
 * Возможные параметры:
  - action - Обязательно, в нём действие над сервером. Возможное действие pay
  При action pay ожидается следующий параметр:
   - expirationDate - таимстамп времени отключения
```
PUT 0.0.0.0:8000/api/v1/servers/server_id
```

Удаление сервера
  * Вернёт ok если успешно, иначе ошибку
 ```
DELETE 0.0.0.0:8000/api/v1/servers/server_id
```

Получение списка стоек.
 * Возможные GET параметры:
   - sortByFate - Опционально. Вернуть отсортирвоанным по дате
   - includeDeleted - Опционально. Включить сервера в статусе Deleted
 * Возвращает список серверов
```
GET 0.0.0.0:8000/api/v1/serverRacks
```

Создание сервера
 * Возвращает id созданной стойки
```
POST 0.0.0.0:8000/api/v1/serverRacks
```

Добавление/удаление серверов в стойку
 * Возвращает id созданного сервера
 * Вернёт ok если успешно, иначе ошибку
 * Возможные параметры:
  - action - Обязательно, в нём действие над сервером. Возможное действия add-server и remove-server
  - server_id - ид сервера который надо переместить
```
PUT 0.0.0.0:8000/api/v1/serverRacks/server_id
```

Удаление стойки
  * Вернёт ok если успешно, иначе ошибку
 ```
DELETE 0.0.0.0:8000/api/v1/serverRacks/server_rack_id
```

##Примеры

Получение списка всех серверов

```
curl -X GET 0.0.0.0:8000/api/v1/servers
```

Ответ

```
{"result":[{"created":"Fri, 17 May 2019 00:54:21 GMT","id":1,"modified":"Fri, 17 May 2019 00:57:18 GMT","serverRackId":1,"status":"Unpaid"}]}
```

Получение списка всех серверов

```
curl -X POST 0.0.0.0:8000/api/v1/servers
```

Ответ

```
{"result":[{"created":"Fri, 17 May 2019 00:54:21 GMT","id":1,"modified":"Fri, 17 May 2019 00:57:18 GMT","serverRackId":1,"status":"Unpaid"}]}
```

Создание сервера

```
curl -X POST 0.0.0.0:8000/api/v1/servers
```

Ответ

```
{"result":{"id":25}}
```

Перевод в Deleted

```
curl -X DELETE 0.0.0.0:8000/api/v1/servers/25
```

Ответ

```
{"result":"ok"}
```

Создание стойки на 20 серверов

```
curl -X POST --header "Content-Type: application/json"  0.0.0.0:8000/api/v1/serverRacks --data '{"isBig":true}' 
```

Ответ

```
{"result":{"id":52}}
```

Добавление сервера в стойку

```
curl -X PUT --header "Content-Type: application/json"  0.0.0.0:8000/api/v1/serverRacks/52 --data '{"action":"add-server","serverId":24}'
```

Ответ

```
{"result":"ok"}
```

Удаление сервера из стойки

```
curl -X PUT --header "Content-Type: application/json"  0.0.0.0:8000/api/v1/serverRacks/52 --data '{"action":"remove-server","serverId":24}'
```

Ответ

```
{"result":"ok"}
```