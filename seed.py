from app.database import SessionLocal, engine, Base
from app.models import WeeklyTemplateModel

def seed_data():
    # Убедимся, что таблицы созданы
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    # Очищаем старый шаблон перед заполнением, чтобы данные не дублировались
    db.query(WeeklyTemplateModel).delete()

    schedule_data = [
        # --- ПОНЕДЕЛЬНИК (1) ---
        WeeklyTemplateModel(day_of_week=1, lesson_number=1, subject="Разговоры о важном", teacher="Степанова Н.Н.", classroom="205"),
        WeeklyTemplateModel(day_of_week=1, lesson_number=2, subject="Математика", teacher="Степанова Н.Н.", classroom="205"),
        WeeklyTemplateModel(day_of_week=1, lesson_number=3, subject="Англ. яз", teacher="1:Григорян Г.М 2:Аббасова С.Я.", classroom="210"),
        WeeklyTemplateModel(day_of_week=1, lesson_number=4, subject="Русс.яз.", teacher="Степанова Н.Н.", classroom="205"),
        WeeklyTemplateModel(day_of_week=1, lesson_number=5, subject="Лит. Чтение (С)", teacher="Степанова Н.Н.", classroom="205"),
        WeeklyTemplateModel(day_of_week=1, lesson_number=6, subject="Физ-ра (С)", teacher="Жаркова С.Ю.", classroom="210"),

        # --- ВТОРНИК (2) ---
        WeeklyTemplateModel(day_of_week=2, lesson_number=1, subject="Математика", teacher="Степанова Н.Н.", classroom="205"),
        WeeklyTemplateModel(day_of_week=2, lesson_number=2, subject="Англ. яз", teacher="1:Григорян Г.М 2:Аббасова С.Я.", classroom="210"),
        WeeklyTemplateModel(day_of_week=2, lesson_number=3, subject="Русс. яз. (С)", teacher="Степанова Н.Н.", classroom="205"),
        WeeklyTemplateModel(day_of_week=2, lesson_number=4, subject="Н.теннис/Шахматы", teacher="Луценко О.Н./Мезенцева Е"),
        WeeklyTemplateModel(day_of_week=2, lesson_number=5, subject="Окр. мир", teacher="Степанова Н.Н.", classroom="205"),
        WeeklyTemplateModel(day_of_week=2, lesson_number=6, subject="Русс. яз. (С)", teacher="Степанова Н.Н.", classroom="205"),

        # --- СРЕДА (3) ---
        WeeklyTemplateModel(day_of_week=3, lesson_number=1, subject="Математика", teacher="Степанова Н.Н.", classroom="205"),
        WeeklyTemplateModel(day_of_week=3, lesson_number=2, subject="Музыка", teacher="Биктимирова Ф.И."),
        WeeklyTemplateModel(day_of_week=3, lesson_number=3, subject="Русс. яз. (С)", teacher="Степанова Н.Н.", classroom="205"),
        WeeklyTemplateModel(day_of_week=3, lesson_number=4, subject="Лит. чтение (С)", teacher="Степанова Н.Н.", classroom="205"),
        WeeklyTemplateModel(day_of_week=3, lesson_number=5, subject="ИЗО", teacher="Степанова Н.Н.", classroom="205"),
        WeeklyTemplateModel(day_of_week=3, lesson_number=6, subject="Физ-ра (С)", teacher="Жаркова С.Ю."),

        # --- ЧЕТВЕРГ (4) ---
        WeeklyTemplateModel(day_of_week=4, lesson_number=1, subject="Англ. яз", teacher="1:Григорян Г.М 2:Аббасова С.Я."),
        WeeklyTemplateModel(day_of_week=4, lesson_number=2, subject="Математика", teacher="Степанова Н.Н.", classroom="205"),
        WeeklyTemplateModel(day_of_week=4, lesson_number=3, subject="Лит. чтение", teacher="Степанова Н.Н.", classroom="205"),
        WeeklyTemplateModel(day_of_week=4, lesson_number=4, subject="Н.теннис/Шахматы", teacher="Луценко О.Н./Мезенцева Е", classroom="205"),
        WeeklyTemplateModel(day_of_week=4, lesson_number=5, subject="Русс. яз", teacher="Степанова Н.Н.", classroom="205"),
        WeeklyTemplateModel(day_of_week=4, lesson_number=6, subject="ТРУД", teacher="Степанова Н.Н.", classroom="205"),

        # --- ПЯТНИЦА (5) ---
        WeeklyTemplateModel(day_of_week=5, lesson_number=1, subject="Русс. яз", teacher="Степанова Н.Н.", classroom="205"),
        WeeklyTemplateModel(day_of_week=5, lesson_number=2, subject="Лит. чтение", teacher="Степанова Н.Н.", classroom="205"),
        WeeklyTemplateModel(day_of_week=5, lesson_number=3, subject="Окр. мир", teacher="Степанова Н.Н.", classroom="205"),
        WeeklyTemplateModel(day_of_week=5, lesson_number=4, subject="Хореография", teacher="Тартарницев Д.А."),
        WeeklyTemplateModel(day_of_week=5, lesson_number=5, subject="ОРКСЭ", teacher="Степанова Н.Н.", classroom="205"),
        WeeklyTemplateModel(day_of_week=5, lesson_number=6, subject="Математика (C)", teacher="Степанова Н.Н.", classroom="205"),
    ]

    try:
        db.add_all(schedule_data)
        db.commit()
        print("🎉 База данных успешно заполнена тестовым расписанием!")
    except Exception as e:
        db.rollback()
        print(f"❌ Произошла ошибка при заполнении БД: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()