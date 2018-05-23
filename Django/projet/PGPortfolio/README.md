This code is part of the implementation of the project "Cryptofolio" by Julien Denes and Michael Trazzi.
It is largely based on the original implementation of the paper "A Deep Reinforcement Learning Framework for the Financial Portfolio Management Problem" ([arXiv:1706.10059](https://arxiv.org/abs/1706.10059)).

* The deep reinforcement learning framework is the core part of the library.
The method is basically the policy gradient on immediate reward.
 One can configurate the topology, training method or input data in a separate json file. The training process will be recorded and user can visualize the training using tensorboard.
Result summary and parallel training are allowed for better hyper-parameters optimization.
* The financial-model-based portfolio management algorithms are also embedded in this library for comparision purpose, whose implementation is based on Li and Hoi's toolkit [OLPS](https://github.com/OLPS/OLPS).

## Platform Support
Python 3.5+ in windows and Python 2.7+/3.5+ in linux are supported.

## Dependencies
Install Dependencies via `pip install -r requirements.txt`

* tensorflow (>= 1.0.0)
* tflearn
* pandas
* ...

## User Guide
Please check out [User Guide](user_guide.md)

## Acknowledgement
This project would not have been finished without using the codes from the following open source projects:
* [Original source (PGPortfolio)](https://github.com/ZhengyaoJiang/PGPortfolio)
* [Online Portfolio Selection toolbox](https://github.com/OLPS/OLPS)

## Risk Disclaimer (for Live-trading)

There is always risk of loss in trading. **All trading strategies are used at your own risk**

*The volumes of many cryptocurrency markets are still low. Market impact and slippage may badly affect the results during live trading.*
