## About AutoDD Rev 2

AutoDD = Automatically does the "due diligence" for you. 
If you want to know what stocks people are talking about on reddit, this little program might help you. 

Original author - Fufu Fang https://github.com/fangfufu

Rev 2 Author - Steven Zhu https://github.com/kaito1410 Napo2k https://github.com/Napo2k

The original AutoDD produced a simple table of the stock ticker and the number of threads talking about the ticker.

Version 2 of AutoDD adds some options and features that the original did not have.

	- ability to display a change in results (ie, an increase or decrease of score from the previous day to today)
	
	- ability to pull additional stock information from yahoo finance (such as open and close price, volume, average volume, etc)
	
	- ability to pull results from multiple subreddits (pennystocks, RobinHoodPennyStocks, stocks, Daytrading, etc)
	
	- added score system to calculate a score for each ticker based on the number of occurrences, DD, Catalyst, or technical analysis flair, and number of upvotes
	
	- Can be run with a windows scheduler to run the program at a set time everyday

## Requirements 

Python (tested on python 3.8.1) https://www.python.org/downloads/release/python-381/

Pip - python get-pip.py https://phoenixnap.com/kb/install-pip-windows#:~:text=PIP%20is%20automatically%20installed%20with,9%2B%20and%20Python%203.4%2B.

psaw - pip install psaw https://pypi.org/project/psaw/

yahooquery - pip install yahooquery https://pypi.org/project/yahooquery/

tabulate - pip install tabulate https://pypi.org/project/tabulate/

The requirements can be installed by running install_requirements.bat / install_requirements.sh

## Running

Watch the setup video here https://www.youtube.com/watch?v=YwfwJYjnBFU

To set up the dependencies on Windows 10

	1. Install python 3.8 and make sure you add python to the path variable during installation
	2. Run install_requirements.bat, it should open a terminal and install the dependencies
	3. If all dependencies are installed successfully, run run_auto_dd.bat
	4. After 1-2 minutes, you should find a table_records.txt file in the AutoDD folder
	5. To generate a new table, simply run run_auto_dd.bat again, it will append a new table to the table_records.txt file

To set up the dependencies on Linux/MacOSX
	
	1. Install python 3.8 and Pip3 https://medium.com/swlh/installing-python-and-pip-on-mac-72b7639a58
	2. Run install_requirements.sh, it should open a terminal and install the dependencies
	3. If all dependencies are installed successfully, run run_auto_dd.sh
	4. After 1-2 minutes, you should find a table_records.txt file in the AutoDD folder
	5. To generate a new table, simply run run_auto_dd.bat again, it will append a new table to the table_records.txt file


For Advanced Users:
	
	1. Simply open the terminal (powershell or command prompt on windows, terminal on linux/MacOSX) and navigate to the AutoDD folder, then type:
		
		python main.py -h
		
	2. Follow the help document and set up the optional parameters as you'd like. 

## Columns Explained

Code - Ticker Name

Total - Total score on the ticker for r/pennystock subreddit. Higher means more discussions/chatter about this ticker

Recent - Score of the ticker from the last X hours. By default, Recent shows the score from the last 12 hours. If you change the interval for example --interval 48, then recent show data from 24 hours ago (48 divide by 2)

Prev - Score of the ticker from the last X to 2X hour period. By default, Prev shows the score from the last 12-24 hour period. If you change the interval for example --interval 48, then recent show data from the 24-48 hour period

Change - (Recent score - Prev score) Shows increase or decrease in amount of chatter/discussions about this ticker. Positive numbers = increase in discussions, higher numbers means more discussions/chatter about this ticker

Rockets - Number of Rocket Emojis

Price - Current stock price

%DayChange - Percentage change in todays price compared to yesterday

%50DayChange - Percentage change in todays price compared to the last 50 day average

%ChangeVol - Percentage Change in volumn from today to the 3 month average

