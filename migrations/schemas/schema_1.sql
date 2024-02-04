CREATE TABLE IF NOT EXISTS tasks(
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        task_type INTEGER,
        file_path TEXT,
        number_of_copies INTEGER,
        coast INT,
        sides_count TEXT,
        pay_way INTEGER,
        status INTEGER
        )