import argparse
import os
from os import name, system 
from NSEOptionChainImporter import Program


""" Clear Screen   """

def clearScreen():
    if (name == "nt"):
        system("cls")
    else:
        system("clear")


if __name__ == "__main__":

    clearScreen()
    print("Start")
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--symbol", dest="symbol", action="store",
                        default="jindalstel", help="NSE Symbol")
    parser.add_argument("-f", "--format", dest="format",
                        action="store", default="csv",  help="CSV or JSON format")
    parser.add_argument("-p", "--fileNamePrefix", dest="fileNamePrefix", action="store",
                        default="",  help="File name prefix")
    parser.add_argument("-sd", "--sourcedirectory", dest="sd", action="store",
                        default="/Documents/June/",  help="Source Directory path (in home dir)")
    parser.add_argument("-dd", "--destinationdirectory", dest="dd", action="store",
                        default="/Documents/June/",  help="Destination Directory path (in home dir)")
    parser.add_argument("-o", "--online", dest="onlineData", action="store_true", default=True,
                        help="Get data from NSE portal when set to 'True', else get data from the html store local using -sd")

    # parser.add_argument('-s', action='store', dest='symbol' , default="nifty", help='NSE Symbol')
    args = parser.parse_args()
    fnp = ''
    if(args.fileNamePrefix == ''):
        fnp = args.symbol
    else:
        fnp = args.fileNamePrefix

    if(name == "nt"):
        if (args.sd == ''):
            args.sd = "c:\\temp\\"
        if(args.dd == ''):
            args.dd = "c:\\temp\\"
    else:
        if (args.sd == ''):
            args.sd = os.path.expanduser('~')
        if(args.dd == ''):
            args.dd = os.path.expanduser('~')

    pro = Program(args.symbol, args.format, fnp,
                  args.sd, args.dd, args.onlineData)
    pro.Main()
