import sqlite3


class MySqlite3:
    def __init__(self, db):
        self.db = db

    def connection(self):
        conn = sqlite3.connect(self.db)
        cur = conn.cursor()
        conn.row_factory = sqlite3.Row
        return conn, cur

    def commit_close(self, conn):
        conn.commit()
        conn.close()

    def query(self, query):
        conn, cur = self.connection()
        cur.execute(query)
        rows = cur.fetchall()
        conn.close()
        return rows

    def edit_insert(self, query, var):
        conn, cur = self.connection()
        cur.execute(query, var)
        self.commit_close(conn)

    def delete(self, query, var):
        conn, cur = self.connection()
        cur.execute(query, var)
        self.commit_close(conn)

    def query2(self, query, var):
        conn, cur = self.connection()
        cur.execute(query, var)
        rows = cur.fetchall()
        conn.close()
        return rows

    def get_headers(self, table_name):
        conn, cur = self.connection()
        cur.execute(f"select * from {table_name}")
        header_list = [member[0] for member in cur.description]
        conn.close()
        return header_list

    def create_table(self, table_name, col_list):
        conn, cur = self.connection()
        cur.execute(f"CREATE TABLE {table_name} ({col_list[0]} INT)")
        for col in col_list[1:]:
            cur.execute(f"ALTER TABLE {table_name} ADD {col}")
        self.commit_close(conn)
