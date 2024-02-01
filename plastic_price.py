import os
import pandas as pd

def read_csv(url :str):
    df = pd.read_csv(url)
    return df

def change_columns_name(df: pd.DataFrame):
    df.columns = df.iloc[0]
    df = delete_row(0, df)
    columns = df.columns
    return df, columns

def create_dataframe(columns :list):
    new_df = pd.DataFrame(columns=columns)
    return new_df

def delete_row(index :int, df :pd.DataFrame):
    df = df.drop(index=index)

    return df


def get_data_from_column(df :pd.DataFrame, columns :list, index :int):
    data = df[columns[index]]

    return data


def get_data_row_to_list(df :pd.DataFrame, index :int):
    data = df.iloc[index].to_list()
    return data

def get_date(df : pd.DataFrame):
    date = get_data_row_to_list(df, 0)
    new_date = []
    del date[0]

    for i in date:
        temp_date_back = i.split('/')
        if len(temp_date_back) > 3:
            del temp_date_back[1]
        temp_date_front = i.split('/')
        if len(temp_date_front[0]) > 2:
            temp_date_front = temp_date_front[0].split('-')[0]
        else:
            temp_date_front = temp_date_front[0]
            
            print(temp_date_front)
        del temp_date_back[0]
        new_date.append(f'{temp_date_front}/{temp_date_back[0]}/{temp_date_back[1]}')
    df = delete_row(1, df)
    return df, new_date

def prepare_temp_dataframe(df :pd.DataFrame, columns :list, date :list, index :int):
    new_columns = ['type', 'date', 'price']
    data = get_data_from_column(df, columns, index+1)
    current_date = date[index]
    temp_dates = [current_date for _ in range(len(data))]
    temp_df = create_dataframe(columns=new_columns)
    temp_df[new_columns[0]] = df['ชนิด']
    temp_df[new_columns[1]] = temp_dates
    temp_df[new_columns[2]] = data

    return temp_df
    

def add_data(df :pd.DataFrame, date :list, columns :list):
    new_columns = ['type', 'date', 'price']
    new_df = create_dataframe(new_columns)
    for idx, d in enumerate(date):
        temp_df = prepare_temp_dataframe(df, columns, date, idx)
        new_df = pd.concat([new_df, temp_df], ignore_index=True)
    
    return new_df

def save_to_csv(df :pd.DataFrame, path :str):
    df.to_csv(path, index=False)

def main():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSdiWEirzRNYezEaHaFA5iF9Td7QlkBEm1eR8ZjkXGfc2-uFO89jHKNJQH5uT_cXhBUV2A6I10tcjtU/pub?output=csv"
    main_df = read_csv(url)
    main_df, columns = change_columns_name(main_df)

    df_no_date, dates = get_date(main_df)
    new_df = add_data(df_no_date, dates, columns)
    os.makedirs('results', exist_ok=True)
    save_to_csv(new_df, 'results/ตารางราคา-Y2024.csv')

if __name__ == "__main__":
    main()