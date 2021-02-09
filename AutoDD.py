#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" AutoDD: Automatically does the so called Due Diligence for you. """

#AutoDD - Automatically does the "due diligence" for you.
#Copyright (C) 2021  Fufu Fang, Steven Zhu

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

__author__ = "Fufu Fang kaito1410 Napo2k gobbedy"
__copyright__ = "The GNU General Public License v3.0"

# Native Python imports
import os
import sys
import re
import locale
from datetime import datetime, timedelta
from psaw import PushshiftAPI
import praw
from tabulate import tabulate
from fast_yahoo import *

# dictionary of possible subreddits to search in with their respective column name
subreddit_dict = {'pennystocks': 'pnnystks',
                  'RobinHoodPennyStocks': 'RHPnnyStck',
                  'Daytrading': 'daytrade',
                  'StockMarket': 'stkmrkt',
                  'stocks': 'stocks',
                  'investing': 'investng',
                  'wallstreetbets': 'WSB'}

# note: the following scoring system is tuned to calculate a "popularity" score
# feel free to make adjustments to suit your needs

# x base point of for a ticker that appears on a subreddit title or text body that fits the search criteria
base_points = 4

# x bonus points for each flair matching 'DD' or 'Catalyst' of for a ticker that appears on the subreddit
bonus_points = 2

# every x upvotes on the thread counts for 1 point (rounded down)
upvote_factor = 2

# rocket emoji
rocket = '🚀'

# =================================================================================================
# praw credentials
CLIENT_ID = "3RbFQX8O9UqDCA"
CLIENT_SECRET = "NalOX_ZQqGWP4eYKZv6bPlAb2aWOcA"
USER_AGENT = "subreddit_scraper"

def get_submission_praw(n, sub_dict):

    """
    Returns a list of results for submission in past:
    1st list: current result from n hours ago until now
    2nd list: prev result from 2n hours ago until n hours ago
     """
    mid_interval = datetime.utcnow() - timedelta(hours=n)
    timestamp_mid = mid_interval.timestamp()
    timestamp_start = (mid_interval - timedelta(hours=n)).timestamp()
    timestamp_end = datetime.utcnow().timestamp()

    reddit = praw.Reddit(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, user_agent=USER_AGENT)


    recent = {}
    prev = {}
    for key in sub_dict:
        subreddit = reddit.subreddit(key)
        all_results = []
        # praw limitation gets only 1000 posts
        for post in subreddit.new(limit=1000):
            all_results.append([post.title, post.link_flair_text, post.selftext, post.score, post.created])

        recent[key] = [posts for posts in all_results if posts[4] >= timestamp_mid and posts[4] <= timestamp_end]
        prev[key] = [posts for posts in all_results if posts[4] >= timestamp_start and posts[4] < timestamp_mid]

    return recent, prev

def get_submission_psaw(n, sub_dict):

    """
    Returns a list of results for submission in past:
    1st list: current result from n hours ago until now
    2nd list: prev result from 2n hours ago until n hours ago
     """
    api = PushshiftAPI()

    mid_interval = datetime.today() - timedelta(hours=n)
    timestamp_mid = int(mid_interval.timestamp())
    timestamp_start = int((mid_interval - timedelta(hours=n)).timestamp())
    timestamp_end = int(datetime.today().timestamp())

    recent = {}
    prev = {}
    for key in sub_dict:
        # results from the last n hours
        recent[key] = api.search_submissions(after=timestamp_mid,
                                     before=timestamp_end,
                                     subreddit=key,
                                     filter=['title', 'link_flair_text', 'selftext', 'score'])

        # results from the last 2n hours until n hours ago
        prev[key] = api.search_submissions(after=timestamp_start,
                                     before=timestamp_mid,
                                     subreddit=key,
                                     filter=['title', 'link_flair_text', 'selftext', 'score'])

    return recent, prev

