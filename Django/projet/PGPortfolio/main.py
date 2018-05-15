import os
import time
import importlib
import json
import numpy as np
import pandas as pd
import tensorflow as tf
from datetime import datetime
from random import randint
from pgportfolio.tools.configprocess import parse_time
from pgportfolio.marketdata.poloniex import Poloniex
from pgportfolio.learn.nnagent import NNAgent
from pgportfolio.tools.data import get_type_list, get_chart_until_success
from pgportfolio.tools.configprocess import load_config

# from pgportfolio.tools.trade import calculate_pv_after_commission
global valid_algorithms
valid_algorithms = ['anticor1', 'bcrp', 'best', 'bk', 'cornk', 'crp', 'cwmr_std', 'eg', 'm0', 'olmar', 'pamr', 'rmr', 'sp', 'ubah', 'up', 'wmamr']

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
def predict_portfolio(algo, chosen_coins, date, old_omega):

    # Set config
    if algo.isdigit():
        config = load_config(algo)
    else:
        with open("pgportfolio/net_config.json") as file: config = json.load(file)

    input_config = config["input"]
    feature_number = input_config["feature_number"]
    period = input_config["global_period"]
    volume = input_config["volume_average_days"]
    features = get_type_list(feature_number)

    # Set start and end times for retrieving data
    if algo.isdigit():
        net_dir = "/home/michael/cryptofolio/Django/projet/PGPortfolio/train_package/" + algo + "/netfile"
        end = int(date - (date%period)) # converts into closest smaller interval
        start = end - volume*period # setting start to 30 periods before end
        start = int(start - (start%period))
    elif algo in ['bcrp', 'best']:
        end = int(date - (date%period)) # converts into closest smaller interval
        start = end - 90*volume*period # setting start to 2700 periods before end (special algos)
        start = int(start - (start%period))
    else:
        end = int(date - (date%period)) # converts into closest smaller interval
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

    return omega

def main():
    # Chose time (should be "now")
    now = time.time()
    # A way to get a list all available coins (e.g. to let the user chose his coins)
    coin_list = create_coinlist()
    all_coins = coin_list.index.tolist()
    print("Available coins:", all_coins)
    # The list of all implemented valid_algorithms, '8' is a trained NN (example)
    print("Available algorithms:", ['8'] + valid_algorithms)
    # A fake choice of algorithm, should be chosen by the user
    algo = '8'
    # A fake portfolio, should be the cryptocurrencies chosen by the user
    chosen_coins = ['reversed_USDT', 'ETH', 'XRP', 'STR', 'XMR', 'LTC', 'BCH', 'DASH', 'BTS', 'XEM', 'ETC']
    # A fake old omega (portfolio repartition), again should be previous one or chosen by user
    omega = [randint(0,100) for x in range(len(chosen_coins)+1)]
    omega = np.array([x/sum(omega) for x in omega])
    ##### THIS IS THE VERY IMPORTANT FUNCTION #####
    new_omega = predict_portfolio(algo=algo, chosen_coins=chosen_coins, date=now, old_omega=omega)
    ###############################################
    print("Omega:", new_omega)
    print("Computation time:", time.time()-now)

    return new_omega

if __name__ == "__main__":
    main()