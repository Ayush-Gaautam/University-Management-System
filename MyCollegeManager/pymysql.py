import sqlite3


def connect(host=None, user=None, password=None, db=None, **kwargs):
    return SQLiteConnection(db or "my_college_db")


class SQLiteConnection:
    def __init__(self, db_name):
        self.db_name = db_name
        self.db_path = f"{db_name}.sqlite3"
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self._initialize_schema()

    def _initialize_schema(self):
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS department (
                dname TEXT PRIMARY KEY
            )
            """
        )
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS course (
                dname TEXT,
                cname TEXT PRIMARY KEY,
                fee TEXT,
                duration TEXT,
                units TEXT
            )
            """
        )
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS student (
                rollno TEXT PRIMARY KEY,
                name TEXT,
                phone TEXT,
                gender TEXT,
                dob TEXT,
                address TEXT,
                department TEXT,
                course TEXT
            )
            """
        )
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS user (
                username TEXT PRIMARY KEY,
                password TEXT,
                usertype TEXT,
                picture TEXT
            )
            """
        )

        self.conn.execute("INSERT OR IGNORE INTO department (dname) VALUES ('Computer Science')")
        self.conn.execute("INSERT OR IGNORE INTO department (dname) VALUES ('Business')")
        self.conn.execute(
            "INSERT OR IGNORE INTO course (dname, cname, fee, duration, units) VALUES ('Computer Science', 'Python', '5000', '6', 'Month(s)')"
        )
        self.conn.execute(
            "INSERT OR IGNORE INTO course (dname, cname, fee, duration, units) VALUES ('Business', 'Marketing', '4000', '3', 'Month(s)')"
        )
        self.conn.execute(
            "INSERT OR IGNORE INTO student (rollno, name, phone, gender, dob, address, department, course) VALUES ('101', 'Alice', '9876543210', 'Female', '2002-01-01', 'Main Street', 'Computer Science', 'Python')"
        )
        self.conn.execute(
            "INSERT OR IGNORE INTO user (username, password, usertype, picture) VALUES ('admin', 'admin', 'Admin', 'default2.png')"
        )
        self.conn.commit()

    def cursor(self):
        return SQLiteCursor(self.conn)

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()


class SQLiteCursor:
    def __init__(self, conn):
        self.conn = conn
        self._cursor = conn.cursor()
        self.rowcount = 0

    def execute(self, query, params=()):
        sql = self._translate_query(query)
        values = tuple(params) if params is not None else ()
        self._cursor.execute(sql, values)
        self.rowcount = self._cursor.rowcount
        return self.rowcount

    def executemany(self, query, params_list):
        sql = self._translate_query(query)
        self._cursor.executemany(sql, params_list)
        self.rowcount = self._cursor.rowcount
        return self.rowcount

    def fetchone(self):
        return self._cursor.fetchone()

    def fetchall(self):
        return self._cursor.fetchall()

    def __getattr__(self, name):
        return getattr(self._cursor, name)

    @staticmethod
    def _translate_query(query):
        return query.replace('%s', '?')