def get_submission_generators(n, sub, allsub, use_psaw):

    """
    Returns two dictionaries:
    1st dictionary: current result from n hours ago until now
    2nd dictionary: prev result from 2n hours ago until n hours ago
    The two dictionaries' keys are the requested subreddit: all subreddits if allsub is True, and just "sub" otherwise
    The value paired with each subreddit key is a generator which traverses each submission
    Note that the generator for each subreddit will only perform http requests when it is traversed, such that this
    function itself does not retrieve any reddit data (merely the generators)
     """

    if sub not in subreddit_dict:
        subreddit_dict[sub] = sub

    sub_dict = {sub:subreddit_dict[sub]}
    if allsub:
        sub_dict = subreddit_dict

    if use_psaw:
        recent, prev = get_submission_psaw(n, sub_dict)

        print("Searching for tickers...")
        current_scores, current_rocket_scores = get_ticker_scores_psaw(recent)
        prev_scores, prev_rocket_scores = get_ticker_scores_psaw(prev)
    else:
        recent, prev = get_submission_praw(n, sub_dict)
        if recent and not prev:
            print('submission results were not found for the previous time period. This may be a popular subreddit with lots of submissions. Try reducing the time interval with the --interval parameter')
        elif not recent and not prev:
            print("praw did not fetch any results for the sub: ")
            print(sub)
            print("try switching to psaw")
        else: 
            print("Searching for tickers...")
            current_scores, current_rocket_scores = get_ticker_scores_praw(recent)
            prev_scores, prev_rocket_scores = get_ticker_scores_praw(prev)  

    return current_scores, current_rocket_scores, prev_scores, prev_rocket_scores

def get_ticker_scores_praw(sub_gen_dict):
    """
    Return two dictionaries:
    --sub_scores_dict: a dictionary of dictionaries. This dictionaries' keys are the requested subreddit: all subreddits
    if args.allsub is True, and just args.sub otherwise. The value paired with each subreddit key is a dictionary of
    scores, where each key is a ticker found in the reddit submissions.
    --rocket_scores_dict: a dictionary whose keys are the tickers found in reddit submissions, and value is the number
    of rocker emojis found for each ticker.

    :param sub_gen_dict: A dictionary of generators for each subreddit, as outputted by get_submission_generators
    """

    # Python regex pattern for stocks codes
    pattern = '(?<=\$)?\\b[A-Z]{3,5}\\b(?:\.[A-Z]{1,2})?'

    # Dictionaries containing the summaries
    sub_scores_dict = {}

    # Dictionaries containing the rocket count
    rocket_scores_dict = {}

    for sub, submission_list in sub_gen_dict.items():

        sub_scores_dict[sub] = {}

        for submission in submission_list:
            # every ticker in the title will earn this base points
            increment = base_points

            # flair is worth bonus points
            if submission[1] is not None:
                if 'DD' in submission[1]:
                    increment += bonus_points
                elif 'Catalyst' in submission[1]:
                    increment += bonus_points
                elif 'technical analysis' in submission[1]:
                    increment += bonus_points

            # every 2 upvotes are worth 1 extra point
            if upvote_factor > 0 and submission[3] is not None:
                increment += math.ceil(submission[3]/upvote_factor)

            # search the title for the ticker/tickers
            title = ' ' + submission[0] + ' '
            title_extracted = set(re.findall(pattern, title))

            # search the text body for the ticker/tickers
            selftext_extracted = set()
            if submission[2] is not None:
                selftext = ' ' + submission[2] + ' '
                selftext_extracted = set(re.findall(pattern, selftext))

            extracted_tickers = selftext_extracted.union(title_extracted)
            extracted_tickers = {ticker.replace('.', '-') for ticker in extracted_tickers}

            count_rocket = title.count(rocket) + selftext.count(rocket)
            for ticker in extracted_tickers:
                rocket_scores_dict[ticker] = rocket_scores_dict.get(ticker, 0) + count_rocket

            # title_extracted is a set, duplicate tickers from the same title counted once only
            for ticker in extracted_tickers:
                sub_scores_dict[sub][ticker] = sub_scores_dict[sub].get(ticker, 0) + increment

    return sub_scores_dict, rocket_scores_dict

