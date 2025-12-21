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

@Gooey(program_name="Dividend Data Compiler", default_size=(800, 600), optional_cols=1)
def main():
    parser = GooeyParser(description="Dividend Data Compiler")

    radio = parser.add_argument_group("Menu Options", "Choose to display or export data to a CSV file")
    ticker_group = parser.add_argument_group("Ticker Options", "Select ticker symbols from different sectors to provide data for")

    group = radio.add_mutually_exclusive_group()
    group.add_argument("--display", metavar="Display Data", action="store_true", help="Display dividend data in console")
    group.add_argument("--export", metavar="Export to CSV", action="store_true", help="Export dividend data to CSV file")
    group.add_argument("--exportOHLC", metavar="Export OHLC to CSV", action="store_true", help="Export OHLC data in a 15 day period of the latest dividend pay date to CSV file")

    # todo: allow use to choose filename and file path to download

    # TODO: split tickers into different sectors 
    ticker_group.add_argument(
        "--basic_mats",
        metavar="Basic Materials",
        widget="Listbox",
        choices=[
            "AEM.TO", "ABX.TO", "FM.TO", "FNV.TO", "K.TO", "NTR.TO", "TECK-B.TO", "WPM.TO"
        ],
        nargs='*',
        help="Basic Materials sector ticker symbols",
        default=[]
    )

    ticker_group.add_argument(
        "--comm_services",
        metavar="Communication Services",
        widget="Listbox",
        choices=[
            "BCE.TO", "RCI-B.TO", "T.TO"
        ],
        nargs='*',
        help="Communication Services sector ticker symbols",
        default=[]
    )

    ticker_group.add_argument(
        "--consumer_cyc",
        metavar="Consumer Cyclical",
        widget="Listbox",
        choices=[
            "ATD.TO", "CTC-A.TO", "CCL-B.TO", "GIL.TO", "MG.TO", "QSR.TO"
        ],
        nargs='*',
        help="Consumer Cyclical sector ticker symbols",
        default=[]
    )

    ticker_group.add_argument(
        "--consumer_stap",
        metavar="Consumer Staples",
        widget="Listbox",
        choices=[
            "DOL.TO", "WN.TO", "L.TO", "MRU.TO", "SAP.TO"
        ],
        nargs='*',
        help="Consumer Staples sector ticker symbols",
        default=[]
    )

    ticker_group.add_argument(
        "--energy",
        metavar="Energy",
        widget="Listbox",
        choices=[
            "AQN.TO", "CCO.TO", "CNQ.TO", "CVE.TO", "ENB.TO", "IMO.TO", "PPL.TO", "SU.TO", "TRP.TO", "TOU.TO"
        ],
        nargs='*',
        help="Energy sector ticker symbols",
        default=[]
    )

    ticker_group.add_argument(
        "--fin_services",
        metavar="Financial Services",
        widget="Listbox",
        choices=[
            "BMO.TO", "BNS.TO", "BAM.TO", "BN.TO", "CM.TO", "IFC.TO", "MFC.TO", "NA.TO", "POW.TO", "RY.TO", "SLF.TO", "TD.TO"
        ],
        nargs='*',
        help="Financial Services sector ticker symbols",
        default=[]
    )

    ticker_group.add_argument(
        "--industrials",
        metavar="Industrials",
        widget="Listbox",
        choices=[
            "CAE.TO", "CNR.TO", "CP.TO", "TRI.TO", "WCN.TO", "WSP.TO"
        ],
        nargs='*',
        help="Industrials sector ticker symbols",
        default=[]
    )

    ticker_group.add_argument(
        "--info_tech",
        metavar="Information Technology",
        widget="Listbox",
        choices=[
            "GIB-A.TO", "CSU.TO", "OTEX.TO", "SHOP.TO"
        ],
        nargs='*',
        help="Information Technology sector ticker symbols",
        default=[]
    )

    ticker_group.add_argument(
        "--real_estate",
        metavar="Real Estate",
        widget="Listbox",
        choices=[
            "CAR-UN.TO", "FSV.TO"
        ],
        nargs='*',
        help="Real Estate sector ticker symbols",
        default=[]
    )

    ticker_group.add_argument(
        "--utils",
        metavar="Utilities",
        widget="Listbox",
        choices=[
            "BIP-UN.TO", "EMA.TO", "FTS.TO", "H.TO"
        ],
        nargs='*',
        help="Utilities sector ticker symbols",
        default=[]
    )

    args = parser.parse_args()

    # List of TSX60 ticker symbols
    tickers = yf.Tickers('AEM.TO AQN.TO ATD.TO BMO.TO BNS.TO ABX.TO BCE.TO BAM.TO ' \
    'BN.TO BIP-UN.TO CAE.TO CCO.TO CAR-UN.TO CM.TO CNR.TO CNQ.TO CP.TO CTC-A.TO CCL-B.TO ' \
    'CVE.TO GIB-A.TO CSU.TO DOL.TO EMA.TO ENB.TO FM.TO FSV.TO FTS.TO FNV.TO WN.TO GIL.TO H.TO ' \
    'IMO.TO IFC.TO K.TO L.TO MG.TO MFC.TO MRU.TO NA.TO NTR.TO OTEX.TO PPL.TO POW.TO QSR.TO RCI-B.TO ' \
    'RY.TO SAP.TO SHOP.TO SLF.TO SU.TO TRP.TO TECK-B.TO T.TO TRI.TO TD.TO TOU.TO WCN.TO WPM.TO WSP.TO')

    # List of symbols to provide data for
    ticker_list = args.basic_mats + args.comm_services + args.consumer_cyc + args.consumer_stap + args.energy + args.fin_services + \
                  args.industrials + args.info_tech + args.real_estate + args.utils

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