from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import datetime
from app.database import get_db
from app.security import verify_api_key
from app.schemas import TemplateItemCreate, TemplateItemResponse, ExceptionCreate, ExceptionResponse, DayScheduleResponse, LessonBase
from app.models import WeeklyTemplateModel, ScheduleExceptionModel

router = APIRouter(
    prefix="/schedule", 
    # tags=["Schedule"],
    dependencies=[Depends(verify_api_key)]
)

# Массив с названиями дней недели на русском языке. 
# Индексы в Python идут с 0, поэтому первый элемент оставляем пустым, чтобы Пн был под индексом 1.
RUSSIAN_DAYS = [
    "", 
    "Понедельник", 
    "Вторник", 
    "Среда", 
    "Четверг", 
    "Пятница", 
    "Суббота", 
    "Воскресенье"
]

def generate_schedule_for_date(target_date: datetime.date, db: Session) -> DayScheduleResponse:
    """
    Генерирует итоговое расписание на одну конкретную дату, 
    совмещая шаблон дня недели и замены.
    """
    day_of_week = target_date.isoweekday() # 1 = Понедельник, 7 = Воскресенье
    day_name = RUSSIAN_DAYS[day_of_week]   # Получаем текстовое название

    # 1. Получаем базовые уроки из шаблона для этого дня недели
    template_lessons = db.query(WeeklyTemplateModel)\
        .filter(WeeklyTemplateModel.day_of_week == day_of_week)\
        .order_by(WeeklyTemplateModel.lesson_number).all()

    # 2. Получаем замены/исключения на эту конкретную дату
    exceptions = db.query(ScheduleExceptionModel)\
        .filter(ScheduleExceptionModel.date == target_date).all()

    exceptions_dict = {exp.lesson_number: exp for exp in exceptions}
    final_lessons = []
    
    for t_lesson in template_lessons:
        if t_lesson.lesson_number in exceptions_dict:
            exp = exceptions_dict.pop(t_lesson.lesson_number)
            if exp.subject.strip().lower() != "отмена":
                final_lessons.append(LessonBase(
                    lesson_number=exp.lesson_number,
                    subject=exp.subject,
                    classroom=exp.classroom,
                    teacher=exp.teacher
                ))
        else:
            final_lessons.append(LessonBase(
                lesson_number=t_lesson.lesson_number,
                subject=t_lesson.subject,
                classroom=t_lesson.classroom,
                teacher=t_lesson.teacher
            ))

    for lesson_num, exp in exceptions_dict.items():
        if exp.subject.strip().lower() != "отмена":
            final_lessons.append(LessonBase(
                lesson_number=exp.lesson_number,
                subject=exp.subject,
                classroom=exp.classroom,
                teacher=exp.teacher
            ))

    final_lessons.sort(key=lambda x: x.lesson_number)

    # Возвращаем обновленный объект с полем day_name
    return DayScheduleResponse(
        date=target_date,
        day_of_week=day_of_week,
        day_name=day_name,
        lessons=final_lessons
    )


# --- 8 РЕАЛИЗОВАННЫХ ЭНДПОИНТОВ ---

# 1. Расписание на текущий день (один день)
@router.get("/today", response_model=DayScheduleResponse, summary="Расписание на текущий день", tags=["Расписание"])
def get_today_schedule(db: Session = Depends(get_db)):
    """
    Возвращает итоговое расписание на **сегодняшний день**.
    Автоматически берет шаблон текущего дня недели и накладывает актуальные замены.
    """
    return generate_schedule_for_date(datetime.date.today(), db)


# 2. Расписание на текущую неделю (массив из 7 дней текущей недели, с Пн по Вс)
@router.get("/current-week", response_model=list[DayScheduleResponse], summary="Расписание на текущую неделю с Пн по Вс",  tags=["Расписание"])
def get_current_week_schedule(db: Session = Depends(get_db)):
    today = datetime.date.today()
    start_of_week = today - datetime.timedelta(days=today.weekday()) # Понедельник
    
    week_schedule = []
    for i in range(7):
        current_date = start_of_week + datetime.timedelta(days=i)
        week_schedule.append(generate_schedule_for_date(current_date, db))
    return week_schedule


