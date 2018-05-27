# Cryptofolio: an optimization platform for cryptocurrencies portfolios.

**Authors:** Julien Denes ([jdenes](https://github.com/jdenes)), Michael Trazzi ([mtrazzi](https://github.com/mtrazzi))

**Visit the landing page of the platform [here](https://michaeltrazzi.wixsite.com/cryptoptimisation)!**

This repository is the final result of project "Cryptofolio", an applied project for Université Pierre et Marie Curie (UPMC) Master's Degree in Computer Science. More information [here](http://androide.lip6.fr/?q=node/384) (in french).

The overall goal of the platform is to provide cryptocurrencies investor with a decision aid on how to create a diversified portfolio to maximize returns and minimize risks.
Several optimization algorithms are proposed, from traditional high-frequency live trading to state-of-the-art Convolutional Neural Network (CNN).

## Structure of the repository
* [Django](Django): source code of our platform, implemented with Python Django. The section of the code dedicated to portfolio optimization is [here](Django/projet/PGPortfolio).
* [Literature](Literature): most of the literature we based our theoretical choices on is available on this folder.
* [Report](Rapport): a complete exposition of our study of the algorithms and development steps, in particular in [the final report](Rapport/Rapport.pdf) and in the specifications (cahier des charges) (in french).
* [Other material](Material): various deprecated material used during the development of the platform, including: tryouts with R Shiny, unused datasets, figures and notes from tryouts with algorithms.

## Access the platform
The landing page of the platform is available [here](https://michaeltrazzi.wixsite.com/cryptoptimisation) and the application [here](https://cryptoptimize.herokuapp.com/).

## Acknowledgement and sources
This project would not have been finished without using the codes from the following open source projects:
* [Original source code (PGPortfolio)](https://github.com/ZhengyaoJiang/PGPortfolio)
* [Online Portfolio Selection toolbox](https://github.com/OLPS/OLPS)

## License
This software is available under a [GNU General Public License](LICENSE).

## Risk disclaimer
There is always a high risk of loss in trading cryptocurrencies. All suggestions from this platform are followed at your own risk.