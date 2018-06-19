## NSE-OptionChain-Importer
NSE([National Stock Exchange of India](https://nseindia.com/)) Option Chain Importer.
Used to import the data from [Option Chain](https://nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp) to csv, json, html

*Parameters:*
``` 
  -s, --symbol                  NSE Symbol
  -f, --format                  CSV/JSON/BOTH format, 'BOTH' will generate csv and json files
  -p, --fileNamePrefix          File name prefix
  -sd, --sourcedirectory        Source Directory path (in home dir)
  -dd , --destinationdirectory  Destination Directory path (in home dir)
  -o, --online                  Get data from NSE portal when set to 'True', else get data from the html store local using -sd
  -sah, --sahtml                Save HTML file