# 3. Расписание на следующую неделю (массив из 7 дней следующей недели, с Пн по Вс)
@router.get("/next-week", response_model=list[DayScheduleResponse], summary="Расписание на следующую неделю с Пн по Вс", tags=["Расписание"])
def get_next_week_schedule(db: Session = Depends(get_db)):
    today = datetime.date.today()
    start_of_next_week = today - datetime.timedelta(days=today.weekday()) + datetime.timedelta(days=7)
    
    next_week_schedule = []
    for i in range(7):
        current_date = start_of_next_week + datetime.timedelta(days=i)
        next_week_schedule.append(generate_schedule_for_date(current_date, db))
    return next_week_schedule


# 4. Расписание на текущий день + N дней (массив из N дней включая текущий)
@router.get("/today-plus-days/{days_count}", response_model=list[DayScheduleResponse], summary="Расписание на N дней вперед", tags=["Расписание"])
def get_schedule_with_offset(days_count: int, db: Session = Depends(get_db)):
    """
    Возвращает массив дней с расписанием, начиная с сегодняшнего дня, на указанное количество дней вперед.
    """
    if days_count < 1:
        raise HTTPException(status_code=400, detail="Количество дней должно быть не меньше 1")
    
    today = datetime.date.today()
    offset_schedule = []
    for i in range(days_count):
        current_date = today + datetime.timedelta(days=i)
        offset_schedule.append(generate_schedule_for_date(current_date, db))
    return offset_schedule


# 5. Возвращать шаблон расписания на неделю (список всех элементов шаблона)
@router.get("/template", response_model=list[TemplateItemResponse], summary="Получить базовый шаблон на неделю", tags=["Управление шаблоном"])
def get_weekly_template(db: Session = Depends(get_db)):
    """
    Возвращает постоянное недельное расписание, разбитое по дням недели (1 - Понедельник, 7 - Воскресенье).
    """
    return db.query(WeeklyTemplateModel).order_by(WeeklyTemplateModel.day_of_week, WeeklyTemplateModel.lesson_number).all()


# 6. Принимать обновления шаблона расписания на неделю
@router.post("/template", response_model=list[TemplateItemResponse], status_code=status.HTTP_201_CREATED, summary="Обновить базовый шаблон на неделю", tags=["Управление шаблоном"])
def update_weekly_template(items: list[TemplateItemCreate], db: Session = Depends(get_db)):
    """
    Полностью перезаписывает базовое расписание. **Внимание:** старый шаблон будет удален.
    """
    db.query(WeeklyTemplateModel).delete()  # Полностью перезаписываем шаблон
    db_items = [WeeklyTemplateModel(**item.model_dump()) for item in items]
    db.add_all(db_items)
    db.commit()
    return db_items


# 7. Возвращать замены на конкретную дату (замены на один день)
@router.get("/exceptions/{date}", response_model=list[ExceptionResponse], summary="Получить замены на дату", tags=["Замены и исключения"])
def get_exceptions_by_date(date: datetime.date, db: Session = Depends(get_db)):
    """
    Возвращает список точечных изменений (замен или отмен) на выбранную дату.
    """
    return db.query(ScheduleExceptionModel).filter(ScheduleExceptionModel.date == date).order_by(ScheduleExceptionModel.lesson_number).all()


# 8. Принимать замены на конкретную дату
@router.post("/exceptions", response_model=list[ExceptionResponse], status_code=status.HTTP_201_CREATED, summary="Добавить замены на дату", tags=["Замены и исключения"])
def create_exceptions(exceptions: list[ExceptionCreate], db: Session = Depends(get_db)):
    """
    Принимает список замен. Если на указанный урок в этот день уже существовала замена, она будет обновлена.
    Чтобы **отменить** урок, передайте в поле `subject` строку `"Отмена"`.
    """
    # Для гибкости: если на эти даты/уроки уже были замены, заменяем их новыми
    for exp in exceptions:
        db.query(ScheduleExceptionModel).filter(
            ScheduleExceptionModel.date == exp.date,
            ScheduleExceptionModel.lesson_number == exp.lesson_number
        ).delete()
        
    db_items = [ScheduleExceptionModel(**exp.model_dump()) for exp in exceptions]
    db.add_all(db_items)
    db.commit()
    return db_items