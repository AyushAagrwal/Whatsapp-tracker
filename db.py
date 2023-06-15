import sqlite3

con = sqlite3.connect('data.db',check_same_thread=False)
cur = con.cursor()


def create_table(table_name):
    query = f"CREATE TABLE IF NOT EXISTS {table_name} (name TEXT NOT NULL,from_time TEXT NOT NULL,to_time TEXT NOT NULL)"
    try:
        cur.execute(query)
        print('table created')
    except:
        print('error')

create_table('info')



def insertion_table(table_name,data_tuple):
    try:
        query = f"INSERT INTO {table_name} VALUES {data_tuple}"
        cur.execute(query)
        con.commit()
        return "sucessfully inserted"
    except:
        return "error insertion"
    

def local_mysql_query(query):
    con = sqlite3.connect('data.db',check_same_thread=False)
    cur = con.cursor()

    cur.execute(query)
    con.commit()
    data = cur.fetchall()
    return data