def get_ticker_scores_psaw(sub_gen_dict):
    """
    Return two dictionaries:
    --sub_scores_dict: a dictionary of dictionaries. This dictionaries' keys are the requested subreddit: all subreddits
    if args.allsub is True, and just args.sub otherwise. The value paired with each subreddit key is a dictionary of
    scores, where each key is a ticker found in the reddit submissions.
    --rocket_scores_dict: a dictionary whose keys are the tickers found in reddit submissions, and value is the number
    of rocker emojis found for each ticker.

    :param sub_gen_dict: A dictionary of generators for each subreddit, as outputted by get_submission_generators
    """

    # Python regex pattern for stocks codes
    pattern = '(?<=\$)?\\b[A-Z]{3,5}\\b(?:\.[A-Z]{1,2})?'

    # Dictionaries containing the summaries
    sub_scores_dict = {}

    # Dictionaries containing the rocket count
    rocket_scores_dict = {}

    for sub, submission_gen in sub_gen_dict.items():

        sub_scores_dict[sub] = {}

        # looping over each submission
        for submission in submission_gen:

            # every ticker in the title will earn this base points
            increment = base_points

            # flair is worth bonus points
            if hasattr(submission, 'link_flair_text'):
                if 'DD' in submission.link_flair_text:
                    increment += bonus_points
                elif 'Catalyst' in submission.link_flair_text:
                    increment += bonus_points
                elif 'technical analysis' in submission.link_flair_text:
                    increment += bonus_points

            # every 2 upvotes are worth 1 extra point
            if hasattr(submission, 'score') and upvote_factor > 0:
                increment += math.ceil(submission.score / upvote_factor)

            # search the title for the ticker/tickers
            if hasattr(submission, 'title'):
                title = ' ' + submission.title + ' '
                title_extracted = set(re.findall(pattern, title))

            # search the text body for the ticker/tickers
            selftext_extracted = set()
            if hasattr(submission, 'selftext'):
                selftext = ' ' + submission.selftext + ' '
                selftext_extracted = set(re.findall(pattern, selftext))

            extracted_tickers = selftext_extracted.union(title_extracted)
            extracted_tickers = {ticker.replace('.', '-') for ticker in extracted_tickers}

            count_rocket = title.count(rocket) + selftext.count(rocket)
            for ticker in extracted_tickers:
                rocket_scores_dict[ticker] = rocket_scores_dict.get(ticker, 0) + count_rocket

            # title_extracted is a set, duplicate tickers from the same title counted once only
            for ticker in extracted_tickers:
                sub_scores_dict[sub][ticker] = sub_scores_dict[sub].get(ticker, 0) + increment

    return sub_scores_dict, rocket_scores_dict

def populate_df(current_scores_dict, prev_scores_dict, interval):
    """
    Combine two score dictionaries, one from the current time interval, and one from the past time interval
    :returns: the populated dataframe
    """
    dict_result = {}
    total_sub_scores = {}

    for sub, current_sub_scores_dict in current_scores_dict.items():
        total_sub_scores[sub] = {}
        for symbol, current_score in current_sub_scores_dict.items():
            if symbol in dict_result.keys():
                dict_result[symbol][0] += current_score
                dict_result[symbol][1] += current_score
                dict_result[symbol][3] += current_score
            else:
                dict_result[symbol] = [current_score, current_score, 0, current_score]
            total_sub_scores[sub][symbol] = total_sub_scores[sub].get(symbol, 0) + current_score

    for sub, prev_sub_scores_dict in prev_scores_dict.items():
        for symbol, prev_score in prev_sub_scores_dict.items():
            if symbol in dict_result.keys():
                dict_result[symbol][0] += prev_score
                dict_result[symbol][2] += prev_score
                dict_result[symbol][3] -= prev_score
            else:
                dict_result[symbol] = [prev_score, 0, prev_score, -prev_score]
            total_sub_scores[sub][symbol] = total_sub_scores[sub].get(symbol, 0) + prev_score

    first_col = str(interval) + 'H Total'
    columns = [first_col, 'Recent', 'Prev', 'Change']
    df = pd.DataFrame.from_dict(dict_result, orient='index', columns=columns)

    if len(current_scores_dict) > 1:
        dtype_dict = {}
        for sub, total_score_dict in total_sub_scores.items():
            # add each total score dict as new column of df
            df[sub] = pd.Series(total_score_dict)
            # pandas will insert NaN for missing symbols, which converts entire column to float
            # will use the below dict to convert these columns back to int
            dtype_dict[sub] = 'int32'
        df = df.fillna(value=0).astype(dtype_dict)

    return df

