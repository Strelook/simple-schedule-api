from pydantic import BaseModel, ConfigDict
import datetime

class LessonBase(BaseModel):
    lesson_number: int
    subject: str
    classroom: str | None = None
    teacher: str | None = None

# Схемы для шаблона на неделю
class TemplateItemCreate(LessonBase):
    day_of_week: int

class TemplateItemResponse(TemplateItemCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)

# Схемы для замен/исключений
class ExceptionCreate(LessonBase):
    date: datetime.date

class ExceptionResponse(ExceptionCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)

# Общая схема для отдачи итогового расписания на один день
class DayScheduleResponse(BaseModel):
    date: datetime.date
    day_of_week: int
    day_name: str
    lessons: list[LessonBase]