import sqlite3
import os
import database
from config import AppConfig

class databaseprovider:
    def __init__(self, data):
        self.data = data
    
    def GetConnetion(self):
        conn = sqlite3.connect(AppConfig().ConnectionString())
        return conn 

    def CreateTable(self, tableName):
        fl = open("database/createtable.sql", "r")
        tblcontent = fl.read()
        tblname = AppConfig().TableName()
        tblcontent = tblcontent.replace("TABLENAME", tblname)
        conn = self.GetConnetion()
        conn.execute(tblcontent)
        conn.close()
        #TODO
        


        
