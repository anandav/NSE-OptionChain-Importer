import argparse
import dircache
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
from bs4 import BeautifulSoup


class Program:
    def __init__(self):
        self.clearScreen()
        print ("start")

    def Main(self):
        sourceDirectory = "/home/aditi/Documents/May/"
        destinationDirectory = "/home/aditi/Documents/May/"
        fileNamePrefix = "Jindal Steel Optionchain "
        baseUrl = "https://nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp?instrument=OPTSTK&symbol=JINDALSTEL"
        #"https://nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp?symbolCode=1816&symbol=JINDALSTEL&symbol=jindalstel&instrument=OPTSTK&date=-&segmentLink=17&segmentLink=17"
        outputType = "json"  #"csv"
        # self.ReadSavedOptionChain(sourceDirectory, destinationDirectory,
        #                           fileNamePrefix, outputType)
        self.ReadTodayOptionChain(baseUrl, destinationDirectory,
                                  fileNamePrefix, outputType)

        print('Finished')

    def ReadSavedOptionChain(self, sourceDirectory, destinationDirectory,
                             fileNamePrefix, outputType):
        lstFiles = self.ReadFilesInDirectory(sourceDirectory)
        for file in lstFiles:
            sourceFileName = sourceDirectory + file
            print ("reading:" + sourceFileName)
            page = open(sourceFileName, "r")
            soup = BeautifulSoup(page, "html.parser")
            self.ReadHtmlAndWriteToDestinationFile(soup, destinationDirectory,
                                                   fileNamePrefix, outputType)

    def ReadTodayOptionChain(self, baseUrl, destinationDirectory,
                             fileNamePrefix, outputType):
        print ("Getting data from" + baseUrl)
        page = requests.get(baseUrl)
        if (page.status_code == 200):
            print("page downloeded")
            soup = BeautifulSoup(page.content, "html.parser")

            # self.WriteFile(filePath=
            #     destinationDirectory + "__temp_" + fileNamePrefix + ".html"
            #     ,outputType= None,html= str(soup), lstColmn =None, lstRows= None)

            self.ReadHtmlAndWriteToDestinationFile(soup, destinationDirectory,
                                                   fileNamePrefix, outputType)
        else:
            print("failed to get page")

    def ReadHtmlAndWriteToDestinationFile(self, soup, destinationDirectory,
                                          fileNamePrefix, outputType):
        optionChainDate = self.GetDate(soup)
        tupleResult = self.ReadTable(soup)
        desitnationFileName = destinationDirectory + fileNamePrefix + optionChainDate.strftime(
            "%d-%m") + '.' + outputType
        print ("writing:" + desitnationFileName)
        self.WriteFile(desitnationFileName, tupleResult[0], tupleResult[1],
                       outputType)

    def ReadFilesInDirectory(self, rootFolder):
        lstfiles = []
        for root, dirs, files in os.walk(rootFolder):
            for file in files:
                if (file.endswith(".html")):
                    lstfiles.append(file)
        return lstfiles

    def ReadTable(self, soup):
        lstColmn = []
        tbl = soup.find(id="octable")

        #print(datetime.date.today())
        tblHeader = tbl.find("thead")
        tblHeaderRow = tblHeader.find_all("tr")
        tblBody = tbl.find("tbody")
        #foundTBody = False
        if (tblBody != None):
            tblBodyRow = tblBody.find_all("tr")
        else:
            tblBodyRow = tbl.find_all("tr")

        #print(tblBodyRow)

        try:
            currentHeader = tblHeaderRow[1].find_all("th")
            currentHeader = currentHeader[1:len(currentHeader) - 1]
            colLen = len(currentHeader)
            for col in currentHeader:
                txt = col.text
                encodedtxt = txt.encode("utf8")
                lstColmn.append(encodedtxt)
            rowLen = len(tblBodyRow)
            startIndex = 0

            lstRows = [[0 for x in range(colLen)] for y in range(rowLen)]
            for i in range(startIndex, rowLen):
                currentRow = tblBodyRow[i]
                cells = currentRow.find_all("td")
                cells = cells[1:len(cells) - 1]
                j = 0
                for cell in cells:
                    cellText = cell.text.strip("\r\n\t-").strip(',')
                    if (cellText == ''):
                        cellText = 0
                    lstRows[i][j] = float(cellText)
                    j += 1
                #print(lstRows[i])

        except:
            traceback.print_exc()

        tupleResult = (lstColmn, lstRows)
        return tupleResult

    def WriteFile(self, filePath, lstColmn, lstRows, outputType, html=None):

        fl = file(filePath, "w")
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
                jsonArray = []
                lstColmn = self.AddPrefixToColumnUsedInJson(lstColmn)
                for row in lstRows:
                    customJson = dict(zip(lstColmn, row))
                    jsonArray.append(customJson)
                json.dump(jsonArray, fl)
        elif (html != None):
            fl.write(html)
        else:
            fl.write("Nothing to write")

        fl.close()

    def AddPrefixToColumnUsedInJson(self, lstColmn):
        lstCalls = ["Call_" + x for inx, x in enumerate(lstColmn) if inx < 10]
        lstSP = [x for inx, x in enumerate(lstColmn) if inx == 10]
        lstPuts = ["Put_" + x for inx, x in enumerate(lstColmn) if inx >= 11]
        lstColmn = []
        lstColmn = lstCalls + lstSP + lstPuts
        return lstColmn

    def clearScreen(self):
        if (name == "nt"): system("cls")
        else: system("clear")

    def GetDate(self, soup):
        dateSpan = soup.find("p", {"class": "notification"})
        dateSpan2 = soup.select("#wrapper_btm table span")

        optionDate = date(1981,10,17)
        if (dateSpan != None):
            dateSpan = dateSpan.find("span")
            optionDate = dateSpan.text.replace("Normal Market has Closed.",
                                               "").strip()
        else:
            optionDate = dateSpan2[1].get_text(strip=True).replace(
                "As on ", "").replace(" IST", "")

        objOptDate = dateutil.parser.parse(optionDate)
        return objOptDate


if __name__ == "__main__":
    pro = Program()
    pro.Main()
