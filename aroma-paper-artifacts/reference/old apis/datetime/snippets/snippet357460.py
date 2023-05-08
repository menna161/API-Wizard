import cbpro
from cbpro.public_client import PublicClient
import time
import threading
from json import dumps, loads
from cbpro.websocket_client import WebsocketClient
import TradingBotConfig as theConfig
from datetime import datetime
import pytz
from tzlocal import get_localzone
from requests.exceptions import ConnectionError
from GDAXCurrencies import GDAXCurrencies
import math


def GDAX_LoadHistoricData(self, startTimestamp, stopTimestamp):
    print(('Init to retrieve Historic Data from %s to %s' % (datetime.fromtimestamp(startTimestamp).isoformat(), datetime.fromtimestamp(stopTimestamp).isoformat())))
    print('---------')
    self.HistoricDataReadIndex = 0
    local_tz = get_localzone()
    print(('GDAX - Local timezone found: %s' % local_tz))
    tz = pytz.timezone(str(local_tz))
    stopSlice = 0
    startSlice = startTimestamp
    self.HistoricDataRaw = []
    self.HistoricData = []
    granularityInSec = round(self.GDAX_HISTORIC_DATA_MIN_GRANULARITY_IN_SEC)
    nbIterationsToRetrieveEverything = (((stopTimestamp - startTimestamp) / round(self.GDAX_HISTORIC_DATA_MIN_GRANULARITY_IN_SEC)) / round(self.GDAX_MAX_HISTORIC_PRICES_ELEMENTS))
    print(('GDAX - Nb Max iterations to retrieve everything: %s' % nbIterationsToRetrieveEverything))
    nbLoopIterations = 0
    while (stopSlice < stopTimestamp):
        stopSlice = (startSlice + (self.GDAX_MAX_HISTORIC_PRICES_ELEMENTS * granularityInSec))
        if (stopSlice > stopTimestamp):
            stopSlice = stopTimestamp
        print(('GDAX - Start TS : %s  stop TS : %s' % (startSlice, stopSlice)))
        startTimestampSliceInISO = datetime.fromtimestamp(startSlice, tz).isoformat()
        stopTimestampSliceInISO = datetime.fromtimestamp(stopSlice, tz).isoformat()
        print(('GDAX - Retrieving Historic Data from %s to %s' % (startTimestampSliceInISO, stopTimestampSliceInISO)))
        if (self.IsConnectedAndOperational == 'True'):
            print('GDAX - Using public client to retrieve historic prices')
            HistoricDataSlice = self.clientAuth.get_product_historic_rates(self.productStr, granularity=granularityInSec, start=startTimestampSliceInISO, end=stopTimestampSliceInISO)
            if (stopSlice < stopTimestamp):
                time.sleep(0.35)
            print('GDAX - Using private client to retrieve historic prices')
        else:
            HistoricDataSlice = self.clientPublic.get_product_historic_rates(self.productStr, granularity=granularityInSec, start=startTimestampSliceInISO, end=stopTimestampSliceInISO)
            if (stopSlice < stopTimestamp):
                time.sleep(0.25)
            print('GDAX - Using public client to retrieve historic prices')
        print(('GDAX - Size of HistoricDataSlice: %s' % len(HistoricDataSlice)))
        try:
            for slice in reversed(HistoricDataSlice):
                self.HistoricDataRaw.append(slice)
        except BaseException as e:
            print('GDAX - Exception when reversing historic data slice')
        startSlice = stopSlice
        nbLoopIterations = (nbLoopIterations + 1)
        percentage = round(((nbLoopIterations * 100) / nbIterationsToRetrieveEverything))
        if (percentage > 100):
            percentage = 100
        self.theUIGraph.UIGR_updateLoadingDataProgress(str(percentage))
    print(('GDAX - LoadHistoricData - Cleaning buffer. Nb elements before cleaning : %s' % len(self.HistoricDataRaw)))
    tempIterationIndex = 0
    currentBrowsedTimestamp = 0
    while (tempIterationIndex < len(self.HistoricDataRaw)):
        if (self.HistoricDataRaw[tempIterationIndex][0] <= (currentBrowsedTimestamp + 1)):
            pass
        else:
            currentBrowsedTimestamp = self.HistoricDataRaw[tempIterationIndex][0]
            self.HistoricData.append(self.HistoricDataRaw[tempIterationIndex])
        tempIterationIndex = (tempIterationIndex + 1)
    print(('GDAX - %s Historical samples have been retrieved (after cleaning)' % len(self.HistoricData)))
