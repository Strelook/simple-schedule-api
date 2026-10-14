from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine, Base
from app.routers import schedule

# Описываем метаданные для тегов, чтобы они шли в красивом порядке с описанием
tags_metadata = [
    {
        "name": "Расписание",
        "description": "Эндпоинты для получения итогового расписания (с учетом замен) на различные периоды.",
    },
    {
        "name": "Управление шаблоном",
        "description": "Просмотр и редактирование базового недельного расписания (Пн-Вс).",
    },
    {
        "name": "Замены и исключения",
        "description": "Управление точечными изменениями, отменами и переносами уроков на конкретные даты.",
    },
]

# Автоматически создаем таблицы в SQLite при запуске
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME, description=settings.PROJECT_DESCRIPTION, openapi_tags=tags_metadata)

# Отключаем CORS: разрешаем любые источники, методы и заголовки
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутер расписания
app.include_router(schedule.router)