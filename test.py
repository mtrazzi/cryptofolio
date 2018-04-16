from __future__ import absolute_import, division, print_function
import json
import logging
import os
import time
import numpy as np
import pandas as pd
from argparse import ArgumentParser
from datetime import datetime
from random import randint

from pgportfolio.tools.configprocess import preprocess_config
from pgportfolio.tools.configprocess import load_config
from pgportfolio.tools.trade import save_test_data
from pgportfolio.tools.trade import calculate_pv_after_commission
from pgportfolio.tools.shortcut import execute_backtest
from pgportfolio.resultprocess import plot
from pgportfolio.trade.backtest import BackTest
from pgportfolio.tdagent.algorithms import crp, olmar, up, anticor1, pamr, best, bk, cwmr_std, eg, sp, ubah, wmamr, bcrp, cornk, m0, rmr
from pgportfolio.trade import trader
from pgportfolio.marketdata.datamatrices import DataMatrices
from pgportfolio.learn.rollingtrainer import RollingTrainer
from main import build_parser

"""
1. main.py : on appelle "execute_backtest(options.algo, config)" (dans shortcut.py) avec comme arg :
    * options.algo = le numéro de l'instance
    * config = son net.config.json correspondant ; config = load_config(algo)

2. shortcut.py : on construit "backtester = BackTest(config, agent=agent, agent_type=agent_type, net_dir=net_dir)" (dans backtest.py) avec comme arg
    * config = toujours pareil
    * agent = None
    * agent_type = "nn"
    * net_dir = "./train_package/" + algo + "/netfile" (algo c'est options.algo)
    /!\ l'objet Backtester hérite de Trader (trader.py)

3. shortcut.py : on appelle "backtester.start_trading()" (dans trader.py car hérite de Trader)
    * lui-même itère self._total_steps fois la méthode "__trade_body" (dans trader.py aussi)

4. trader.py : __trade_body(self) : 3 étapes :
    a. omega = self._agent.decide_by_history(), avec paramètres :
        * self.generate_history_matrix() (depuis backtest.py) :
            ** retourne self.__test_set["X"][self._steps]
            ** self.__test_set = data_matrices.get_test_set()
            ** data_matrices = self._rolling_trainer.data_matrices
            ** self._rolling_trainer = RollingTrainer(config, net_dir, agent=agent)
            ** data_matrices retourne self._matrix
            ** self._matrix = DataMatrices.create_from_config(config) => voir datamatrices.py
        * self._last_omega.copy() = le omega (vecteur de poids) précédent
    b. self.trade_by_strategy(omega) (depuis backtest.py) :
        * update la valeur de self._last_omega (avec commission)
        * calcule la valeur du portfolio
    c. self.rolling_train() (depuis backtest.py) :
        * appelle self._rolling_trainer.rolling_train() (voir rollingtrainer.py)
        * qui appelle self._agent.train(x, y, last_w, w) avec x, y, last_w, w = self.next_batch()
        * _agent est un NNAgent, appelle sa méthode train (dans nnagent.py) => juste pour réentrainter le réseau mais osef
"""

algo = '8'
config = load_config(algo)
config["input"]['start_date'] = '2018/04/05'
config["input"]['end_date'] = '2018/04/07'
config["input"]['global_period'] = 1800
config["input"]['test_portion'] = 0.5
print("Config:", config)
net_dir = "./train_package/" + algo + "/netfile"
backtester = BackTest(config, agent=None, agent_type='nn', net_dir=net_dir)
print("----- Starting to trade -----")
total_steps = backtester._total_steps
backtester._steps = randint(0,total_steps)
print("Total steps:", total_steps)
print("Date:", backtester._steps)
omeg = [randint(0,100) for x in range(backtester._last_omega.shape[0])]
sum_omeg = sum(omeg)
backtester._last_omega = np.array([x/sum_omeg for x in omeg])
print("Old omega:", backtester._last_omega)
omega = backtester._agent.decide_by_history(backtester.generate_history_matrix(), backtester._last_omega.copy())
print("New omega:", omega)
