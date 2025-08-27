import yfinance as yf
from datetime import datetime, timezone

def display_data(t, t_list):
    for i in range(len(t_list)):
        try:
            print(f'{t.tickers[t_list[i]].info["longName"]} ({t.tickers[t_list[i]].info["symbol"]})')
            print(f'Dividend Yield (%): {t.tickers[t_list[i]].info["dividendYield"]}%')
            print(f'Dividend Rate ({t.tickers[t_list[i]].info["currency"]}): {t.tickers[t_list[i]].info["dividendRate"]}')

            print(f'Ex-Dividend Date: {datetime.fromtimestamp(t.tickers[t_list[i]].info["exDividendDate"], tz=timezone.utc)}')

            print('\nLatest dividend pay date:')
            print(t.tickers[t_list[i]].dividends.tail(1))
        except:
            print('The data for the symbol', t_list[i], 'could not be successfully fetched.')

def export_to_csv(t, t_list):
    csv_file = open("data.csv", 'w')

    csv_file.write('Symbol,Div Yield,Div Pay Date,Ex-Div Date\n')

    for i in range(len(t_list)):
        try:
            csv_file.write(f'{t_list[i]},{t.tickers[t_list[i]].info["dividendRate"]} ({t.tickers[t_list[i]].info["dividendYield"]}%),{t.tickers[t_list[0]].dividends.index[-1].date()},{datetime.fromtimestamp(t.tickers[t_list[i]].info["exDividendDate"], tz=timezone.utc).date()}\n')
        except:
            print(f'Error writing information of {t_list[i]} into csv file.')

    csv_file.close()

def main():
    tickers = yf.Tickers('AEM.TO AQN.TO ATD.TO BMO.TO BNS.TO ABX.TO BCE.TO BAM.TO BN.TO BIP-UN.TO CAE.TO CCO.TO CAR-UN.TO CM.TO CNR.TO CNQ.TO CP.TO CTC-A.TO CCL-B.TO CVE.TO GIB-A.TO CSU.TO DOL.TO EMA.TO ENB.TO FM.TO FSV.TO FTS.TO FNV.TO WN.TO GIL.TO H.TO IMO.TO IFC.TO K.TO L.TO MG.TO MFC.TO MRU.TO NA.TO NTR.TO OTEX.TO PPL.TO POW.TO QSR.TO RCI-B.TO RY.TO SAP.TO SHOP.TO SLF.TO SU.TO TRP.TO TECK-B.TO T.TO TRI.TO TD.TO TOU.TO WCN.TO WPM.TO WSP.TO')

    ticker_list = ["AEM.TO", "AQN.TO", "ATD.TO", "BMO.TO", "BNS.TO", "ABX.TO", "BCE.TO", "BAM.TO", "BN.TO", "BIP-UN.TO", "CAE.TO", "CCO.TO", "CAR-UN.TO", "CM.TO", "CNR.TO", "CNQ.TO", "CP.TO", "CTC-A.TO", "CCL-B.TO", "CVE.TO", "GIB-A.TO", "CSU.TO", "DOL.TO", "EMA.TO", "ENB.TO", "FM.TO", "FSV.TO", "FTS.TO", "FNV.TO", "WN.TO", "GIL.TO", "H.TO", "IMO.TO", "IFC.TO", "K.TO", "L.TO", "MG.TO", "MFC.TO", "MRU.TO", "NA.TO", "NTR.TO", "OTEX.TO", "PPL.TO", "POW.TO", "QSR.TO", "RCI-B.TO", "RY.TO", "SAP.TO", "SHOP.TO", "SLF.TO", "SU.TO", "TRP.TO", "TECK-B.TO", "T.TO", "TRI.TO", "TD.TO", "TOU.TO", "WCN.TO", "WPM.TO", "WSP.TO"]

    # display_data(tickers, ticker_list)

    export_to_csv(tickers, ticker_list)

if __name__ == "__main__":
    main()