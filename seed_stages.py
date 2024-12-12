from sqlalchemy import create_engine, text

# Подключение к базе данных
DATABASE_URL = "postgresql://hr_monitor_user:hr_monitor_password@db:5432/hr_monitor_db"
engine = create_engine(DATABASE_URL)

def seed_stages():
    # Открываем соединение с базой
    with engine.connect() as conn:
        # Вставка данных в таблицу
        conn.execute(text("""
            INSERT INTO stages (name, description)
            VALUES
              ('открыта', 'Резюме загружено в систему'),
              ('изучена', 'HR просмотрел резюме'),
              ('интервью', 'Рекрут приглашен на интервью с HR'),
              ('прошли интервью', 'Рекрут прошел интервью с HR'),
              ('техническое собеседование', 'Рекрут приглашен на техническое собеседование'),
              ('пройдено техническое собеседование', 'Рекрут прошел техническое собеседование'),
              ('оффер', 'HR выслал предложение рекруту')
        """))

if __name__ == "__main__":
    seed_stages()
    print("Stages seeded successfully.")
