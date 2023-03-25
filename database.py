import sqlite3
class Database():

    def Database(self, dbname):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)
        self.cursor = self.conn.cursor()
        try:
            self.cursor.execute(f"SELECT * FROM {dbname}")
        except:
            #Создаётся таблица с параметрами заказа
            #Параметр confirmed отвечает за подтверждение заказа админом
            #Параметр pending определяет наличие заказа в очереди на печать
            #Параметр finished определяет завершённость заказа
            #Рекомендуется проверять сначала confirmed, а затем pending
            #Также рекомендуется спрашивать админа перед тем, как задать свойство finished
            self.cursor.execute(f'''CREATE TABLE {dbname}(
            id INTEGER NOT NULL,
            task_type TEXT,
            file_sent BOOLEAN,
            number_of_copies INTEGER, 
            two_side_printing INTEGER,
            pay_with_card INTEGER,
            confirmed INTEGER,
            pending INTEGER,
            finished INTEGER 
            )''')

    def insert_task(self, id:int, task_type='NULL', file_sent=0, number_of_copies=0, two_side_printing=0, pay_with_card=0, confirmed=0, pending=0, finished=0):
        self.cursor.execute(f"INSERT INTO {self.dbname} (id, task_type, file_sent, number_of_copies, two_side_printing, pay_with_card, confirmed, pending, finished) VALUES ({id}, {task_type}, {file_sent}, {number_of_copies}, {two_side_printing}, {pay_with_card}, {confirmed}, {pending}, {finished})")