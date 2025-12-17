import yfinance as yf
from datetime import datetime, timezone, timedelta, date
import pandas as pd
from gooey import Gooey, GooeyParser

def display_data(t, t_list):
    for symbol in t_list:
        try:
            cur: yf.Ticker = t.tickers[symbol]

            print(f'{cur.info["longName"]} ({cur.info["symbol"]})')
            print(f'Dividend Yield (%): {cur.info["dividendYield"]}%')
            print(f'Dividend Rate ({cur.info["currency"]}): {cur.info["dividendRate"]}')

            print(f'Ex-Dividend Date: {datetime.fromtimestamp(cur.info["exDividendDate"], tz=timezone.utc).date()}')

            print(f'Latest dividend pay date: {cur.dividends.index[-1].date()}\n')
        except:
            print(f'The data for the symbol {symbol} could not be successfully fetched.\n')

def export_to_csv(t, t_list):
    csv_file = open("data.csv", 'w')
    csv_file.write('Symbol,Div Yield,Div Pay Date,Ex-Div Date\n')
    # csv_file.write('Symbol,Div Yield,Div Pay Date\n')

    for symbol in t_list:
        try:
            cur: yf.Ticker = t.tickers[symbol]

            csv_file.write(f'{symbol},{cur.info["dividendRate"]} ({cur.info["dividendYield"]}%),')
            # csv_file.write(f'{symbol},{cur.info["dividendYield"]}%,')

            csv_file.write(f'{cur.dividends.index[-1].date()},')
            csv_file.write(f'{datetime.fromtimestamp(cur.info["exDividendDate"], tz=timezone.utc).date()}\n')
        except:
            print(f'Error writing information of {symbol} into csv file.')

    csv_file.close()

def export_ohlc_to_csv(t, t_list, period):
    # clear out csv file before appending new data
    csv_file = open("ohlc.csv", 'w')
    csv_file.write('Date,Ticker,Open,High,Low,Close,Volume,Dividends,Stock Splits\n')
    csv_file.close()

    for symbol in t_list:
        try:
            cur_ticker: yf.Ticker = t.tickers[symbol]

            pay_date = cur_ticker.dividends.index[-1].date()
            period_start = pay_date - timedelta(days=period)
            period_end = pay_date + timedelta(days=period + 1)

            cur_ohlc: pd.DataFrame = cur_ticker.history(start=period_start, end=period_end, interval='1d')
            cur_ohlc.insert(0, "Ticker", symbol)
            cur_ohlc.to_csv("ohlc.csv", mode='a', header=False)
        except:
            print(f'Error writing information of {symbol} into csv file.')


def main():
    # Replace the placeholder ('######') in the bracket with ticker symbols of your choice delimited by spaces
    # For example: 'AEM.TO AQN.TO ATD.TO'
    tickers = yf.Tickers('######')

    # Replace the placeholders ('######') in the array with ticker symbols that you entered in the line above
    # For example: ["AEM.TO", "AQN.TO", "ATD.TO"]
    ticker_list = ["######"]

    display_data(tickers, ticker_list)
    export_to_csv(tickers, ticker_list)
    export_ohlc_to_csv(tickers, ticker_list, 7)

if __name__ == "__main__":
    main()