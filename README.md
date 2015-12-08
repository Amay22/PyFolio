# PyFolio
### OVERVIEW:
PyFolio is a free web application designed to provide trading simulations to users and it is built on Python Django Framework. PyFolio uses real-time stock market data to paint the most accurate picture of investment portfolios customized for perspective investors. It allows users to design their own portfolios and display quantitative factors with highly visualized graphs and charts.
### TARGET AUDIENCE:
Our target audience includes anyone and everyone who is interested in stock investing. Whether you are new to the stock market and want to test the water before turning to a stockbroker, or you are a student interested in investing and looking for a place to do market simulation, or you are an experienced independent stock trader looking for a place to test out different portfolio strategies but don’t have access to the tools, PyFolio is the right place for you.
### FEATURES:
* Leverages a user friendly interface
  * Straightforward buttons to look up stocks and buy/sell certain number of shares
  * “Money Spent” and “Money Earned” help to keep track of users’ profit and loss
* Displays accurate and real-time stock market data for each individual stock in the portfolio. Individual stock details include:
  * Basic information include open price, market cap, volume, EPS, etc.
  * Financial Ratios include P/E ratio, Price/Book ratio, short ratio, etc.
  * Real Time Data include real time market cap, ask price, bid price, etc.
  * Changes and Trends include 50 days, 200 days, and yearly moving average
  * Additional Information include year high/low price, last dividend date, etc.
* Provides highly visualized graphs and charts to analyze portfolio performance. Portfolio details include:
  * Portfolio OHLC & Volume
  * Portfolio Time vs. Value
  * Portfolio Historical Data
* Provides relevant up-to-date news based on users’ portfolio
  * Stock related news
  * Industry related news

### ADVANTAGES:
* Completely free of charge
* Open sources (Project available on GitHub)
* User-Friendly and self-explanatory (No need to know big financial terms)
* Highly visualized information customized to users’ needs

In summary, PyFolio is a one-stop shop for users to gather data, news, and analysis in order to build value-adding portfolios. It is practical and useful in many ways. Hope you will enjoy using PyFolio. Please [read our Wiki page](https://github.com/Amay22/PyFolio/wiki)

### HOW TO RUN:

First, make sure below items have been installed before running the application

1. Install node if haven't done so already. Use [Homebrew](http://brew.sh/) for Mac OS or [Choclatey](https://chocolatey.org/) for Windows.

For Mac OS use [Homebrew](http://brew.sh/).

```
brew install node
```

For Windows use [Choclatey](https://chocolatey.org/).

```
choco install nodejs
```


2. install coffee if haven't done so already.

```
sudo npm install -g coffee-script
```

3. Install the requirement packages for PyFolio

```
pip install –r requirments.txt
```

Then use the below commands to run the application:

Make Migrations to update changes on the database.

```
python manage.py makemigrations
```
Migrate to the to make all the changes on the database.

```
python manage.py migrate
```

Repeat the two steps if there is any change to any of the models.py

This step is to run the application on the localhost server.

```
python manage.py runserver
```




