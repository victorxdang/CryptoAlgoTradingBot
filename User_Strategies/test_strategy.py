import pandas as pd
import numpy as np

from Source.BaseStrategy import BaseStrategy


class test_strategy(BaseStrategy):
    
    def __init__(self):
        print(f"Running test_strategy")