import pandas as pd
import numpy as np

from Source.Kraken import Kraken

class BaseStrategy():

    def __init__(self):
        self.kraken = Kraken()

    def run(self):
        """
        Description:
            To be used for live/paper trading.
        """

        print(f"Running Live/Paper Trading")

    def backtest(self, pair: str, timeframe: int, capital: float = 10000, stake_amount: float = 0.9, trade_fee = 0.0026):
        """
        Description:
            To be used for backtesting.
        """

        df = self.kraken.get_ohlcv_data(pair, timeframe)
        df["buy"] = 0
        df["sell"] = 0
        df["stoploss"] = 0

        df = self.create_indicators(df, pair)
        df = self.set_buy_signals(df, pair)
        df = self.set_sell_signals(df, pair)

        # last buy timestamp, keep track to retrieve this row when a sell happens.
        # reset to None when sell happens
        last_buy_timestamp = None
        last_buy_stake_amount = 0
        last_buy_coin_amount = 0

        total_capital = capital
        total_profit_absolute = 0
        total_profit_percent = 0

        cumulative_profit = 0
        cumulative_percent = 0

        wins = 0
        losses = 0
        trades = 0
        total_amount_gained = 0
        total_amount_lost = 0
        highest_winner_timestamp = None
        highest_winner = 0
        highest_loser_timestamp = None
        highest_loser = 0

        rejected_signals = 0
        stoploss_amount = 0

        output = []
        output.append(f"- Start of Backtesting for {pair} -")

        for timestamp in df.index:
            row = df.loc[timestamp]
            stoploss_hit = row["low"] < row["stoploss"]

            if row['buy'] == row['sell']:
                # both buy and sell signals are present, ignore
                rejected_signals += 1

            elif row['buy'] == 1 and last_buy_timestamp is None:
                last_buy_timestamp = timestamp
                buy_amount = (total_capital * stake_amount)
                fee_amount = buy_amount * trade_fee
                last_buy_stake_amount = buy_amount - fee_amount
                last_buy_coin_amount = last_buy_stake_amount / row["close"]
                total_capital -= last_buy_stake_amount
            elif (row["sell"] == 1 and last_buy_timestamp is not None) or stoploss_hit:
                price = row["close"]
                if stoploss_hit:
                    stoploss_amount += 1
                    price = row["stoploss"] 

                sell_amount = price * last_buy_coin_amount
                fee_amount = sell_amount * trade_fee
                current_sell = sell_amount - fee_amount
                current_profit =  current_sell - last_buy_stake_amount 
                current_percent = ((current_sell / last_buy_stake_amount) - 1) * 100
                total_capital += current_sell 

                cumulative_profit += current_profit
                cumulative_percent += current_percent

                if current_profit > 0:
                    wins += 1
                    total_amount_gained += current_profit

                    if current_profit > highest_winner:
                        highest_winner = current_profit
                        highest_winner_timestamp = timestamp
                else:
                    losses += 1
                    total_amount_lost += current_profit

                    if current_profit < highest_loser:
                        highest_loser = current_profit
                        highest_loser_timestamp = timestamp

                trades += 1
                last_buy_timestamp = None
                last_buy_stake_amount = 0
                last_buy_coin_amount = 0

            # $10 is generally the minimum amount needed to trade on exchanges
            if total_capital < 10 and last_buy_timestamp is None:
                break


            if last_buy_timestamp is not None:
                row = df.loc[last_buy_timestamp]

        if trades > 0:
            total_capital += last_buy_stake_amount
            total_profit_absolute = total_capital - capital
            total_profit_percent = ((total_capital / capital) - 1) * 100

            output.append(f"\n- End of Backtesting for {pair} -")
            output.append(f"\n\nWins/Loss/Total: {wins}/{losses}/{(wins + losses)}")
            output.append(f"\nW/L Ratio: {(wins / trades) * 100:.2f}%")
            output.append(f"\nTotal Gained: ${total_amount_gained:.2f}")
            output.append(f"\nTotal Lost: ${total_amount_lost:.2f}")
            output.append(f"\nBest Performer: ${highest_winner:.2f} - {highest_winner_timestamp}")
            output.append(f"\nWorst Performer: ${highest_loser:.2f} - {highest_loser_timestamp}")
            output.append(f"\n\nTotal Balance: ${total_capital:.2f}")
            output.append(f"\nTotal Profit Absolute: ${total_profit_absolute:.2f}")
            output.append(f"\nTotal Profit Percent: {total_profit_percent:.2f}%")
            output.append(f"\nCumulative Profit: ${cumulative_profit:.2f}")
            output.append(f"\nCumulative Profit %: {cumulative_percent:.2f}%")
            output.append(f"\nRejected Signals: {rejected_signals}")
            output.append(f"\nStoploss Hit: {stoploss_amount}")
        else:
            output.append(f"\nNo Trades Made")

        print("".join(output))
        return df


    """
    Below functions are to be overwritten by user strategies.
    """

    def create_indicators(self, dataframe: pd.DataFrame, pair: str) -> pd.DataFrame:
        # to be overwritten by strategy
        return dataframe

    def set_buy_signals(self, dataframe: pd.DataFrame, pair: str) -> pd.DataFrame:
        # to be overwritten by strategy
        return dataframe

    def set_sell_signals(self, dataframe: pd.DataFrame, pair: str) -> pd.DataFrame:
        # to be overwritten by strategy
        return dataframe
