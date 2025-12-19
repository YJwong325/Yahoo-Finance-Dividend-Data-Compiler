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

@Gooey
def main():
    parser = GooeyParser(description="Dividend Data Compiler")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("--display", metavar="Display Data", action="store_true", help="Display dividend data in console")
    group.add_argument("--export", metavar="Export to CSV", action="store_true", help="Export dividend data to CSV file")
    group.add_argument("--exportOHLC", metavar="Export OHLC to CSV", action="store_true", help="Export OHLC data in a 15 day period of the latest dividend pay date to CSV file")

    parser.add_argument(
        "symbols", 
        metavar="Symbols", 
        widget="Listbox", 
        choices=[
                    "AEM.TO", "AQN.TO", "ATD.TO", "BMO.TO", "BNS.TO", 
                    "ABX.TO", "BCE.TO", "BAM.TO", "BN.TO", "BIP-UN.TO", 
                    "CAE.TO", "CCO.TO", "CAR-UN.TO", "CM.TO", "CNR.TO", 
                    "CNQ.TO", "CP.TO", "CTC-A.TO", "CCL-B.TO", "CVE.TO", 
                    "GIB-A.TO", "CSU.TO", "DOL.TO", "EMA.TO", "ENB.TO", 
                    "FM.TO", "FSV.TO", "FTS.TO", "FNV.TO", "WN.TO", 
                    "GIL.TO", "H.TO", "IMO.TO", "IFC.TO", "K.TO", 
                    "L.TO", "MG.TO", "MFC.TO", "MRU.TO", "NA.TO", 
                    "NTR.TO", "OTEX.TO", "PPL.TO", "POW.TO", "QSR.TO", 
                    "RCI-B.TO", "RY.TO", "SAP.TO", "SHOP.TO", "SLF.TO", 
                    "SU.TO", "TRP.TO", "TECK-B.TO", "T.TO", "TRI.TO", 
                    "TD.TO", "TOU.TO", "WCN.TO", "WPM.TO", "WSP.TO"
                ], 
        nargs='*', 
        help="List of ticker symbols to provide data for"
    )

    args = parser.parse_args()

    # List of TSX60 ticker symbols
    tickers = yf.Tickers('AEM.TO AQN.TO ATD.TO BMO.TO BNS.TO ABX.TO BCE.TO BAM.TO ' \
    'BN.TO BIP-UN.TO CAE.TO CCO.TO CAR-UN.TO CM.TO CNR.TO CNQ.TO CP.TO CTC-A.TO CCL-B.TO ' \
    'CVE.TO GIB-A.TO CSU.TO DOL.TO EMA.TO ENB.TO FM.TO FSV.TO FTS.TO FNV.TO WN.TO GIL.TO H.TO ' \
    'IMO.TO IFC.TO K.TO L.TO MG.TO MFC.TO MRU.TO NA.TO NTR.TO OTEX.TO PPL.TO POW.TO QSR.TO RCI-B.TO ' \
    'RY.TO SAP.TO SHOP.TO SLF.TO SU.TO TRP.TO TECK-B.TO T.TO TRI.TO TD.TO TOU.TO WCN.TO WPM.TO WSP.TO')

    # List of symbols to provide data for
    ticker_list = args.symbols

    if args.display:
        display_data(tickers, ticker_list)
    elif args.export:
        export_to_csv(tickers, ticker_list)
    elif args.exportOHLC:
        export_ohlc_to_csv(tickers, ticker_list, 7)
    else:
        print("No option selected. Please try again.")

if __name__ == "__main__":
    main()