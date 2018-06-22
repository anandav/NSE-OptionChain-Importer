import sqlite3
import os
import database
import configparser
from config import AppConfig


class databaseprovider:
    def __init__(self, data):
        self.data = data
        # self.config = configparser.ConfigParser()
        # self.config.read("config.ini")

    def GetConnetion(self):
        conn = sqlite3.connect(AppConfig().ConnectionString())
        return conn

    def CreateOptionChainTable(self, tableName):
        fl = open(AppConfig().ScriptCreateOptionChainTable(), "r")
        tblcontent = fl.read()
        tblname = AppConfig().TableName()
        tblcontent = tblcontent.replace("TABLENAME", tblname)
        conn = self.GetConnetion()
        conn.execute(tblcontent)
        conn.close()

    def SaveOptionChainData(self):
        data = self.PrepareData()
        conn = self.GetConnetion()
        fl = open(AppConfig().ScriptInsertOptionChain(), "r")
        tbl = fl.read()
        fl.close()
        if(len(data) > 0):
            conn.executemany(tbl, data)
        conn.commit()
        conn.close()    
      

    def PrepareData(self):
        result = []
        for item in self.data["OptionChain"]:
            result.append((self.data["Symbol"], self.data["Date"], self.data["SpotPrice"], 'call', item["StrickPrice"], item["Calls"]["AskPrice"], item["Calls"]["AskQty"], item["Calls"]
                           ["BidPrice"], item["Calls"]["BidQty"], item["Calls"]["Chng in OI"], item["Calls"]["IV"], item["Calls"]["LTP"], item["Calls"]["Net Chng"], item["Calls"]["OI"], item["Calls"]["Volume"]))
            result.append((self.data["Symbol"], self.data["Date"], self.data["SpotPrice"], 'put', item["StrickPrice"], item["Puts"]["AskPrice"], item["Puts"]["AskQty"],
                           item["Puts"]["BidPrice"], item["Puts"]["BidQty"], item["Puts"]["Chng in OI"], item["Puts"]["IV"], item["Puts"]["LTP"], item["Puts"]["Net Chng"], item["Puts"]["OI"], item["Puts"]["Volume"]))

        return result
