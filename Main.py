import questionary
import fire
import Source.Bot as bot

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
        

        # find all of the strategy classes under the User_Strategies folder
        strategy_folder = "./User_Strategies/"

        # add all of the strategy classes to the list with the ".py" extension removed
        strategy_list = [f[:-3] for f in listdir(strategy_folder) if isfile(f"{strategy_folder}{f}")]
        strategy_list.append("Return")

        # ask the user to select the strategy to use
        strategy = questionary.select("Select the strategy to use:", strategy_list).ask()

        if strategy == strategy_list[-1]: # Return
            continue

        if option == main_options[0]: # Paper run
            print("Paper Run")
        elif option == main_options[1]: # Backtest
            # get all of the tradeable crypto pairs to have the user select one
            all_pair_names = kraken.get_tradeable_usd_asset_names()
            pair = questionary.select("Select a pair to backtest:", choices = all_pair_names).ask()
            timeframe = int(questionary.text("Enter Timeframe:", default = "1440").ask())
            plot = questionary.confirm("Plot Backtest Results?").ask()

            # start backtesting
            bot.backtest(strategy, pair, timeframe, plot)

    print("Exiting...")


if __name__ == '__main__':
    fire.Fire(main)