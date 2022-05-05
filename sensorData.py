import pandas as pd
import numpy as np
from random import randint



def procent(val, procente=20):
    return val*procente/100

def generate_dateframe(size, pattern, seed=None, in_interval=True):
    rng = np.random.default_rng(seed)
    df = pd.DataFrame()

    # Generarea datelor ce se vor incadra in interval
    if(in_interval):
        for key, value in pattern.items():
            min, max = value[1]
            if value[0] == "int":
                df[key] = rng.integers(min, max, size)
            elif value[0] == "float":
                df[key] = np.around(rng.uniform(min, max, size), decimals=2)
        df["starea"] = 1
    # generarea datelor inafara de interval
    else:
        for key, value in pattern.items():
            min, max = value[1]

            if value[0] == "int":
                interval_calc = randint(1, size)  # interval aliator
                df[key] = np.concatenate((
                    # generarea valorilor sub minim
                    rng.integers(min-procent(min), min, interval_calc),
                    # generarea valorilor peste maximum
                    rng.integers(max, max+procent(max), size - interval_calc)
                ))
            elif value[0] == "float":
                interval_calc = randint(1, size)  # interval aliator
                df[key] = np.concatenate((
                    np.around(rng.uniform(min - procent(min),
                              min, interval_calc), decimals=2),
                    np.around(rng.uniform(max, max + procent(max),
                              size - interval_calc), decimals=2)
                ))

        df["starea"] = 0

    return df


engine_data_interval = {
    'temp': ['int', (90, 105)],
    'rpm': ['int', (760, 840)],
    'voltage': ['float', (13.2, 14.6)]
}

def getGeneratedData():
    good_data = generate_dateframe(
        size=1200, pattern=engine_data_interval, in_interval=True)

    bad_data = generate_dateframe(
        size=500, pattern=engine_data_interval, in_interval=False)

    learndata = pd.concat([good_data, bad_data])

    learndata.sample(frac=1) #amestcarea datelor

    learndata
    return learndata