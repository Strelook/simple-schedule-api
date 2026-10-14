from sqlalchemy import String, Integer, Date
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
import datetime

# Шаблон расписания на неделю (Пн-Сб)
class WeeklyTemplateModel(Base):
    __tablename__ = "weekly_templates"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    day_of_week: Mapped[int] = mapped_column(Integer, index=True)  # 1 - Понедельник, 7 - Воскресенье
    lesson_number: Mapped[int] = mapped_column(Integer)            # Номер урока (1, 2, 3...)
    subject: Mapped[str] = mapped_column(String)                   # Предмет
    classroom: Mapped[str | None] = mapped_column(String, nullable=True) # Класс
    teacher: Mapped[str | None] = mapped_column(String, nullable=True) # Учитель

# Замены / Исключения на конкретную дату
class ScheduleExceptionModel(Base):
    __tablename__ = "schedule_exceptions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    date: Mapped[datetime.date] = mapped_column(Date, index=True)  # Конкретная дата замены
    lesson_number: Mapped[int] = mapped_column(Integer)
    subject: Mapped[str] = mapped_column(String)                   # Новый предмет (или 'Отмена')
    classroom: Mapped[str | None] = mapped_column(String, nullable=True)
    teacher: Mapped[str | None] = mapped_column(String, nullable=True) # Учитель