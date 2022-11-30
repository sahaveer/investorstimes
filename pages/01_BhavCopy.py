import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import datetime
from datetime import date,timedelta
import EOD
import random
from streamlit_lottie import st_lottie
from streamlit_lottie import st_lottie_spinner


stock_quotes = [
"""'I have two basic rules about winning in trading as well as in life:\n1. If you don’t bet, you can’t win.\n2. If you lose all your chips, you can’t bet.' \n\n– Larry Hite""",
"""'When you genuinely accept the risks, you will be at peace with any outcome.'\n – Mark Douglas""",
"""'By living the philosophy that my winners are always in front of me, it is not so painful to take a loss.' \n– Marty Schwartz""",
"""'The trend is your friend until the end when it bends.' \n– Ed Seykota""",
"""'The secret to being successful from a trading perspective is to have an indefatigable and an undying and unquenchable thirst for information and knowledge.'\n-Paul Tudor Jones""",
"""'Wide diversification is only required when investors do not understand what they are doing.'\n– Warren Buffett""",
"""'If you don’t respect risk, eventually they’ll carry you out.'\n– Larry Hite""",
"""'Opportunities come infrequently. When it rains gold put out a bucket not a thimble.'\n– Warren Buffet""",
"""'The trend is your friend – until it stabs you in the back with a chopstick.'\n– @StockCats""",
"""The four most dangerous words in investing are: ‘this time it’s different.'\n– Sir John Templeton""",
"""'It’s not how much money you make, but how much money you keep, how hard it works for you, and how many generations you keep it for.'\n– Robert Kiyosaki""",
"""'Know what you own, and know why you own it.'\n- Peter Lynch""",
"""'All the math you need in the stock market you get in the fourth grade.'\n-Peter Lynch""",
"""'I just wait until there is money lying in the corner, and all I have to do is go over there and pick it up. I do nothing in the meantime.'\n– Jim Rogers""",
"""'A rising tide lifts all boats over the wall of worry and exposes bears swimming naked.'\n– @StockCats""",
"""'In investing, what is comfortable is rarely profitable.”\n– Robert Arnott""",
"""'Sometimes the best trade is no trade.”\n– Anonymous""",
"""The game of speculation is the most uniformly fascinating game in the world. But it is not a game for the stupid, the mentally lazy, the person of inferior emotional balance, or the get-rich-quick adventurer. They will die poor.'\n– Jesse Livermore""",
"""'Bulls make money, bears make money, pigs get slaughtered.""",
"""You get recessions, you have stock market declines. If you don’t understand that’s going to happen, then you’re not ready, you won’t do well in the markets.”\n- Peter Lynch""",
"""'Dangers of watching every tick are twofold: overtrading and increased chances of prematurely liquidating good positions'\n– Jack Schwager""",
"""'Traders need a daily routine that they love. If you don’t love it, you’re not gonna do it.'\n–Scott Redler""",
"""'Financial peace isn’t the acquisition of stuff. It’s learning to live on less than you make, so you can give money back and have money to invest. You can’t win until you do this.'\n– Dave Ramsey""",
"""'Michael Marcus taught me one other thing that is absolutely critical: You have to be willing to make mistakes regularly; there is nothing wrong with it. Michael taught me about making your best judgment, being wrong, making your next best judgment, being wrong, making your third best judgment, and then doubling your money.'\n– Bruce Kovner""",
"""'Amateurs think about how much money they can make. Professionals think about how much money they could lose.'\n– Jack Schwager"""
"""'If you can’t take a small loss, sooner or later you will take the mother of all losses.'\n– Ed Seykota""",
"""'5/1 risk/reward ratio allows you to have a hit rate of 20%. I can actually be a complete imbecile. I can be wrong 80% of time and still not lose.'\n– Paul Tudor Jones""",
"""Bottoms in the investment world don’t end with four-year lows; they end with 10- or 15-year lows.'\n– Jim Rogers""",
"""'If you think in positive terms, you will achieve positive results.'\n— Norman Vincent Peale""",
"""'The market is a device for transferring money from the impatient to the patient.'\n– Warren Buffet""",
"""'Take your profits or someone else will take them for you.'\n– J.J. Evans""",
"""'In trading, everything works sometimes and nothing works always.'""",
"""'The most important quality for an investor is temperament, not intellect. You need a temperament that neither derives great pleasure from being with the crowd or against the crowd.'\n-Warren Buffett"""
"""'All you need is one pattern to make a living.'\n– Linda Raschke""",
"""'The core problem, however, is the need to fit markets into a style of trading rather than finding ways to trade that fit with market behavior.'\n– Brett Steenbarger""",
"""'The obvious rarely happens, the unexpected constantly occurs.'\n– Jesse Livermore""",
"""'Hope is bogus emotion that only costs you money.'\n– Jim Cramer""",
"""'Five fundamental truths:\n1. Anything can happen.\n2. You don’t need to know what is going to happen next in order to make money.\n3. There is a random distribution between wins and losses for any given set of variables that define an edge.\n4. An edge is nothing more than an indication of a higher probability of one thing happening over another.\n5. Every moment in the market is unique.'\n– Mark Douglas""",
"""'Invest in yourself. Your career is the engine of your wealth.'\n– Paul Clitheroe""",
"""'IF YOU WANT TO BE A LEDGE… FIND YOUR EDGE…'\n– Tom Dante @Trader_Dante""",
"""'Once you find the system that works for your style/personality and confidence is gained, wash, rinse, repeat over and over again.'\n– @Sunrisetrader""",
"""'An investment in knowledge pays the best interest.'\n– Benjamin Franklin""",
"""'Investing should be more like watching paint dry or watching grass grow. If you want excitement, take $800 and go to Las Vegas.'\n– Paul Samuelson""",
"""'Stocks are bought not in fear but in hope. They are typically sold out of fear.'\n– Justin Mamis""",
"""'How many millionaires do you know who have become wealthy by investing in savings accounts? I rest my case.'\n– Robert G. Allen""",
"""'Accepting losses is the most important single investment device to insure safety of capital.'\n– Gerald M. Loeb""",
"""'In trading the impossible happens about twice a year.'\n– Henri M Simoes @TraderHMS""",
"""'You don’t need to trade everyday. You trade when your setups are there… The greatest surfers in the world don’t try to catch every wave– Wait for the right setup!'\n-Dale Pinkert""",
"""'The desire for constant action irrespective of underlying conditions is responsible for many losses in Wall Street.'\n– Jesse Livermore""",
]

