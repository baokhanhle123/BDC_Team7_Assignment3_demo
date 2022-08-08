import sqlite3


def get_all(query):
    conn = sqlite3.connect("data/data.db")
    data = conn.execute(query).fetchall()
    conn.close()
    return data


def get_column_names():
    conn = sqlite3.connect("data/data.db")
    data = conn.execute("SELECT * FROM users").description
    names = [rec[0] for rec in data]
    conn.close()
    return names


def get_records_by_ip(rec_ip):
    conn = sqlite3.connect("data/data.db")
    sql = """
    SELECT * FROM users WHERE ip_address=?
    """
    data = conn.execute(sql, (rec_ip,)).fetchall()
    conn.close()
    return data


if __name__ == "__main__":
    # print(get_all("SELECT * FROM category"))
    print(get_records_by_ip("14.185.94.34"))
    # print(get_column_names())
