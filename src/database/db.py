import pymysql
import os

class Database():
    
    def __init__(self, host, user, password, database):
        self.connection= pymysql.connect(
            host=host,
            port=3306,
            user=user,
            password=password,
            database=database,
            cursorclass=pymysql.cursors.DictCursor
        )
        self.connection.autocommit(True)
        
    def add_user(self, user):
        self.connection.ping()
        with self.connection.cursor() as cursor:
            try:
                cursor.execute("INSERT INTO users (user_id, username, fullname, date_reg) VALUES (%s, %s, %s, %s);",
                                    (user["user_id"],
                                    user["username"],
                                    user["full_name"],
                                    user["date_reg"],))
            except:
                cursor.execute("UPDATE users SET username= %s, fullname= %s WHERE user_id=%s;",
                                    (user["username"],
                                     user["full_name"],
                                     user["user_id"],))
           
    def get_tasks(self, section=None, task_id= None):
        self.connection.ping()
        with self.connection.cursor() as cursor:
            if section:
                cursor.execute("SELECT * FROM tasks WHERE Блок= %s;", (section, ))
            elif task_id:
                cursor.execute("SELECT * FROM tasks WHERE id= %s;", (task_id, ))
            else:
                cursor.execute("SELECT * FROM tasks;")
            return cursor.fetchall()
    
    def get_task_from_id(self, task_id):
        self.connection.ping()
        with self.connection.cursor() as cursor:
            cursor.execute("""SELECT tasks.id, `section_id`, `theme`, `numEGE`, `exercise`, `answer`,
                               `maxBalls`, `decide`, `typecheck`, `section`
                               FROM tasks
                               INNER JOIN sections ON tasks.section_id = sections.id
                               WHERE tasks.id=%s""", (task_id))
            
        return cursor.fetchone()
     
    def upQueue(self, user_id):
        self.connection.ping()
        with self.connection.cursor() as cursor:
            count=len(self.get_tasks())-1
            user_queue= self.get_user_queue(user_id)
            if user_queue < count:
                cursor.execute("UPDATE users SET queue=queue+1 WHERE user_id=%s;", (user_id, ))
            else:
                cursor.execute("UPDATE users SET queue=0 WHERE user_id=%s;", (user_id, ))
                
    def get_user_tasks(self, user_id, section=None):
        self.connection.ping()
        with self.connection.cursor() as cursor:
            if section:
                cursor.execute("SELECT * FROM stats WHERE section= %s and user_id= %s;", (section, user_id, ))
            else:
                cursor.execute("SELECT * FROM stats WHERE user_id= %s;", (user_id, ))
            return cursor.fetchall()
        
    def get_user_tasks_answer(self, user_id, param='right'):
        self.connection.ping()
        with self.connection.cursor() as cursor:
            if param == 'right':
                cursor.execute("SELECT * FROM stats WHERE (user_answer = max_answer) and user_id=%s;", (user_id, ))
            elif param == 'partly':
                cursor.execute("SELECT * FROM stats WHERE (user_answer < max_answer) and (user_answer != 0) and user_id=%s;", (user_id, ))
            elif param == 'wrong':
                cursor.execute("SELECT * FROM stats WHERE (user_answer = 0) and user_id=%s;", (user_id, ))
            return cursor.fetchall()
        
    def get_max_points(self, user_id, section= None):
        self.connection.ping()
        with self.connection.cursor() as cursor:
            if section:
                cursor.execute("SELECT SUM(max_answer) FROM stats WHERE user_id=%s and section=%s;", (user_id, section, ))
            else:
                cursor.execute("SELECT SUM(max_answer) FROM stats WHERE user_id=%s;", (user_id, ))
            return cursor.fetchone()['SUM(max_answer)']
        
    def get_answer_points(self, user_id, section= None):
        self.connection.ping()
        with self.connection.cursor() as cursor:
            if section:
                cursor.execute("SELECT SUM(user_answer) FROM stats WHERE user_id=%s and section=%s;", (user_id, section, ))
            else:
                cursor.execute("SELECT SUM(user_answer) FROM stats WHERE user_id=%s;", (user_id, ))
                
            res= cursor.fetchone()['SUM(user_answer)']
            return res if res else 0
        
    def add_user_an(self, user_id, task_id, user_an):
        self.connection.ping()
        with self.connection.cursor() as cursor:
            cursor.execute("UPDATE stats SET user_answer=%s WHERE user_id=%s and task_id=%s", (user_an, user_id, task_id, ))
            
            print(cursor.rowcount)
            
    def get_stat(self, user_id):
        self.connection.ping()
        with self.connection.cursor() as cursor:
            cursor.execute("""SELECT * FROM stats WHERE user_id=%s""", (user_id))
            return cursor.fetchall()
        
    def add_last_task(self, user_id, task_id, section, max_an):
        self.connection.ping()
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM stats WHERE task_id=%s", (task_id))
            if len(cursor.fetchall()) == 1:
                cursor.execute("DELETE FROM stats WHERE task_id=%s", task_id)
            cursor.execute("INSERT INTO stats (user_id, task_id, section, max_answer) VALUES (%s, %s, %s, %s)", 
                               (user_id, task_id, section, max_an, ))
              
    def last_user_answer(self, user_id):
        self.connection.ping()
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM stats WHERE user_id=%s ORDER BY id DESC", (user_id, ))
            
            return cursor.fetchone()
     
    def get_last_tasks(self, user_id, section=None):
        self.connection.ping()
        with self.connection.cursor() as cursor:      
            if section:
                cursor.execute("SELECT task_id FROM stats WHERE user_id=%s and section=%s ORDER BY id DESC", (user_id, section, ))
            else:
                cursor.execute("SELECT task_id FROM stats WHERE user_id=%s ORDER BY id DESC", (user_id, ))
                
            return cursor.fetchmany(10)
        
    def getdata_tasks(self, bad_tasks, section=None):
        self.connection.ping()
        with self.connection.cursor() as cursor:
            if section:
                cursor.execute(f"""SELECT tasks.id, `section_id`, `theme`, `numEGE`, `exercise`, `answer`,
                               `maxBalls`, `decide`, `typecheck`, `section`
                               FROM tasks
                               INNER JOIN sections ON tasks.section_id = sections.id
                               WHERE section_id=%s and tasks.id not in (%s)""", (section, bad_tasks))
            else:
                cursor.execute(f"""SELECT tasks.id, `section_id`, `theme`, `numEGE`, `exercise`, `answer`,
                               `maxBalls`, `decide`, `typecheck`, `section`
                               FROM tasks
                               INNER JOIN sections ON tasks.section_id = sections.id
                               WHERE tasks.id not in (%s)""", (bad_tasks, ))
                
            return cursor.fetchall()
        
    def delete_last_task(self, id_):
        self.connection.ping()
        with self.connection.cursor() as cursor:
            cursor.execute("DELETE FROM stats WHERE id=%s", (id_, ))
            
    def import_tasks(self):
        self.connection.ping()
        with self.connection.cursor() as cursor:    
            cursor.execute("""INSERT INTO tasks
                           (`numEGE`, `section`, `theme`,
                           `exercise`, `answer`, `maxBalls`,
                           `decide`, `typecheck`)
                           VALUES (
                               %s, (SELECT id FROM sections WHERE section= %s), %s, %s,
                               %s, %s, %s, %s )""")