import yfinance as yf
from datetime import datetime, timezone, timedelta, date
import pandas as pd
from gooey import Gooey, GooeyParser
import os

def display_data(t: yf.Tickers, t_list: list[str]) -> None:
    """
    Displays dividend data for the selected TSX60 constituents including dividend yield, dividend rate, 
    and date of the latest paid dividend.
    
    :param t: yfinance Tickers object containing all TSX60 constituents.
    :param t_list: List of TSX60 constituents to display data for.
    """

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

def export_to_csv(t: yf.Tickers, t_list: list[str], file: str) -> None:
    """
    Exports dividend data for the selected TSX60 constituents including dividend yield, dividend rate,
    and date of the latest paid dividend to a comma-separated values (CSV) file.
    
    :param t: yfinance Tickers object containing all TSX60 constituents.
    :param t_list: List of TSX60 constituents to display data for.
    :param file: The full path of the CSV file to save the data to.
    """

    csv_file = open(file, 'w')
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

def export_ohlc_to_csv(t: yf.Tickers, t_list: list[str], period: int, file: str) -> None:
    """
    Exports the Open, High, Low, Close (OHLC) values for a specific number of days for the selected TSX60 constituents, including volume
    and stock splits for each date/record, to a comma-separated values (CSV) file.
    
    :param t: yfinance Tickers object containing all TSX60 constituents.
    :param t_list: List of TSX60 constituents to display data for.
    :param period: The number of days before and after the last dividend pay date. (15-day period by default - allow users to choose in the future)
    :param file: The full path of the CSV file to save the data to.
    """

    # clear out csv file before appending new data
    csv_file = open(file, 'w')
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
            cur_ohlc.to_csv(file, mode='a', header=False)
        except:
            print(f'Error writing information of {symbol} into csv file.')

@Gooey(program_name="Dividend Data Compiler", program_description="A Python app to collect historical dividend data for S&&P/TSX 60 constituents on Yahoo Finance.", default_size=(800, 600))
def main():
    parser = GooeyParser(description="Dividend Data Compiler")

    # add title and description to radio button menu group
    menu = parser.add_argument_group(
        "Menu Options", 
        "Choose to display or export data to a CSV file", 
        gooey_options={
            'show_border': True,
            'show_underline': True
        }
    )

    # add radio buttons
    radio = menu.add_mutually_exclusive_group()
    radio.add_argument("--display", metavar="Display Data", action="store_true", help="Display dividend data in console")
    radio.add_argument("--export", metavar="Export to CSV", action="store_true", help="Export dividend data to CSV file")
    radio.add_argument("--exportOHLC", metavar="Export OHLC to CSV", action="store_true", help="Export OHLC data in a 15 day period of the latest dividend pay date to CSV file")

    # add title, desc, and input to select filename and location to save the generated csv as 
    file = parser.add_argument_group(
        "File Options", 
        "If either export options are selected above, choose a location and specify the filename to save the CSV file",
        gooey_options={
            'show_border': True,
            'show_underline': True
        }
    )
    file.add_argument(
        "file", 
        metavar="Save As", 
        help="Default filename is data.csv in the current directory",
        widget="FileSaver", 
        gooey_options={
            'wildcard': "CSV (Comma delimited) (*.csv)|*.csv|" "All files (*.*)|*.*",
            'message': "Save As",
            'default_dir': os.path.abspath(os.getcwd()),
            'default_file': "data.csv"
        },
        default=os.path.join(os.path.abspath(os.getcwd()), "data.csv")
    )

    # add title and description to TSX 60 ticker selection fields
    ticker_group = parser.add_argument_group(
        "Ticker Options", 
        "Select ticker symbols from different sectors to provide data for", 
        gooey_options={
            'columns': 2,
            'show_border': True,
            'show_underline': True
        }
    )

    # split tickers into different sectors 
    ticker_group.add_argument(
        "--basic_mats",
        metavar="Basic Materials",
        widget="Listbox",
        choices=[
            "AEM.TO", "ABX.TO", "FM.TO", "FNV.TO", "K.TO", "NTR.TO", "TECK-B.TO", "WPM.TO"
        ],
        nargs='*',
        help="ticker symbols",
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
        help="ticker symbols",
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
        help="ticker symbols",
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
        help="ticker symbols",
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
        help="ticker symbols",
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
        help="ticker symbols",
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
        help="ticker symbols",
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
        help="ticker symbols",
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
        help="ticker symbols",
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
        help="ticker symbols",
        default=[]
    )

    # retrieve user input
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
        export_to_csv(tickers, ticker_list, args.file)
    elif args.exportOHLC:
        export_ohlc_to_csv(tickers, ticker_list, 7, args.file)
    else:
        print("No option selected. Please try again.")

if __name__ == "__main__":
    main()