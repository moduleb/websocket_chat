![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) 
![FastAPI](https://img.shields.io/badge/FastAPI-%0c584b?style=for-the-badge&logo=fastapi&logoColor=white) 
![Aiogram](https://img.shields.io/badge/Aiogram-white?style=for-the-badge&logo=chatbot&color=%234796EC) 
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white) 
![Nginx](https://img.shields.io/badge/nginx-009639?style=for-the-badge&logo=nginx) 
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white) 
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-black?style=for-the-badge&logo=sqlalchemy&logoColor=red) 
![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white) 
![Celery](https://img.shields.io/badge/celery-%23a9cc54.svg?style=for-the-badge&logo=celery&logoColor=ddf4a4)

# ICQ 2024
#### Сервис для обмена мгновенными сообщениями между пользователями в реальном времени.

**Компоненты:**
- Веб-приложение: => FastAPI
- Веб-сервер: => Nginx
- База данных: => PostgreSQL
- Очередь задач и кеширование: => Redis
- Телеграм-бот: => Aiogram 3
- Менеджер задач: => Celery
- Управление миграциями: => Alembic

**Возможности:**
1. Регистрация и аутентификация пользователей.
2. Отправка и получение сообщений:
   - Пользователи могут отправлять сообщения друг другу в реальном времени через WebSocket соединение.
3. Сохранение истории сообщений:
   - Все сообщения сохраняются в базе данных.
   - При выборе чата с определенным участником пользователь видит историю переписки между ними.
4. Telegram-бот:
   - Бот уведомляет пользователя о новом сообщении, если он офлайн (нужно указать Telegram ID при регистрации).
   - Возможность получить свой ID при выполнениее команды /start в боте.
5. Веб-интерфейс для тестирования:
   - Возможность тестировать приложение через веб-страницу.
   - Веб-интерфейс реализован на JS, CSS, HTML.
6. Документация:
   - Доступна интерактивная документация Swagger по адресу /docs

**Технические подробности:**
- Язык программирования: Python 3.12.
- Фреймворк: FastAPI для RESTful API.
- Асинхронность:
   - Используются `async/await` для обработки запросов.
   - Реальное время реализовано с помощью WebSockets.
   - Используются асинхронный драйвер базы данных asyncpg.
- Базы данных:
   - PostgreSQL для хранения пользователей и сообщений.
   - Redis в качестве очереди задач и хранилица сессий.
- ORM и миграции:
   - SQLAlchemy для работы с базой данных.
   - Alembic для управления миграциями.
- Фоновые задачи:
   - Celery для обработки фоновых задач (отправка уведомлений через бота).
- Контейнеризация:
   - Docker для контейнеризации приложения.
- Сервер:
   - Nginx для обратного проксирования и обработки статических файлов.

## Запуск:
> Для запуска вам потребуется [установить Docker](https://www.docker.com/).  
1. Клонировать проект с GitHub:
   ```bash
   git clone https://github.com/moduleb/websocket_chat.git
   ```

2. Перейти в папку проекта:
   ```bash
   cd websocket_chat
   ```

3. Указать токен от Telegram бота в формате `TOKEN=ваш_токен`:
   ```bash
   nano .env.EXAMPLE
   ```

4. Переименовать файл в `.env`:
   ```bash
   mv .env.EXAMPLE .env
   ```

5. Запустить приложение:
   ```bash
   sudo docker compose up -d --build
   ```

6. Перейти по адресу:
	- на локальной машине http://127.0.0.1:8000
	- на удаленном сервере http://<IP адрес сервера>:8000
	- документация доступна по адресу /docs

7. Остановить приложение:
```bash
sudo docker compose stop
```

