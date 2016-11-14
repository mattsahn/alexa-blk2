import logging
import requests
import json
from random import randint

from flask import Flask, render_template

from flask_ask import Ask, statement, question, session


app = Flask(__name__)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)


@ask.launch

def new_game():

    welcome_msg = render_template('welcome')

    return question(welcome_msg)

@ask.intent("StockInfoIntent")

def stock_info(ticker):

    print(ticker)
    StockRequest = requests.get("https://www.blackrock.com/tools/hackathon/security-data", params= {'identifiers':ticker})

    data = json.loads(StockRequest.text)

    print("json loaded")

    if (data["success"] != True):
        print("security not found. exiting")
        return question("I could not find that security. Please try again")

    assetType = data["resultMap"]["SECURITY"][0]["assetType"]

    print(assetType)

    if(assetType == "Stock"):
        print(ticker + " is a stock")
        description =  data["resultMap"]["SECURITY"][0]["description"]
        peRatio =  data["resultMap"]["SECURITY"][0]["peRatio"]
        #msg = ticker + " is the stock for " + description + ". It has a P E ratio of " + str(peRatio)
        msg = render_template('stockInfo',ticker=ticker,description=description,peRatio=str(peRatio))

    if(assetType == "Fund"):
        print("this is a fund")
        morningstarCategory = data["resultMap"]["SECURITY"][0]["characteristicsMap"]["morningstarCategory"]
        print(morningstarCategory)
        msg = ticker + " is a " + morningstarCategory + " fund"
   
    return question(msg) 

#@ask.intent("YesIntent")

#def next_round():

#    numbers = [randint(0, 9) for _ in range(3)]

#    round_msg = render_template('round', numbers=numbers)

#    session.attributes['numbers'] = numbers[::-1]  # reverse

#    return question(round_msg)


#@ask.intent("AnswerIntent", convert={'first': int, 'second': int, 'third': int})

#def answer(first, second, third):

#    winning_numbers = session.attributes['numbers']

#    if [first, second, third] == winning_numbers:

#        msg = render_template('win')

#    else:

#        msg = render_template('lose')

#    return statement(msg)

@ask.intent("AMAZON.StopIntent")

def stop():
    return statement("Goodbye.")

if __name__ == '__main__':

    app.run(debug=True)