def filter_df(df, min_val):
    """
    Filter the score dataframe

    :param dataframe df: the dataframe to be filtered
    :param int min_val: the minimum total score
    :returns: the filtered dataframe
    """
    BANNED_WORDS = [
        'THE', 'FUCK', 'ING', 'CEO', 'USD', 'WSB', 'FDA', 'NEWS', 'FOR', 'YOU', 'AMTES', 'WILL', 'CDT', 'SUPPO',
        'MERGE', 'BUY', 'HIGH', 'ADS', 'FOMO', 'THIS', 'OTC', 'ELI', 'IMO', 'TLDR', 'SHIT', 'ETF', 'BOOM', 'THANK',
        'PPP', 'REIT', 'HOT', 'MAYBE', 'AKA', 'CBS', 'SEC', 'NOW', 'OVER', 'ROPE', 'MOON', 'SSR', 'HOLD', 'SELL',
        'COVID', 'GROUP', 'MONDA', 'USA', 'YOLO', 'MUSK', 'AND', 'STONK', 'ELON', 'CAD', 'WIN', 'GET', 'BETS', 'INTO',
        'JUST', 'MAKE', 'NEED', 'BIG', 'STONK', 'ELON', 'CAD', 'OUT', 'TOP', 'ALL', 'ATH', 'ANY', 'AIM', 'IPO', 'EDIT'
    ]

    # compares the first column, which is the total score to the min val
    df = df[df.iloc[:, 0] >= min_val]
    drop_index = pd.Index(BANNED_WORDS).intersection(df.index)
    df = df.drop(index=drop_index)
    return df

def get_financial_stats(results_df, threads=True, advanced=False):

    # TODO: should be able to build the smarts so that a single dictionary necessary, and download_advanced_stats
    # function should be able to figure out which yahoo module the stat belongs to

    # dictionary of ticker summary profile information to get from yahoo
    summary_profile_measures = {'industry': 'Industry'}

    # dictionary of ticker financial information to get from yahoo
    financial_measures = {'currentPrice': 'Price', 'quickRatio': 'QckRatio', 'currentRatio': 'CrntRatio',
                          'targetMeanPrice': 'Trgtmean', 'recommendationKey': 'Recommend'}

    # dictionary of ticker summary information to get from yahoo
    summary_measures = {'previousClose': 'prvCls', 'open': 'open', 'dayLow': 'daylow', 'dayHigh': 'dayhigh',
                        'payoutRatio': 'pytRatio', 'forwardPE': 'forwardPE', 'beta': 'beta', 'bidSize': 'bidSize',
                        'askSize': 'askSize', 'volume': 'volume', 'averageVolume': '3mAvgVol',
                        'averageVolume10days': 'avgvlmn10', 'fiftyDayAverage': '50dayavg',
                        'twoHundredDayAverage': '200dayavg'}

    # dictionary of ticker key stats summary
    key_stats_measures = {'shortPercentOfFloat': 'Short/Float%'}

    # mapping of yahoo module names to dictionaries containing data we want to retrieve
    module_name_map = {'summaryProfile': summary_profile_measures, 'defaultKeyStatistics': key_stats_measures}

    if advanced:
        module_name_map.update({'summaryDetail': summary_measures, 'financialData': financial_measures})

    # check for valid symbols and get quick stats
    ticker_list = list(results_df.index.values)
    quick_stats_df = get_quick_stats(ticker_list, threads)
    valid_ticker_list = list(quick_stats_df.index.values)

    summary_stats_df = download_advanced_stats(valid_ticker_list, module_name_map, threads)
    results_df_valid = results_df.loc[valid_ticker_list]
    results_df = pd.concat([results_df_valid, quick_stats_df, summary_stats_df], axis=1)
    results_df.index.name = 'Ticker'

    return results_df

