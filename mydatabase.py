import sqlite3
import os
import database

class databaseprovider:
    def __init__(self, connectionString, data):
        self.connectionString = connectionString
    
    def CreateTable(self, tableName):
        fl =  open(os.open("database/createtable.sql"), "r")

        
