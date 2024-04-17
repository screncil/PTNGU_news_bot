import sqlite3

import config


class vspConnection:

    def __init__(self):
        self.conn = sqlite3.connect(config.SQLITEDATABASE_URI)
        self.cur = self.conn.cursor()



class User(vspConnection):

    def getAllUsers(self):
        return self.cur.execute("SELECT * FROM users").fetchall()

    def addUser(self, user_id, username, join_time):
        self.cur.execute("INSERT INTO users (user_id, username, join_time) VALUES (?,?,?)", (user_id, username, join_time))
        self.conn.commit()

    def checkUserExists(self, user_id) -> bool:
        return bool(len(self.cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchall()))


class Admin(vspConnection):

    def getAllAdmins(self) -> list:
        return self.cur.execute("SELECT * FROM users WHERE admin=1").fetchall()

    def getAllAdminIds(self):
        return self.cur.execute("SELECT user_id FROM users WHERE admin=1").fetchall()[0]

    def checkAdmin(self, user_id) -> bool:
        return bool(self.cur.execute("SELECT admin FROM users WHERE user_id=?", (user_id)))



class Questions(vspConnection):

    def addQuestion(self, question_id, questioner_id, text, username):
        self.cur.execute("INSERT INTO questions (question_id, questioner_id, text, username) VALUES (?,?,?,?)", (question_id, questioner_id, text, username,))
        self.conn.commit()

    def checkUser(self, user_id) -> bool:
        return bool(len(self.cur.execute("SELECT * FROM questions WHERE questioner_id=?", (user_id,)).fetchall()))

    def getQuestion(self, question_id):
        return self.cur.execute("SELECT * FROM questions WHERE question_id=?", (question_id,)).fetchall()

    def getStatus(self, question_id):
        return bool(self.cur.execute("SELECT answering FROM questions WHERE question_id=?", (question_id,)).fetchone()[0])

    def updateStatus(self, question_id):
        self.cur.execute("UPDATE questions SET answering=1 WHERE question_id=?", (question_id,))
        self.conn.commit()

    def deleteQuestion(self, question_id):
        self.cur.execute("DELETE FROM questions WHERE question_id=?", (question_id,))
        self.conn.commit()


class News(vspConnection):

    def addNews(self, title, text, date ,news_id):
        self.cur.execute("INSERT INTO news (title, text, date, news_id) VALUES (?, ?, ?, ?)", (title, text, date, news_id))
        self.conn.commit()
