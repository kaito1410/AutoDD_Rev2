## About AutoDD Rev 2

AutoDD = Automatically does the "due diligence" for you. 
If you want to know what stocks people are talking about on reddit, this little program might help you. 

Original author - Fufu Fang https://github.com/fangfufu

Rev 2 Author - Steven Zhu https://github.com/kaito1410

The original AutoDD produced a simple table of the stock ticker and the number of threads talking about the ticker.

Version 2 of AutoDD adds some options and features that the original did not have.
	- ability to display a change in results (ie, from the previous day to today)
	- ability to pull additional stock information from yahoo (such as open and close price, volume, average volumn, etc)
	- ability to pull results from multiple subreddits (pennystocks, RobinHoodPennyStocks, stocks, Daytrading, etc)
	- added score system to calculate a score for each ticker based on the number of occurrences, DD or Catalyst flair, and number of upvotes
	- Can be run with a windows schedular to run the program at a set time everyday

## Requirements 

Python (tested on python 3.8) - make sure you add python to the path variable during installation

Pip python get-pip.py https://phoenixnap.com/kb/install-pip-windows#:~:text=PIP%20is%20automatically%20installed%20with,9%2B%20and%20Python%203.4%2B.

psaw - pip install psaw https://pypi.org/project/psaw/

yahooquery - pip install yahooquery https://pypi.org/project/yahooquery/

## Running
Simply open the terminal (powershell or command prompt in windows) and navigate to the AutoDD.py folder, then type:

    python AutoDD.py
	
Alternatively, you can run the script by providing the folder to AutoDD.py (note, you can use any path/folder, as long as it contains AutoDD.py)

	ie. python C:\AutoDD-folder\AutoDD.py

Running the script typically takes 1 minute or so, depending on your options and the number of results found
Once the script finishes running:
	
	1. The terminal will output: "Wrote to file successfully: C:\AutoDD-folder\table_records.txt"
	2. An output called table_records.txt will be created in the same folder as AutoDD.py.
		- If table_records.txt already exists, it will append to the text file instead 

## Example output

Simple Output:

![Alt text](simple_autodd.JPG?raw=true "Title")

Advanced Output:

![Alt text](advanced_autodd.JPG?raw=true "Title")

## Options

In terminal, type:

	python AutoDD.py -h
	
This will produce the following help text:

	usage: AutoDD.py [-h] [--interval [INTERVAL]] [--min [MIN]] [--adv] [--sub [SUB]] [--sort [SORT]] [--filename [FILENAME]]

	AutoDD Optional Parameters

	optional arguments:
	  -h, --help            show this help message and exit
	  --interval [INTERVAL]
							Choose a time interval in hours to filter the results, default is 24 hours
	  --min [MIN]           Filter out results that have less than the min score, default is 10
	  --adv                 Using this parameter shows advanced ticker information, running advanced mode is slower
	  --sub [SUB]           Choose a different subreddit to search for tickers in, default is pennystocks
	  --sort [SORT]         Sort the results table by descending order of score, 1 = sort by total score, 2 = sort by recent score, 3 = sort by previous score, 4 = sort by change in score
	  --filename [FILENAME]
							Change the file name from table_records.txt to whatever you wish
			
			
Interval (Time interval)
	- Choose a time interval in hours to filter the results, default is 24 hours
	- The score in the Total column shows the score for each ticker in the last 24 hours
	- The score in the Recent column shows the score for each ticker in the last 12 hours
	- The score in the Prev column shows the score for each ticker in the last 12-24 hours
	- The score in the other subreddit columns shows the score for each ticker in the last 24 hours
	
Min (Minimum score)
	- Filter out results that have less than the min score in the Title column, default is 10
	
Adv (Advanced settings)
	- Using this parameter shows advanced ticker information, running advanced mode is slower
	- This options shows additional yahoo information on the ticker, such as open price, day low, day high, forward PE, beta, volume, etc.
	
Sub (Subreddit)
	- Choose a different subreddit to search for tickers in, default is pennystocks
	- When a different subreddit is choosen, the total, recent, prev columns contain the score for the choosen subreddit
	- Possible choices: pennystocks, RobinHoodPennyStocks, Daytrading, StockMarket, stocks

Sort
	- Sort the results by descending order of score, by default the table shows the highest total score first
	-  pass in values 1, 2, 3, or 4
	- 1 = sort by total score, 2 = sort by recent score, 3 = sort by previous score, 4 = sort by change in score

Filename
	- choose a different filename, this programs saves the table results to table_records.txt in the same folder as the AutoDD.py program
	
## Scheduler (Tested on Windows) 
	
1. Create a .bat file and type in:

python path-to-AutoDD\AutoDD.py --whatever options you want to configure

2. Open windows Task Scheduler

3. Create a basic task

4. Fill in the name and description

5. Choose a trigger that works for you, mine is every day

6. Choose "Start a program" and put in the path to your .bat file 
	- ie. "C:\AutoDD-folder\run_auto_dd.bat"
	
7. That's it, just check table_records.txt or the file name that you've selected and it will have the table ready
	
## Developers/Advanced Users

I'm a C++ main, so excuse my python code/inefficencies with handling tables and lists in python.

I've put a couple global variables for some advanced users to allow for easy modifications:

	# dictionary of possible subreddits to search in with their respective table column name
	subreddit_dict = {'pennystocks' : 'pnystks',
					  'RobinHoodPennyStocks' : 'RHPnnyStck',
					  'Daytrading' : 'daytrade',
					  'StockMarket' : 'stkmrkt',
					  'stocks' : 'stocks'}

	# dictionary of ticker financial information to get from yahoo
	financial_measures = {'currentPrice' : 'Price', 'quickRatio': 'QckRatio', 'currentRatio': 'CrntRatio', 'targetMeanPrice': 'trgtmean', 'recommendationKey': 'recommadtn'}

	# dictionary of ticker summary information to get from yahoo
	summary_measures = {'previousClose' : 'prvCls', 'open': 'open', 'dayLow': 'daylow', 'dayHigh': 'dayhigh', 'payoutRatio': 'pytRatio', 'forwardPE': 'forwardPE', 'beta': 'beta', 'bidSize': 'bidSize', 'askSize': 'askSize', 'volume': 'volume', 'averageVolume': 'avgvolume', 'averageVolume10days': 'avgvlmn10', 'fiftyDayAverage': '50dayavg', 'twoHundredDayAverage': '200dayavg'}


	# note: the following scoring system is tuned to calculate a "popularity" score
	# feel free to make adjustments to suit your needs

	# x base point of for a ticker that appears on a subreddit title or text body that fits the search criteria
	base_points = 4

	# x bonus points for each flair matching 'DD' or 'Catalyst' of for a ticker that appears on the subreddit
	bonus_points = 2

	# every x upvotes on the thread counts for 1 point (rounded down)
	upvote_factor = 2	

## License

    AutoDD - Automatically does the "due diligence" for you. 
    Copyright (C) 2020  Fufu Fang And Steven Zhu

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
