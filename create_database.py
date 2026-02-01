# create_database.py creates a SQLite database from the Greek_Parliament_Proceedings_1989_2020.csv file
# from the https://zenodo.org/records/4311577#.X8-yMdgzaUk dataset

import sqlite3
import pandas as pd
import os.path as path

# createdb to make an sqlite db
# file = csv file to make the db from "example.csv"
# name = name of saved .db file "exmple.db"
def createdb(file,name):
    
    if path.isfile(name):
        return

    # create db and table
    con = sqlite3.connect(name)
    cur = con.cursor()
    cur.execute("""
    CREATE TABLE speeches (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        member_name TEXT,
        sitting_date DATE,
        political_party TEXT,
        government TEXT,
        member_region TEXT,
        roles TEXT,
        speech TEXT
    );
    """)

    # load file in chunks
    chunks = pd.read_csv(file, chunksize=10000)

    for chunk_number, chunk in enumerate(chunks):
        # print(f"Chunk {chunk_number} data {chunk_number*10000} - {(chunk_number + 1)*10000}")

        # change date to yyyy-mm-dd format for filtering
        chunk["sitting_date"] = pd.to_datetime(
        chunk["sitting_date"],
        format="%d/%m/%Y",
        errors="coerce").dt.strftime("%Y-%m-%d")

        rows = chunk[['member_name', 'sitting_date', 'political_party',
        'government', 'member_region', 'roles', 'speech']].values.tolist()

        # insert data to db
        cur.executemany("""
            INSERT OR IGNORE INTO speeches
            (member_name, sitting_date, political_party, government, member_region, roles, speech)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, rows)

        con.commit()

    con.close()