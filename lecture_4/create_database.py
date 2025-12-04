import sqlite3

"""Создаёт базу данных и таблицы."""
def create_database():
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()

# 1. Создаём таблицу students
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        birth_year INTEGER NOT NULL
    )
    ''')

# 2. Создаём таблицу grades
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS grades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        subject TEXT NOT NULL,
        grade INTEGER NOT NULL,
        FOREIGN KEY (student_id) REFERENCES students (id),
        CHECK (grade BETWEEN 1 AND 100)
    )
    ''')

# 3. Создаём индексы для оптимизации
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_student_id ON grades(student_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_birth_year ON students(birth_year)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_subject ON grades(subject)')

# 4. Вставляем данные студентов
    students_data = [
        ('Alice Johnson', 2005),
        ('Brian Smith', 2004),
        ('Carla Reyes', 2006),
        ('Daniel Kim', 2005),
        ('Eva Thompson', 2003),
        ('Felix Nguyen', 2007),
        ('Grace Patel', 2005),
        ('Henry Lopez', 2004),
        ('Isabella Martinez', 2006)
    ]
    cursor.executemany('INSERT INTO students (full_name, birth_year) VALUES (?, ?)', students_data)

# 5. Вставляем данные оценок
    # Получаем ID студентов
    cursor.execute("SELECT id, full_name FROM students")
    student_ids = {name: id for id, name in cursor.fetchall()}

    grades_data = [
        (student_ids['Alice Johnson'], 'Math', 88),
        (student_ids['Alice Johnson'], 'English', 92),
        (student_ids['Alice Johnson'], 'Science', 85),
        (student_ids['Brian Smith'], 'Math', 75),
        (student_ids['Brian Smith'], 'History', 83),
        (student_ids['Brian Smith'], 'English', 79),
        (student_ids['Carla Reyes'], 'Science', 95),
        (student_ids['Carla Reyes'], 'Math', 91),
        (student_ids['Carla Reyes'], 'Art', 89),
        (student_ids['Daniel Kim'], 'Math', 84),
        (student_ids['Daniel Kim'], 'Science', 88),
        (student_ids['Daniel Kim'], 'Physical Education', 93),
        (student_ids['Eva Thompson'], 'English', 90),
        (student_ids['Eva Thompson'], 'History', 85),
        (student_ids['Eva Thompson'], 'Math', 88),
        (student_ids['Felix Nguyen'], 'Science', 72),
        (student_ids['Felix Nguyen'], 'Math', 78),
        (student_ids['Felix Nguyen'], 'English', 81),
        (student_ids['Grace Patel'], 'Art', 94),
        (student_ids['Grace Patel'], 'Science', 87),
        (student_ids['Grace Patel'], 'Math', 90),
        (student_ids['Henry Lopez'], 'History', 77),
        (student_ids['Henry Lopez'], 'Math', 83),
        (student_ids['Henry Lopez'], 'Science', 80),
        (student_ids['Isabella Martinez'], 'English', 96),
        (student_ids['Isabella Martinez'], 'Math', 89),
        (student_ids['Isabella Martinez'], 'Art', 92)
    ]
    cursor.executemany('INSERT INTO grades (student_id, subject, grade) VALUES (?, ?, ?)', grades_data)

    # Сохраняем изменения и закрываем соединение
    conn.commit()
    conn.close()
    print("База данных успешно создана! Файл: school.db")

if __name__ == "__main__":
    create_database()
