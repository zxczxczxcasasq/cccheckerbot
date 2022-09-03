import sqlite3
import time
#Слито в @mordoradapter
class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()
#Слито в @mordoradapter    
    def add_user(self, user_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO `users` (`user_id`) VALUES (?)", (user_id,))
#Слито в @mordoradapter    
    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            return bool(len(result))
#Слито в @mordoradapter   
    def set_time_sub(self, user_id, time_sub):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `time_sub` = ? WHERE `user_id` = ?", (time_sub, user_id,))
#Слито в @mordoradapter    
    def get_time_sub(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `time_sub` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                time_sub = int(row[0])
            return time_sub
#Слито в @mordoradapter    
    def get_sub_status(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `time_sub` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                time_sub = int(row[0])
            if time_sub > int(time.time()):
                return True
            else:
                return False
#Слито в @mordoradapter
    def add_check(self, user_id, bill_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO `check` (`user_id`, `bill_id`) VALUES (?,?)", (user_id, bill_id,))
#Слито в @mordoradapter
    def get_check(self, bill_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `check` WHERE `bill_id` = ?", (bill_id,)).fetchmany(1)
            if not bool(len(result)):
                return False
            return result[0]
#Слито в @mordoradapter
    def delete_check(self, bill_id):
        with self.connection:
            result = self.cursor.execute("DELETE FROM `check` WHERE `bill_id` = ?", (bill_id,))
#Слито в @mordoradapter    
    def set_active(self, user_id, active):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `active` = ? WHERE `user_id` = ?", (active, user_id,))
#Слито в @mordoradapter
    def get_users(self):
        with self.connection:
            return self.cursor.execute("SELECT `user_id`, `active` FROM `users`").fetchall()
#Слито в @mordoradapter
    def get_antispam(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `antispam` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                antispam = int(row[0])
            if antispam > 0:
                return True
            else:
                return False
#Слито в @mordoradapter
    def set_antispam(self, user_id, antispam):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `antispam` = ? WHERE `user_id` = ?", (antispam, user_id,))
#Слито в @mordoradapter