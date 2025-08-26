import yfinance as yf
from datetime import datetime, timezone

tickers = yf.Tickers('AEM.TO AQN.TO ATD.TO BMO.TO BNS.TO ABX.TO BCE.TO BAM.TO BN.TO BIP-UN.TO CAE.TO CCO.TO CAR-UN.TO CM.TO CNR.TO CNQ.TO CP.TO CTC-A.TO CCL-B.TO CVE.TO GIB-A.TO CSU.TO DOL.TO EMA.TO ENB.TO FM.TO FSV.TO FTS.TO FNV.TO WN.TO GIL.TO H.TO IMO.TO IFC.TO K.TO L.TO MG.TO MFC.TO MRU.TO NA.TO NTR.TO OTEX.TO PPL.TO POW.TO QSR.TO RCI-B.TO RY.TO SAP.TO SHOP.TO SLF.TO SU.TO TRP.TO TECK-B.TO T.TO TRI.TO TD.TO TOU.TO WCN.TO WPM.TO WSP.TO')

ticker_list = ["AEM.TO", "AQN.TO", "ATD.TO", "BMO.TO", "BNS.TO", "ABX.TO", "BCE.TO", "BAM.TO", "BN.TO", "BIP-UN.TO", "CAE.TO", "CCO.TO", "CAR-UN.TO", "CM.TO", "CNR.TO", "CNQ.TO", "CP.TO", "CTC-A.TO", "CCL-B.TO", "CVE.TO", "GIB-A.TO", "CSU.TO", "DOL.TO", "EMA.TO", "ENB.TO", "FM.TO", "FSV.TO", "FTS.TO", "FNV.TO", "WN.TO", "GIL.TO", "H.TO", "IMO.TO", "IFC.TO", "K.TO", "L.TO", "MG.TO", "MFC.TO", "MRU.TO", "NA.TO", "NTR.TO", "OTEX.TO", "PPL.TO", "POW.TO", "QSR.TO", "RCI-B.TO", "RY.TO", "SAP.TO", "SHOP.TO", "SLF.TO", "SU.TO", "TRP.TO", "TECK-B.TO", "T.TO", "TRI.TO", "TD.TO", "TOU.TO", "WCN.TO", "WPM.TO", "WSP.TO"]

for i in range(len(ticker_list)):
    try:
        print(f'{tickers.tickers[ticker_list[i]].info["longName"]} ({tickers.tickers[ticker_list[i]].info["symbol"]})')
        print(f'Dividend Yield (%): {tickers.tickers[ticker_list[i]].info["dividendYield"]}%')
        print(f'Dividend Rate ({tickers.tickers[ticker_list[i]].info["currency"]}): {tickers.tickers[ticker_list[i]].info["dividendRate"]}')

        print(f'Ex-Dividend Date: {datetime.fromtimestamp(tickers.tickers[ticker_list[i]].info["exDividendDate"], tz=timezone.utc)}')

        print('\nLatest dividend pay date:')
        print(tickers.tickers[ticker_list[i]].dividends.tail(1))
    except:
        print('The data for the symbol', ticker_list[i], 'could not be successfully fetched.')