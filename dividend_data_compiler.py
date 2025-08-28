import yfinance as yf
from datetime import datetime, timezone

def display_data(t, t_list):
    for symbol in t_list:
        try:
            cur = t.tickers[symbol]

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

    for symbol in t_list:
        try:
            cur = t.tickers[symbol]

            csv_file.write(f'{symbol},{cur.info["dividendRate"]} ({cur.info["dividendYield"]}%),')
            csv_file.write(f'{cur.dividends.index[-1].date()},')
            csv_file.write(f'{datetime.fromtimestamp(cur.info["exDividendDate"], tz=timezone.utc).date()}\n')
        except:
            print(f'Error writing information of {symbol} into csv file.')

    csv_file.close()

def main():
    tickers = yf.Tickers('AEM.TO AQN.TO ATD.TO BMO.TO BNS.TO ABX.TO BCE.TO BAM.TO BN.TO BIP-UN.TO CAE.TO CCO.TO CAR-UN.TO CM.TO CNR.TO CNQ.TO CP.TO CTC-A.TO CCL-B.TO CVE.TO GIB-A.TO CSU.TO DOL.TO EMA.TO ENB.TO FM.TO FSV.TO FTS.TO FNV.TO WN.TO GIL.TO H.TO IMO.TO IFC.TO K.TO L.TO MG.TO MFC.TO MRU.TO NA.TO NTR.TO OTEX.TO PPL.TO POW.TO QSR.TO RCI-B.TO RY.TO SAP.TO SHOP.TO SLF.TO SU.TO TRP.TO TECK-B.TO T.TO TRI.TO TD.TO TOU.TO WCN.TO WPM.TO WSP.TO')

    ticker_list = ["AEM.TO", "AQN.TO", "ATD.TO", "BMO.TO", "BNS.TO", "ABX.TO", "BCE.TO", "BAM.TO", "BN.TO", "BIP-UN.TO", "CAE.TO", "CCO.TO", "CAR-UN.TO", "CM.TO", "CNR.TO", "CNQ.TO", "CP.TO", "CTC-A.TO", "CCL-B.TO", "CVE.TO", "GIB-A.TO", "CSU.TO", "DOL.TO", "EMA.TO", "ENB.TO", "FM.TO", "FSV.TO", "FTS.TO", "FNV.TO", "WN.TO", "GIL.TO", "H.TO", "IMO.TO", "IFC.TO", "K.TO", "L.TO", "MG.TO", "MFC.TO", "MRU.TO", "NA.TO", "NTR.TO", "OTEX.TO", "PPL.TO", "POW.TO", "QSR.TO", "RCI-B.TO", "RY.TO", "SAP.TO", "SHOP.TO", "SLF.TO", "SU.TO", "TRP.TO", "TECK-B.TO", "T.TO", "TRI.TO", "TD.TO", "TOU.TO", "WCN.TO", "WPM.TO", "WSP.TO"]

    display_data(tickers, ticker_list)

    export_to_csv(tickers, ticker_list)

if __name__ == "__main__":
    main()