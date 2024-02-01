import os
import pandas as pd
import requests


def get_data(url :str):
    header = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
    }

    r = requests.get(url, headers=header)

    dfs = pd.read_html(r.text)

    return dfs[1]
    
def format_data(df :pd.DataFrame):
    df.drop(columns=[df.columns[0], df.columns[-1]], inplace=True)

    return df

def save_to_csv(df :pd.DataFrame, path :str):
    df.to_csv(path, index=False)

def main():
    url = 'https://tradingeconomics.com/commodity/palm-oil'
    df_main = get_data(url)

    formated_df = format_data(df_main)

    save_to_csv(formated_df, 'results/palm-oil-price.csv')
    print(formated_df)
    

if __name__ == "__main__":
    main()