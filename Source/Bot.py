import importlib
import pandas as pd

def run():
    """
    Description:
        To be used for live/paper trading.
    """

    print(f"Running Live/Paper Trading")

def backtest(strategy_name: str, pair: str, timeframe: int, plot_results = True):
    """
    Description:
        To be used for backtesting.
    """

    # import and instaniate the user selected strategy class
    module = importlib.import_module(f"User_Strategies.{strategy_name}")
    script = getattr(module, strategy_name)
    strategy = script()

    # run the strategy
    strategy.run(pair, timeframe, plot_results)

    # grab the dataframes after running the strategy
    df = strategy.dataframe
    pred_df = strategy.predictions_dataframe

    # calculate cumulative returns generated by the trading strategy signals
    cr = (1 + df[["actual_returns", "returns"]]).cumprod()
    print(f"\nCumulative Returns from {cr.index.min()} to {cr.index.max()}")
    print(f"Actual Return: {cr.iloc[-1]['actual_returns'] * 100:.2f}%\nTrading Returns: {cr.iloc[-1]['returns'] * 100:.2f}%")

    # calculate the cumulative returns after running the machine learning model on it
    ml_cr = (1 + pred_df[["ml_actual_returns", "ml_returns"]]).cumprod()
    print(f"\nMachine Learning Cumulative Returns from {ml_cr.index.min()} to {ml_cr.index.max()}")
    print(f"Actual Return: {ml_cr.iloc[-1]['ml_actual_returns'] * 100:.2f}%\nTrading Returns: {ml_cr.iloc[-1]['ml_returns'] * 100:.2f}%")

    print()
