
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

import os
import argparse
import math
import re
import sys
import logging
from AutoDD import *

def main():
    # Instantiate the parser
    parser = argparse.ArgumentParser(description='AutoDD Optional Parameters')

    parser.add_argument('--interval', nargs='?', const=24, type=int, default=24,
                    help='Choose a time interval in hours to filter the results, default is 24 hours')

    parser.add_argument('--min', nargs='?', const=10, type=int, default=10,
                    help='Filter out results that have less than the min score, default is 10')

    parser.add_argument('--adv', default=False, action='store_true',
                    help='Using this parameter shows advanced ticker information, running advanced mode is slower')

    parser.add_argument('--sub', nargs='?', const='pennystocks', type=str, default='pennystocks',
                    help='Choose a different subreddit to search for tickers in, default is pennystocks')

    parser.add_argument('--sort', nargs='?', const=1, type=int, default=1,
                    help='Sort the results table by descending order of score, 1 = sort by total score, 2 = sort by recent score, 3 = sort by previous score, 4 = sort by change in score')

    parser.add_argument('--filename', nargs='?', const='table_records.txt', type=str, default='table_records.txt',
                    help='Change the file name from table_records.txt to whatever you wish')

    args = parser.parse_args()

    print("Getting submissions...")
    # call reddit api to get results
    results_from_api = get_submission(args.interval/2, args.sub)  

    print("Searching for tickers...")
    current_tbl, _ = get_freq_list(results_from_api[0])
    prev_tbl, _ = get_freq_list(results_from_api[1])

    print("Populating table...")
    results_tbl = combine_tbl(current_tbl, prev_tbl)

    for api_result in results_from_api[2:]:
        results_tbl = additional_filter(results_tbl, api_result)

    results_tbl = filter_tbl(results_tbl, args.min)

    if args.sort == 1:
        results_tbl = sorted(results_tbl, key=lambda x: x[1][0], reverse=True)
    elif args.sort == 2:
        results_tbl = sorted(results_tbl, key=lambda x: x[1][1], reverse=True)
    elif args.sort == 3:
        results_tbl = sorted(results_tbl, key=lambda x: x[1][2], reverse=True)
    elif args.sort == 4:
        results_tbl = sorted(results_tbl, key=lambda x: x[1][3], reverse=True)

  
    if args.adv:
        print("Getting advanced table...")
        results_tbl = getTickerInfo(results_tbl)

    print_tbl(results_tbl, args.filename)

if __name__ == '__main__':
    main()
    
