from database import get_connection


def init_db():

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""
        DROP TABLE IF EXISTS tasks;
    """)

    cur.execute("""
        CREATE TABLE tasks
        (
            task_id UUID PRIMARY KEY,
            model_name TEXT,
            status TEXT,
            created_at TIMESTAMP,
            started_at TIMESTAMP,
            finished_at TIMESTAMP,
            result JSONB
        )
    """)

    conn.commit()

    cur.close()
    conn.close()


if __name__ == "__main__":
    init_db()
