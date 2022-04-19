import questionary
import fire
import importlib

from Source.Kraken import Kraken
from os import listdir
from os.path import isfile


def main():   

    kraken = Kraken()

    print("\nWelcome to the Crypto Algorithmic Trading Bot!"
        "\nThis bot only works with the Kraken Exchange."
        "\n\nDISCALIMER:"
        "\nThis software is for educational purposes only!"
        "\nDo not risk more money than you can afford to lose!"
        "\nThere is no guarantee that this software will make a profit."
        "\nAlways do your own research and due diligence.\n")

    main_options = [
        "Start Paper Trading",
        "Backtest Strategy",
        "Quit"
    ]

    while True:
        option = questionary.select("Select an option to continue:", main_options).ask()

        if option == main_options[2]:
            break
        

        strategy_folder = "./User_Strategies/"
        strategy_list = [f[:-3] for f in listdir(strategy_folder) if isfile(f"{strategy_folder}{f}")]
        strategy_list.append("Return")
        strategy = questionary.select("Select the strategy to use:", strategy_list).ask()

        if strategy == strategy_list[-1]:
            continue

        module = importlib.import_module(f"User_Strategies.{strategy}")
        script = getattr(module, strategy)

        if option == main_options[0]:
            script().run()
        elif option == main_options[1]:
            all_pair_names = kraken.get_tradeable_usd_asset_names()
            pair = questionary.select("Select a pair to backtest:", choices = all_pair_names).ask()
            capital = float(questionary.text("Enter initial capital:", default = "10000", validate = validate_float).ask())

            strategy_script = script()
            df = strategy_script.backtest(pair = pair, capital = capital, timeframe = 60)
            if questionary.confirm("Plot Results?").ask():
                strategy_script.plot_results(df, pair)

    print("Exiting...")

    
def validate_float(text):
    try:
        if len(text) > 0:
            _ = float(text)

        return True
    except Exception:
        return "Enter a valid number!"



if __name__ == '__main__':
    fire.Fire(main)