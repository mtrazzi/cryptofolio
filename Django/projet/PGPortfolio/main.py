import os
import time
import importlib
import json
import numpy as np
import pandas as pd
import tensorflow as tf
from datetime import datetime
from random import randint
from pgportfolio.tools.configprocess import parse_time, load_config
from pgportfolio.marketdata.poloniex import Poloniex
from pgportfolio.learn.nnagent import NNAgent
from pgportfolio.tools.data import get_type_list, get_chart_until_success
import random

# from pgportfolio.tools.trade import calculate_pv_after_commission
global valid_algorithms
valid_algorithms = ['anticor1', 'bcrp', 'best', 'bk', 'cornk', 'crp', 'cwmr_std', 'eg', 'm0', 'olmar', 'olmar2', 'pamr', 'rmr', 'sp', 'ubah', 'up', 'wmamr']

# Given a Poloniex object (to read Poloniex API), outputs a dataframe with coins infomation
def create_coinlist():
    polo = Poloniex()
    vol = polo.marketVolume()
    ticker = polo.marketTicker()
    pairs = []
    coins =  []
    volumes = []
    prices = []
    for k, v in vol.items():
        if k.startswith("BTC_") or k.endswith("_BTC"):
            pairs.append(k)
            for c, val in v.items():
                if c != 'BTC':
                    if k.endswith('_BTC'):
                        coins.append('reversed_' + c)
                        prices.append(1.0 / float(ticker[k]['last']))
                    else:
                        coins.append(c)
                        prices.append(float(ticker[k]['last']))
                else:
                    volumes.append(0.0)
    coin_list = pd.DataFrame({'coin': coins, 'pair': pairs, 'volume': volumes, 'price':prices})
    coin_list = coin_list.set_index('coin')
    return coin_list


# Given various parameters, outputs a list of dictionnaries with informations about the coin between the 2 dates
def create_data(coin, coin_list, start, end, period):
    polo = Poloniex()
    chart = get_chart_until_success(polo=polo, pair=coin_list.at[coin, 'pair'], start=start, end=end, period=period)
    for c in chart:
        if c["date"] > 0:
            if c['weightedAverage'] == 0: c['weightedAverage'] = c['close']

            # NOTE here the USDT is in reversed order
            if 'reversed_' in coin:
                c['low'], c['high'], c['open'] = 1.0/c['low'], 1.0/c['high'], 1.0/c['open']
                c['close'], c['weightedAverage'] = 1.0/c['close'], 1.0/c['weightedAverage']
    return chart

# Given various parameters, outputs a History matrix to be used for portfolio prediction
def create_history(coin_list, chosen_coins, start, end, period, features):
    f = len(features)
    l = len(chosen_coins)
    dico = dict()
    # Retrieve data
    for coin in chosen_coins:
        dico[coin] = create_data(coin, coin_list, start, end, period)
    # Construct matrix
    d = len(dico[chosen_coins[0]])
    res = np.zeros((f, l, d))
    for c, coin in enumerate(chosen_coins):
        for i, feature in enumerate(features):
            for date in range(d):
                # print(len(dico[coin]), date)
                x = dico[coin][date][feature]
                res[i, c, date] = x
    return res

