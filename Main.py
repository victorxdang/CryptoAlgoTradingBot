import questionary
import importlib

from os import listdir
from os.path import isfile


def main():   

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
        elif option == main_options[0]:
            module = importlib.import_module(f"User_Strategies.{strategy}")
            script = getattr(module, strategy)
            script().run()
        #elif option == main_options[1]:
        #    Backtest()


        print(f"Selected Option: {option}")
        print(f"Selected Strategy: {strategy}")

    print("Exiting...")
    

if __name__ == '__main__':
    main()