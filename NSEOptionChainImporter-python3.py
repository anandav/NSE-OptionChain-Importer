import argparse

import json
import os
import pickle
import re
import string
import traceback
from datetime import date, time
from json import JSONEncoder, dump
from os import name, system

import dateutil
import pandas as pd
import requests
import urllib3
from bs4 import BeautifulSoup


class Program:
    def __init__(self):
        self.clearScreen()
        self.Date = None
        self.Symbol = None
        self.SpotPrice = None
        print("start")

    """ Main Method """
    def Main(self):
        baseUrl = "https://nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp?instrument=OPTSTK&symbol=JINDALSTEL"
        outputType = "csv"  # "csv"
        fileNamePrefix = "Jindal Steel Optionchain "
        sourceDirectory = ''
        destinationDirectory = ''

        if (name == "nt"):
            sourceDirectory = "E:\\home\\Documents\\June\\"
            destinationDirectory = "E:\\home\\Documents\\June\\"
        else:
            sourceDirectory = os.path.expanduser('~') + "/Documents/June/"
            destinationDirectory = os.path.expanduser('~') + "/Documents/June/"

        self.ReadSavedOptionChain(sourceDirectory, destinationDirectory,
                                   fileNamePrefix, outputType)
        # self.ReadTodayOptionChain(baseUrl, destinationDirectory, fileNamePrefix, outputType)

        print('Finished')

    """  Read Saved NSE Option Chain HTML """
    def ReadSavedOptionChain(self, sourceDirectory, destinationDirectory,
                             fileNamePrefix, outputType):
        lstFiles = self.ReadFilesInDirectory(sourceDirectory)
        for file in lstFiles:
            sourceFileName = sourceDirectory + file
            print("reading:" + sourceFileName)
            page = open(sourceFileName, "rb")
            page = str(page.read())
            page = page.strip('\t')
            soup = BeautifulSoup(page, "html.parser")
            self.PopulateData(soup)
            self.ReadHtmlAndWriteToDestinationFile(soup, destinationDirectory,
                                                   fileNamePrefix, outputType)
    """ Read Todays Option chain from NSE """
    def ReadTodayOptionChain(self, baseUrl, destinationDirectory,
                             fileNamePrefix, outputType):
        print("Getting data from" + baseUrl)
        http = urllib3.PoolManager()
        httpResponce = http.request("GET", baseUrl)
        if (httpResponce.status == 200):
            print("page downloeded")
            soup = BeautifulSoup(httpResponce.data, "html.parser")
            self.PopulateData(soup)
            # self.WriteFile(filePath=
            #     destinationDirectory + "__temp_" + fileNamePrefix + ".html"
            #     ,outputType= None,html= str(soup), lstColmn =None, lstRows= None)

            self.ReadHtmlAndWriteToDestinationFile(soup, destinationDirectory,
                                                   fileNamePrefix, outputType)
        else:
            print("failed to get page")

    """ Read HTML"""
    def ReadHtmlAndWriteToDestinationFile(self, soup, destinationDirectory,
                                          fileNamePrefix, outputType):

        tupleResult = self.ReadTable(soup)
        desitnationFileName = destinationDirectory + fileNamePrefix + self.Date.strftime(
            "%d-%m") + '.' + outputType
        print("writing:" + desitnationFileName)
        self.WriteFile(desitnationFileName, tupleResult[0], tupleResult[1],
                       outputType)

    """ Read Option Chain HTML file """
    def ReadFilesInDirectory(self, rootFolder):
        lstfiles = []
        for root, dirs, files in os.walk(rootFolder):
            for file in files:
                if (file.endswith(".html")):
                    lstfiles.append(file)
        return lstfiles

    """ Read Html Table """
    def ReadTable(self, soup):
        lstColmn = []
        tbl = soup.find(id="octable")
        tblHeader = tbl.find("thead")
        tblHeaderRow = tblHeader.find_all("tr")
        tblBody = tbl.find("tbody")
        if (tblBody != None):
            tblBodyRow = tblBody.find_all("tr")
        else:
            tblBodyRow = tbl.find_all("tr")
        try:
            currentHeader = tblHeaderRow[1].find_all("th")
            currentHeader = currentHeader[1:len(currentHeader) - 1]
            colLen = len(currentHeader)
            for col in currentHeader:
                txt = col.text
                # txt = txt.encode("utf8")
                lstColmn.append(txt)
            rowLen = len(tblBodyRow)
            startIndex = 0
            lstRows = [[0 for x in range(colLen)] for y in range(rowLen-1)]
            for i in range(startIndex, rowLen-1):
                currentRow = tblBodyRow[i]
                cells = currentRow.find_all("td")
                cells = cells[1:len(cells) - 1]
                j = 0
                for cell in cells:
                    cellText = 0
                    cellText = cell.text.strip(
                        "\r\n\t-").replace(",", "").replace("\\n","").replace("\\t","").replace("-","").strip(" ")
                    if (cellText != ''):
                        lstRows[i][j] = float(cellText)
                    j += 1

        except:
            traceback.print_exc()

        tupleResult = (lstColmn, lstRows)
        return tupleResult

    """ Write file  based on output/html parameter"""
    def WriteFile(self, filePath, lstColmn, lstRows, outputType, html=None):
        fl = open(filePath, "w")
        if ((lstColmn != None) and (lstRows != None) and (html == None)):
            if (outputType == 'csv'):
                for x in range(0, len(lstColmn)):
                    fl.write(lstColmn[x])
                    if (x < len(lstColmn) - 1):
                        fl.write(",")
                    else:
                        fl.write("\n")

                for y in range(0, len(lstRows)):
                    rowdata = lstRows[y]
                    if (sum(rowdata) > 0):
                        rowdatalen = len(rowdata)
                        for z in range(0, rowdatalen):
                            fl.write(str(rowdata[z]))

                            if (z < rowdatalen - 1):
                                fl.write(",")
                            else:
                                fl.write("\n")
            elif (outputType == 'json'):
                jsonObject = {"Symbol": self.Symbol, "Date": self.Date.strftime("%d-%m-%Y"),
                              "SpotPrice": self.SpotPrice, "OptionChain": []}
                jsonArray = []
                for row in lstRows:
                    if(sum(row) > 0):
                        calls = dict(zip(lstColmn[0:10], row[0:10]))
                        puts = dict(zip(lstColmn[11:], row[11:]))

                        customJson = dict(
                            {"StrickPrice": row[10],  "Calls": calls, "Puts": puts})
                        jsonArray.append(customJson)
                jsonObject["OptionChain"] = jsonArray
                json.dump(jsonObject, fl)
        elif (html != None):
            fl.write(html)
        else:
            fl.write("Nothing to write")
        fl.close()

    """ Clear Screen   """
    def clearScreen(self):
        if (name == "nt"):
            system("cls")
        else:
            system("clear")

    """ Fill all data"""
    def PopulateData(self, soup):
        dateSpan = soup.find("p", {"class": "notification"})
        dateSpan2 = soup.select(".content_big #wrapper_btm table span")
        _optionDate = None
        if (dateSpan != None):
            dateSpan = dateSpan.find("span")
            _optionDate = dateSpan.text.replace("Normal Market has Closed.",
                                                "").strip()
        else:
            _optionDate = dateSpan2[1].get_text(strip=True).replace(
                "As on ", "").replace(" IST", "")

        _datas = dateSpan2[0].find("b").text.split()
        self.Symbol = _datas[0]
        self.SpotPrice = _datas[1]

        self.Date = dateutil.parser.parse(_optionDate)
        return self.Date


if __name__ == "__main__":
    pro = Program()
    pro.Main()