# Given the chosen network, coins, date, and current portfolio, outputs a new one
def predict_portfolio(algo, investment, chosen_coins, date, old_omega):

    # Set config
    if algo.isdigit():
        config = load_config(algo)
    else:
        with open("/home/michael/cryptofolio/Django/projet/PGPortfolio/pgportfolio/net_config.json") as file: config = json.load(file)

    input_config = config["input"]
    feature_number = input_config["feature_number"]
    period = input_config["global_period"]
    volume = input_config["volume_average_days"]
    features = get_type_list(feature_number)

    # Set start and end times for retrieving data
    date = date - 300*(date%period < 300)
    end = int(date - (date%period)) # converts into closest round time, minus 5 min if too close from it

    if algo.isdigit():
        # Use absolute path, to change to your configuration
        train_package_path = "/home/michael/cryptofolio/Django/projet/PGPortfolio/train_package/"
        net_dir = train_package_path + algo + "/netfile"
        start = end - volume*period # setting start to 30 periods before end
        start = int(start - (start%period))
    elif algo in ['bcrp', 'best']:
        start = end - 90*volume*period # setting start to 2700 periods before end (special algos)
        start = int(start - (start%period))
    else:
        start = end - volume*period # setting start to 30 periods before end
        start = int(start - (start%period))

    # Create history matrix
    coin_list = create_coinlist() # a pandas dataframe with coins (index), pair, volume, price (in BTC)
    history = create_history(coin_list, chosen_coins, start, end, period, features) # history matrix

    # Generate new omega
    if algo.isdigit():
        os.environ["CUDA_VISIBLE_DEVICES"] = ""
        with tf.device("/cpu:0"):
            myAgent = NNAgent(config=config, restore_dir=net_dir, device="cpu")
        omega = myAgent.decide_by_history(history, old_omega)

    elif algo in valid_algorithms:
        package = importlib.import_module("pgportfolio.tdagent.algorithms." + algo)
        myAgent = getattr(package, algo.upper())()
        y = (history[0, :, 1:] / history[0, :, :-1])
        y = np.concatenate((np.ones((1, y.shape[1])), y), axis=0)
        omega = myAgent.decide_by_history(y.T, old_omega)
    else:
        print("Invalid algorithm")
        omega = None

    # Current BTC per Currency price (transformed into Currency per BTC)
    v = 1.0 / history[0, :, -1]
    v = np.concatenate((np.zeros(1), v), axis=0)
    # Round omega to percentage
    round_omega = np.around(omega, decimals=1)
    # Compute omega in term of currencies, not percentage
    portfolio = investment * round_omega * v
    return portfolio, round_omega


# Computes value of a portfolio, given either in percentage or number of coins at any given date
def compute_value(portfolio, chosen_coins, investment, date):

    # Get data
    date = date - 300
    end = int(date - (date%300))
    start = end - 300
    period = 300
    features = ['close']
    coin_list = create_coinlist() # a pandas dataframe with coins (index), pair, volume, price (in BTC)
    history = create_history(coin_list, chosen_coins, start, end, period, features) # history matrix

    # If in proportions: transform to coin numbers
    if np.around(np.sum(portfolio)) == 1.0:
        v = 1.0 / history[0, :, -1]
        v = np.concatenate((np.zeros(1), v), axis=0)
        portfolio = investment * portfolio * v

    # If (or when) in term of coin number: return value in BTC
    v = history[0, :, -1]
    v = np.concatenate((np.zeros(1), v), axis=0)
    res = np.dot(portfolio, v)
    return np.around(res, decimals=10)

def process(algo="8"):
    if (algo=="random"):
        portfolio = [random.random() for i in (range(12))]
        return portfolio, (1/sum(portfolio)) * np.array(portfolio)
    print("using algo: ", algo)
    # Chose time (should be "now")
    now = time.time()
    # A way to get a list all available coins (e.g. to let the user chose his coins)
    coin_list = create_coinlist()
    all_coins = coin_list.index.tolist()
    print("Available coins:", all_coins)
    # The list of all implemented valid_algorithms, '8' is a trained NN (example)
    print("Available algorithms:", ['8'] + valid_algorithms)
    # A fake portfolio, should be the cryptocurrencies chosen by the user
    chosen_coins = ['reversed_USDT', 'ETH', 'XRP', 'STR', 'XMR', 'LTC', 'BCH', 'DASH', 'BTS', 'XEM', 'ETC']
    # A fake old omega (portfolio repartition), again should be previous one or chosen by user
    omega = np.zeros(len(chosen_coins)+1)
    omega[0] = 1
    # A fake amount of BTC to invest at the beginning
    investment = 0.04785
    ##### THIS IS THE VERY IMPORTANT FUNCTION #####
    new_omega = predict_portfolio(algo=algo, investment=investment, chosen_coins=chosen_coins, date=int(now), old_omega=omega)
    ###############################################
    # Set commission, 0.0025 if Poloniex
    commission_rate = 0.0025
    # Compute value and print
    investment = compute_value(portfolio=new_omega[0], chosen_coins=chosen_coins, investment=investment, date=now)
    print("New omega is:", new_omega[0], "with value:", investment)
    print("portfolio is:", new_omega[1])
    print("Computation time:", time.time()-now)

    return list(new_omega[0]), new_omega[1]

def main():
    process('bcrp')

if __name__ == "__main__":
    main()
