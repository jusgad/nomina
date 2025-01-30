import psycopg2

class Database:
    def __init__(self, dbname, user, password, host, port):
        self.conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )

    def save_worker(self, full_name, identification_number, professional_category, base_salary, start_date):
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO workers (full_name, identification_number, professional_category, base_salary, start_date) VALUES (%s, %s, %s, %s, %s)",
                (full_name, identification_number, professional_category, base_salary, start_date)
            )
            self.conn.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"Database Error: {e}")
            return False

    def get_workers(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM workers")
            rows = cursor.fetchall()
            cursor.close()
            return rows
        except Exception as e:
            print(f"Database Error: {e}")
            return []

    def close(self):
        self.conn.close()