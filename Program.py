import argparse
import configparser
import os
import re
from os import name, system
from NSEOptionChainImporter import Program


""" Clear Screen   """


def clearScreen():
    if (name == "nt"):
        system("cls")
    else:
        system("clear")


if __name__ == "__main__":

    config = configparser.ConfigParser()
    config.read("config.ini")
    optionchianurlformat = ''
    connectionString = ''
    if('config' in config):
        optionchianurlformat = config["config"]["optionchianurlformat"]
        connectionString = config["config"]["connectionstring"]

    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--symbol", dest="symbol", action="store",
                        default="jindalstel", help="NSE Symbol")
    parser.add_argument("-f", "--format", dest="format",
                        action="store", default="csv",  help="CSV/JSON/DB format")
    parser.add_argument("-p", "--fileNamePrefix", dest="fileNamePrefix", action="store",
                        default="Optionchain ",  help="File name prefix")
    parser.add_argument("-sd", "--sourcedirectory", dest="sd",
                        action="store",  help="Source Directory path (in home dir)")
    parser.add_argument("-dd", "--destinationdirectory", dest="dd",
                        action="store",  help="Destination Directory path (in home dir)")
    parser.add_argument("-o", "--online", dest="onlineData", action="store_true",  default=True,
                        help="Get data from NSE portal when set to 'True', else get data from the html store local using -sd")
    parser.add_argument("-sah", "--sahtml", dest="saveAsHtml",
                        action="store_true", default=False, help="Save HTML file")

    args = parser.parse_args()
    fnp = ''
    if(args.fileNamePrefix == ''):
        fnp = args.symbol
    else:
        fnp = args.fileNamePrefix

    if(name == "nt"):
        if (args.sd == None):
            args.sd = "c:\\temp\\"
        if(args.dd == None):
            args.dd = "c:\\temp\\"
    else:
        if (args.sd == None):
            args.sd = os.path.expanduser('~')+"/Documents/June/"
        if(args.dd == None):
            args.dd = os.path.expanduser('~')+"/Documents/June/"

    clearScreen()

    print("Start")
    pro = Program(optionchianurlformat, args.symbol, args.format, fnp,
                  args.sd, args.dd, args.onlineData, args.saveAsHtml, connectionString)
    pro.Main()
