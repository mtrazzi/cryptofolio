import os
import time
import numpy as np
import pandas as pd
import tensorflow as tf
from datetime import datetime
from random import randint
from pgportfolio.marketdata.poloniex import Poloniex
from pgportfolio.learn.nnagent import NNAgent
from pgportfolio.tools.data import get_type_list, get_chart_until_success
from pgportfolio.tools.configprocess import load_config
from pgportfolio.tools.trade import calculate_pv_after_commission
# from pgportfolio.tdagent.algorithms import crp, olmar, up, anticor1, pamr, best, bk, cwmr_std, eg, sp, ubah, wmamr, bcrp, cornk, m0, rmr

# Given a Poloniex object (to read Poloniex API), outputs a dataframe with coins infomation
def create_coinlist(polo):
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
def create_data(coin, coin_list, polo, start, end, period):

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
def create_history(coin_list, chosen_coins, polo, start, end, period, features):
    start = int(start - (start%period))
    end = int(end - (end%period))
    f = len(features)
    l = len(chosen_coins)
    d = int((end - start)/period)
    dico = dict()
    # Retrieve data
    for coin in chosen_coins:
        dico[coin] = create_data(coin, coin_list, polo, start, end, period)
    # Construct matrix
    res = np.zeros((f, l, d+1))
    for c, coin in enumerate(chosen_coins):
        for i, feature in enumerate(features):
            for date in range(d+1):
                res[i, c, date] = dico[coin][date][feature]
    return res

# Given the chosen network, coins, date, and current portfolio, outputs a new one
def predict_portfolio(algo, chosen_coins, date, old_omega):

    # Set config
    config = load_config(algo)
    net_dir = "./train_package/" + algo + "/netfile"
    input_config = config["input"]
    feature_number=input_config["feature_number"]
    period=input_config["global_period"]
    features = get_type_list(feature_number)

    # Set start and end times for retrieving data
    end = int(date - (date%period)) # converts into closest smaller interval
    start = end - 30*period # setting start to 30 periods before end
    start = int(start - (start%period))

    # Create history matrix
    polo = Poloniex() # a class to retrieve online data
    coin_list = create_coinlist(polo) # a pandas dataframe with coins (index), pair, volume, price (BTC)
    history = create_history(coin_list, chosen_coins, polo, start, end, period, features)

    # Generate new omega
    os.environ["CUDA_VISIBLE_DEVICES"] = ""
    with tf.device("/cpu:0"):
        myAgent = NNAgent(config=config, restore_dir=net_dir, device="cpu")
    print(history.shape)
    print(old_omega.shape)
    omega = myAgent.decide_by_history(history, old_omega)

    return omega1

def main():
    now = time.time()
    polo = Poloniex()
    coin_list = create_coinlist(polo)
    all_coins = coin_list.index.tolist()
    print("Chose your coins:", all_coins)
    chosen_coins = ['reversed_USDT', 'ETH', 'XRP', 'STR', 'XMR', 'LTC', 'BCH', 'DASH', 'BTS', 'XEM', 'ETC']
    omega = [randint(0,100) for x in range(len(chosen_coins)+1)]
    omega = np.array([x/sum(omega) for x in omega])
    new_omega = predict_portfolio(algo='8', chosen_coins=chosen_coins, date=now, old_omega=omega)
    print("Omega:", new_omega)

if __name__ == "__main__":
    main()