#st.markdown("### Site is in progress \n Shall be launched asap")
st.title("BHAVCOPY NSE especially for AMIBROKER USERS")

full_message_temp ="""
<div style="background-color:#6C8594;overflow-x: auto; padding:10px;border-radius:5px;margin:10px;">
<p style="text-align:justify;color:black;padding:10px">{}</p>
</div>
"""
st.markdown(full_message_temp.format(stock_quotes[random.randint(0,len(stock_quotes)-1)]),unsafe_allow_html=True)
#st.markdown(full_message_temp.format(stock_quotes[35]),unsafe_allow_html=True)

col1,col2 = st.columns([1,1])
with col1:
    my1_date = st.date_input("FROM", value=date.today(),
                                min_value=datetime.date(1990, 1, 1))
with col2:
    if my1_date is not date.today():
        my2_date = st.date_input("TILL", value=min(my1_date+timedelta(60),date.today()),
                                    min_value=datetime.date(1990, 1, 1))
    else :
        my2_date = st.date_input("TILL", value=date.today(),
                                 min_value=datetime.date(1990, 1, 1))

if st.button("GENERATE BHAVCOPIES"):
    try:
        EOD.download_bhav(my1_date,my2_date)
        #EOD.download_bhav(nselink,bselink, indexlink, possible_index_name)
        # st.success("Done downloading, lets try extracting now")
        #eod_existing_files(path_bhav, path_csv)
    except BadZipFile:
        st.error("BadZipFile")
        pass