def get_quick_stats(ticker_list, threads=True):

    quick_stats = {'regularMarketPreviousClose': 'prvCls', 'fiftyDayAverage': '50DayAvg',
                   'regularMarketVolume': 'Volume', 'averageDailyVolume3Month': '3MonthVolAvg',
                   'regularMarketPrice': 'price', 'regularMarketChangePercent': '1DayChange%', 
                   'floatShares': 'float'}

    unprocessed_df = download_quick_stats(ticker_list, quick_stats, threads)

    processed_stats_table = []
    # TODO: if looping over rows becomes slow: vectorize. (Tested with 270 symbols and it's practically instantaneous)
    # See https://engineering.upside.com/a-beginners-guide-to-optimizing-pandas-code-for-speed-c09ef2c6a4d6
    for index, row in unprocessed_df.iterrows():
        symbol = index
        prev_close = row['prvCls']
        avg50day = row['50DayAvg']
        volume = row['Volume']
        avg_vol = row['3MonthVolAvg']
        price = row['price']
        day_change = row['1DayChange%']
        stock_float = row['float']

        valid = False
        if price != "N/A" and price != 0:
            valid = True

        if day_change != "N/A" and day_change != 0 or (day_change == 0 and price == prev_close):
            day_change = "{:.3f}".format(day_change)
            if day_change != 0:
                valid = True
        elif prev_close != "N/A" and prev_close != 0 and price != "N/A":
            day_change = ((float(price) - float(prev_close))/float(prev_close))*100
            day_change = "{:.3f}".format(day_change)
            if day_change != 0:
                valid = True

        change_50day = 0
        if price != "N/A" and price != 0:
            if avg50day != "N/A" and avg50day > 0:
                change_50day = ((float(price) - float(avg50day))/float(avg50day))*100
            else:
                change_50day = 0

        if change_50day != 0:
            change_50day = "{:.3f}".format(change_50day)

        change_vol = 0
        if volume != "N/A" and avg_vol != "N/A":
            if avg_vol != 0 and volume != 0:
                valid = True
                change_vol = ((float(volume) - float(avg_vol))/float(avg_vol))*100

        if change_vol != 0:
            change_vol = "{:.3f}".format(change_vol)

        if stock_float != "N/A":
                stock_float = stock_float
                valid = True

        # if the ticker has any valid column, append
        if valid:
            stat_list = [symbol, price, day_change, change_50day, change_vol, stock_float]
            processed_stats_table.append(stat_list)

    # construct dataframe
    columns = ['Symbol', 'Price', '1DayChange%', '50DayChange%', 'ChangeVol%', 'Float Shares']
    stats_df = pd.DataFrame(processed_stats_table, columns=columns)
    stats_df.set_index('Symbol', inplace=True)

    return stats_df

def print_df(df, filename, writecsv):

    # turn index (symbols) into regular column for printing purposes
    df.reset_index(inplace=True)

    now = datetime.now()
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    # save the file to the same dir as the AutoDD.py script
    completeName = os.path.join(sys.path[0], filename)

    if writecsv:
        completeName += '.csv'
        df.to_csv(completeName, index=False, float_format='%.3f', mode='a', encoding=locale.getpreferredencoding())
        print(file=open(completeName, "a"))
    else:
        completeName += '.txt'
        with open(completeName, "a") as file:
            file.write("date and time now = ")
            file.write(dt_string)
            file.write('\n')
            file.write(tabulate(df, headers='keys', floatfmt='.3f', showindex=False))
            file.write('\n\n')

    print("Wrote to file successfully: ")
    print(completeName)
