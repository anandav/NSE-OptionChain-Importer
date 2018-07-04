## NSE-OptionChain-Importer
NSE([National Stock Exchange of India](https://nseindia.com/)) Option Chain Importer.
Used to import the data from [Option Chain](https://nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp) to csv, json, html

#### *Parameters:*
``` 
  -s, --symbol                  NSE Symbol
  -f, --format                  CSV/JSON/DB format, all option can be used using comma separator
  -p, --fileNamePrefix          File name prefix
  -sd, --sourcedirectory        Source Directory path (in home dir)
  -dd , --destinationdirectory  Destination Directory path (in home dir)
  -o, --online                  Get data from NSE portal when set to 'True', else get data from the html store local using -sd
  -sah, --sahtml                Save HTML file
```

#### *Requirment:*
> 1. urllib3
> 2. bs4(BeautifulSoup)
> 3. certifi
> 4. dateutil

#### *ToDo:*
> * Scheduler download
> * Store date to Database
> * UI to Visivalize data using D3.js and Django



