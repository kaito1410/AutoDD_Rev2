
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" AutoDD: Automatically does the so called Due Diligence for you. """

#AutoDD - Automatically does the "due diligence" for you.
#Copyright (C) 2020  Fufu Fang, Steven Zhu

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <https://www.gnu.org/licenses/>.

__author__ = "Fufu Fang kaito1410 Napo2k"
__copyright__ = "The GNU General Public License v3.0"

import argparse
import logging
from AutoDD import *

def main():
    # Instantiate the parser
    parser = argparse.ArgumentParser(description='AutoDD Optional Parameters')

    parser.add_argument('--interval', nargs='?', const=24, type=int, default=24,
                    help='Choose a time interval in hours to filter the results, default is 24 hours')

    parser.add_argument('--sub', nargs='?', const='pennystocks', type=str, default='pennystocks',
                    help='Choose a different subreddit to search for tickers in, default is pennystocks')

    parser.add_argument('--maxprice', nargs='?', const=9999999, type=int, default=9999999,
                    help='Max price of the the ticker results, default is 9999999')

    parser.add_argument('--minprice', nargs='?', const=0, type=int, default=0,
                    help='Min price of the the ticker results, default is 0')

    parser.add_argument('--sort', nargs='?', const=1, type=int, default=1,
                    help='Sort the results table by descending order of score, 1 = sort by total score, 2 = sort by recent score, 3 = sort by previous score, 4 = sort by change in score, 5 = sort by # of rocket emojis')

    parser.add_argument('--min', nargs='?', const=10, type=int, default=10,
                    help='Filter out results that have less than the min score, default is 10')

    parser.add_argument('--yahoo', default=False, action='store_true',
                    help='Using this parameter shows yahoo finance information on the ticker')

    parser.add_argument('--allsub', default=False, action='store_true',
                    help='Using this parameter searchs from one subreddit only, default subreddit is r/pennystocks.')

    parser.add_argument('--csv', default=False, action='store_true',
                    help='Using this parameter produces a table_records.csv file, rather than a .txt file')

    parser.add_argument('--filename', nargs='?', const='table_records', type=str, default='table_records',
                    help='Change the file name from table_records to whatever you wish')

    args = parser.parse_args()

    print("Getting submissions...")
    # call reddit api to get results
    current_tbl, current_rockets, prev_tbl, prev_rockets  = get_submission(args.interval/2, args.sub)  

    print("Populating results...")
    results_tbl = combine_tbl(current_tbl, prev_tbl)

    results_tbl = filter_tbl(results_tbl, args.min)

    print("Counting rockets...")
    results_tbl = append_rocket_tbl(results_tbl, current_rockets, prev_rockets)

    if args.sort == 1:
        results_tbl = sorted(results_tbl, key=lambda x: x[1][0], reverse=True)
    elif args.sort == 2:
        results_tbl = sorted(results_tbl, key=lambda x: x[1][1], reverse=True)
    elif args.sort == 3:
        results_tbl = sorted(results_tbl, key=lambda x: x[1][2], reverse=True)
    elif args.sort == 4:
        results_tbl = sorted(results_tbl, key=lambda x: x[1][3], reverse=True)
    elif args.sort == 5:
        results_tbl = sorted(results_tbl, key=lambda x: x[1][4], reverse=True)

    if args.allsub:
        print("Searching other subreddits...")
        results_from_psaw = get_submission_psaw_allsubs(args.interval/2)  
        for api_result in results_from_psaw:
            results_tbl = additional_filter(results_tbl, api_result)

    print("Getting quick stats...")
    results_tbl = getQuickStats(results_tbl, args.minprice, args.maxprice)

    if args.yahoo:
        print("Getting yahoo finance information...")
        results_tbl = getTickerInfo(results_tbl)

    print_tbl(results_tbl, args.filename, args.allsub, args.yahoo, args.csv)

if __name__ == '__main__':
    main()
    
