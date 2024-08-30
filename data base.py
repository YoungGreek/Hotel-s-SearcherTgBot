import datetime
import sqlite3 as sq


datetime = datetime.datetime.today()
date = datetime.date()
time = datetime.time()
with sq.connect('TelegramBot.sqlite3') as con:
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users (\n"
                "        name TEXT,\n"
                "        command TEXT,\n"
                "        date TEXT,\n"
                "        time TEXT,\n"
                "        hotels TEXT\n"
                "        )")
    cur.execute("""INSERT INTO users (date, time) VALUES (?, ?)""", (str(date), str(time),))

with sq.connect('TelegramBot.sqlite3') as con:
    cur = con.cursor()
    records = cur.fetchall()
    for row in records:
        print('ID: ', row[0])
        print('ID: ', row[0])
        print('ID: ', row[0])
        print('ID: ', row[0])
        print('ID: ', row[0])