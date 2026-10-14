from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Расписание API"
    PROJECT_DESCRIPTION: str = """
API для управления и вывода школьного расписания конкретного класса.
Служба автоматически объединяет базовый недельный шаблон и точечные замены.

### 🛡️ Авторизация
Для доступа ко всем эндпоинтам необходимо передавать HTTP-заголовок:
* **Заголовок:** `X-API-Key`
* **Значение:** Ваш секретный токен

### 📝 Особенности логики
1. **Замены:** Накладываются поверх шаблона на указанную дату.
2. **Отмена уроков:** Чтобы отменить урок, передайте в поле предмета строку `Отмена`.
"""
    DATABASE_URL: str
    X_API_KEY: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()