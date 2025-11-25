# create_database.py creates a SQLite database from the Greek_Parliament_Proceedings_1989_2020.csv file
# from the https://zenodo.org/records/4311577#.X8-yMdgzaUk dataset

import sqlite3
import pandas as pd
import hashlib

def createdb(file,name):

    # Create db and table
    con = sqlite3.connect(name)
    cur = con.cursor()
    cur.execute("""
    CREATE TABLE speeches (
        id TEXT PRIMARY KEY,
        member_name TEXT,
        sitting_date TEXT,
        parliamentary_period TEXT,
        parliamentary_session TEXT,
        parliamentary_sitting TEXT,
        political_party TEXT,
        government TEXT,
        member_region TEXT,
        roles TEXT,
        member_gender TEXT,
        speech TEXT
    );
    """)

    # Helping function for uniqe id generation
    def make_id(row):
        base = f"{row['sitting_date']}_{row['member_name']}"
        text_hash = hashlib.md5(row["speech"][:200].encode("utf-8")).hexdigest()[:8]
        return f"{base}_{text_hash}"

    # Load file in chunks
    chunks = pd.read_csv(file, chunksize=10000)

    # Interate chunks
    for chunk_number, chunk in enumerate(chunks):
        # print(f"Chunk {chunk_number} data {chunk_number*10000} - {(chunk_number + 1)*10000}")

        # Genarate id for each entry
        chunk["id"] = chunk.apply(make_id, axis=1)

        rows = chunk[['id', 'member_name', 'sitting_date', 'parliamentary_period',
        'parliamentary_session', 'parliamentary_sitting', 'political_party',
        'government', 'member_region', 'roles', 'member_gender', 'speech']].values.tolist()

        # Insert data to db
        cur.executemany("""
            INSERT OR IGNORE INTO speeches
            (id, member_name, sitting_date, parliamentary_period, parliamentary_session, parliamentary_sitting, political_party, government, member_region, roles, member_gender, speech)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, rows)

        con.commit()

    con.close()

