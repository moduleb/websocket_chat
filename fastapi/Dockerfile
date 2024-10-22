FROM python:3.12-alpine

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл с зависимостями
COPY requirements.txt ./

# Устанавливаем зависимости
RUN pip install -r requirements.txt --no-cache-dir

# Копируем остальные файлы проекта в контейнер
COPY . .

# Выполняем миграции Alembic
# RUN ["alembic", "revision", "--autogenerate", "-m", "init"]
# RUN ["alembic", "upgrade", "head"]