Float - Float shares, number of tradable shares of the ticker

Industry - Industry of the company if available

## Example output

Default Output:

![Alt text](default_table.JPG?raw=true "Title")

Allsub Option Output:

![Alt text](allsub_option.JPG?raw=true "Title")

Yahoo Option Output:

![Alt text](yahoo_option.JPG?raw=true "Title")

## Options

In terminal, type:

	python main.py -h
	
This will produce the following help text:

	usage: main.py [-h] [--interval [INTERVAL]] [--min [MIN]] [--adv] [--sub [SUB]] [--sort [SORT]] [--filename [FILENAME]]

	AutoDD Optional Parameters

	optional arguments:
	-h, --help            show this help message and exit
	--interval [INTERVAL]
							Choose a time interval in hours to filter the results, default is 24 hours
	--min [MIN]           Filter out results that have less than the min score, default is 10
	--yahoo               Using this parameter shows yahoo finance information on the ticker, makes the script run slower!
	--sub [SUB]           Choose a different subreddit to search for tickers in, default is pennystocks
	--sort [SORT]         Sort the results table by descending order of score, 1 = sort by total score, 2 = sort by recent score, 3 = sort by previous score, 4 = sort by change in score, 5 = sort by # of rocket emojis
	--allsub              Using this parameter searchs from one subreddit only, default subreddit is r/pennystocks.
	--csv                 Using this parameter produces a table_records.csv file, rather than a .txt file
	--filename [FILENAME]
							Change the file name from table_records.txt to whatever you wish
			
			
			
Interval (Time interval)

	1. Choose a time interval N in hours to filter the results, default is 24 hours
	
	2. The score in the Total column shows the score for each ticker in the last N hours
	
	3. The score in the Recent column shows the score for each ticker in the last N/2 hours, default to 12h
	
	4. The score in the Prev column shows the score for each ticker in the last N/2 - N hours, default is 12h - 24h
	
	5. The score in the other subreddit columns shows the score for each ticker in the last 24 hours
	
	
Min (Minimum score)

	1. Filter out results that have less than the min score in the Title column, default is 10
	
	
Yahoo (Yahoo Finance toggle)

	1. Using this parameter shows yahoo finance information, running yahoo mode is slower
	
	2. This options shows additional yahoo information on the ticker, such as open price, day low, day high, forward PE, beta, volume, etc.
	
	
Sub (Subreddit Selection)

	1. Choose a different subreddit to search for tickers in, default is pennystocks
	
	2. When a different subreddit is choosen, the total, recent, prev columns contain the score for the choosen subreddit
	
	3. Possible choices: pennystocks, RobinHoodPennyStocks, Daytrading, StockMarket, stocks


Sort

	1. Sort the results by descending order of score, by default the table shows the highest total score first
	
	2.  pass in values 1, 2, 3, or 4
	
	3. 1 = sort by total score, 2 = sort by recent score, 3 = sort by previous score, 4 = sort by change in score, 5 = sort by change in # of rocket emojis
	
Allsub (Subreddit toggle)

	1. Using this parameter shows scores on the other subreddits such as RobinHoodPennyStocks, Stocks, WallStreetBets, etc
	
Csv 

	1. Outputs table_records.csv file

Filename

	1. choose a different filename, this programs saves the table results to table_records.txt in the same folder as the AutoDD.py program
	
## Troubleshoot

ModuleNotFoundError: No module named 'something'
	
	- This means the dependency was not installed correctly, try running: 
	
		pip install 'something'
		
	- Another possibility is that python is using the wrong version, try:
		
		python3 main.py
		
AutoDD.py not found

	- This means the terminal can't find the python script, either navigate to the AutoDD folder using terminal or
	
		python path-to-autodd-folder/AutoDD.py
		ie. python C:/AutoDD_Folder/AutoDD.py

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
    Copyright (C) 2020  Fufu Fang, kaito1410, Napo2k

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
