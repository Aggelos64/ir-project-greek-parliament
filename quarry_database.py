import sqlite3
import numpy as np


class quarry_db():

    def __init__(self,filename):
        self.con = sqlite3.connect(filename, check_same_thread=False)
        self.cur = self.con.cursor()


    def get_all_names(self):
        res = self.cur.execute('SELECT DISTINCT member_name FROM speeches')
        a = res.fetchall()
        a = np.array(a)
        a = np.squeeze(a)
        return a
    
    def get_all_partys(self):
        res = self.cur.execute('SELECT DISTINCT political_party FROM speeches')
        a = res.fetchall()
        a = np.array(a)
        a = np.squeeze(a)
        return a
    
    def get_all_speachees(self):
        res = self.cur.execute("SELECT speech FROM speeches")
        a = res.fetchall()
        a = np.array(a,dtype=object)
        a = np.squeeze(a)
        return a
    
    # get all from an array of ids
    def get_by_idarray(self, ids):
        placeholders = ",".join(["?"] * len(ids))
    
        order_clause = "CASE id " + " ".join(f"WHEN ? THEN {i}" for i, _ in enumerate(ids)) + " END"

        sql = f"""
            SELECT *
            FROM speeches
            WHERE id IN ({placeholders})
            ORDER BY {order_clause}
        """
        params = list(ids) + list(ids)

        res = self.cur.execute(sql, params)
        a = res.fetchall()
        a = np.array(a)
        return a
    
    # filters : Dictionary containing filter criteria. Can include:
    #    member_name : Filter by speaker name
    #    date_from : Start date (YYYY-MM-DD)
    #    date_to : End date (YYYY-MM-DD)
    #    political_party : Filter by political party
    def get_ids_by_filters(self,filters={}):
        sql = "SELECT id FROM speeches WHERE 1=1 "
        params = []

        if 'member_name' in filters and filters['member_name']:
            sql += " AND member_name LIKE ?"
            params.append(f"%{filters['member_name']}%")
        
        if 'political_party' in filters and filters['political_party']:
            sql += " AND political_party = ?"
            params.append(filters['political_party'])
        
        if 'date_from' in filters and filters['date_from']:
            print(filters['date_from'])
            sql += " AND sitting_date >= ?"
            params.append(filters['date_from'])
        
        if 'date_to' in filters and filters['date_to']:
            sql += " AND sitting_date <= ?"
            params.append(filters['date_to'])

        if params:
            res = self.cur.execute(sql, params)
        else:
            res = self.cur.execute(sql)

        a = res.fetchall()
        a = np.array(a,dtype=object)
        a = np.squeeze(a)
        return a-1