import time
from datetime import datetime
import threading
from GDAXControler import GDAXControler
from UIGraph import UIGraph
import TradingBotConfig as theConfig
import Notifier as theNotifier


def performBuyDisplayActions(self, isLimitOrder):
    if isLimitOrder:
        if (self.isOrderPlacingActive == False):
            sellTriggerInPercent = self.theSettings.SETT_GetSettings()['sellTrigger']
            if (sellTriggerInPercent > 0.0):
                sellThreshold = (self.currentBuyInitialPriceInEUR * ((sellTriggerInPercent / 100) + 1))
            else:
                sellThreshold = (self.currentBuyInitialPriceInEUR * (theConfig.CONFIG_MIN_PRICE_ELEVATION_RATIO_TO_SELL + (2 * self.platformTakerFeeInPercent)))
            self.theUIGraph.UIGR_updateInfoText(('%s %s Bought @ %s %s via limit order - Waiting for a sell opportunity above %s %s' % (round(self.currentBuyAmountInCryptoWithoutFee, 5), self.theSettings.SETT_GetSettings()['strCryptoType'], round(self.currentBuyInitialPriceInEUR, 5), self.theSettings.SETT_GetSettings()['strFiatType'], round(sellThreshold, 5), self.theSettings.SETT_GetSettings()['strFiatType'])), False)
            theNotifier.SendWhatsappMessage(('*BUY filled* %s %s @ %s %s via limit order - Waiting for a sell opportunity above %s %s' % (round(self.currentBuyAmountInCryptoWithoutFee, 5), self.theSettings.SETT_GetSettings()['strCryptoType'], round(self.currentBuyInitialPriceInEUR, 5), self.theSettings.SETT_GetSettings()['strFiatType'], round(sellThreshold, 5), self.theSettings.SETT_GetSettings()['strFiatType'])))
            self.theUIGraph.UIGR_addMarker(1)
        else:
            self.theUIGraph.UIGR_updateInfoText(('%s %s Partially bought @ %s %s. Still ongoing, waiting for next matches' % (round(self.currentBuyAmountInCryptoWithoutFee, 5), self.theSettings.SETT_GetSettings()['strCryptoType'], round(self.currentBuyInitialPriceInEUR, 5), self.theSettings.SETT_GetSettings()['strFiatType'])), False)
            theNotifier.SendWhatsappMessage(('*BUY match* %s %s @ %s %s. Still ongoing, waiting for next matches' % (round(self.currentBuyAmountInCryptoWithoutFee, 5), self.theSettings.SETT_GetSettings()['strCryptoType'], round(self.currentBuyInitialPriceInEUR, 5), self.theSettings.SETT_GetSettings()['strFiatType'])))
    else:
        buyTimeStr = datetime.fromtimestamp(int(self.buyTimeInTimeStamp)).strftime('%H:%M')
        sellThreshold = (self.currentBuyInitialPriceInEUR * (theConfig.CONFIG_MIN_PRICE_ELEVATION_RATIO_TO_SELL + (2 * self.platformTakerFeeInPercent)))
        self.theUIGraph.UIGR_updateInfoText(('%s - %s %s Bought @ %s %s - Waiting for a sell opportunity above %s %s' % (buyTimeStr, round(self.currentBuyAmountInCryptoWithoutFee, 5), self.theSettings.SETT_GetSettings()['strCryptoType'], round(self.currentBuyInitialPriceInEUR, 5), self.theSettings.SETT_GetSettings()['strFiatType'], round(sellThreshold, 5), self.theSettings.SETT_GetSettings()['strCryptoType'])), False)
        theNotifier.SendWhatsappMessage(('*BUY* %s %s @ %s %s - Waiting for a sell opportunity above %s %s' % (round(self.currentBuyAmountInCryptoWithoutFee, 5), self.theSettings.SETT_GetSettings()['strCryptoType'], round(self.currentBuyInitialPriceInEUR, 5), self.theSettings.SETT_GetSettings()['strFiatType'], round(sellThreshold, 5), self.theSettings.SETT_GetSettings()['strFiatType'])))
        self.theUIGraph.UIGR_addMarker(1)
