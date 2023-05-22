import time
from datetime import datetime
import threading
from GDAXControler import GDAXControler
from UIGraph import UIGraph
import TradingBotConfig as theConfig
import Notifier as theNotifier


def performSellDisplayActions(self, isLimitOrder, isStopLossSell, sellPriceInFiat, profitEstimationInFiat):
    sellTimeInTimestamp = time.time()
    sellTimeStr = datetime.fromtimestamp(int(sellTimeInTimestamp)).strftime('%Hh%M')
    if isLimitOrder:
        if (self.isOrderPlacingActive == False):
            self.theUIGraph.UIGR_updateInfoText(('SELL filled at %s, profit was about %s EUR. Waiting for next buy opportunity' % (sellTimeStr, round(profitEstimationInFiat, 5))), False)
            self.pendingNotificationToSend = ('*SELL filled* at %s %s, profit was about *%s EUR*. ' % (round(sellPriceInFiat, 5), self.theSettings.SETT_GetSettings()['strFiatType'], round(profitEstimationInFiat, 5)))
            self.theUIGraph.UIGR_addMarker(2)
        else:
            self.theUIGraph.UIGR_updateInfoText(('Partial sell at %s, profit was about %s EUR. Still ongoing, waiting for next matches' % (sellTimeStr, round(profitEstimationInFiat, 5))), False)
            self.pendingNotificationToSend = ('*SELL match* at %s %s, profit was about *%s EUR*. ' % (round(sellPriceInFiat, 5), self.theSettings.SETT_GetSettings()['strFiatType'], round(profitEstimationInFiat, 5)))
    else:
        if (isStopLossSell == False):
            self.theUIGraph.UIGR_updateInfoText(('Last sell at %s, profit was about %s EUR. Waiting for next buy opportunity' % (sellTimeStr, round(profitEstimationInFiat, 5))), False)
            self.pendingNotificationToSend = ('*SELL* at %s %s, profit was about *%s EUR*. ' % (round(sellPriceInFiat, 5), self.theSettings.SETT_GetSettings()['strFiatType'], round(profitEstimationInFiat, 5)))
        else:
            self.theUIGraph.UIGR_updateInfoText(('StopLoss-sell at %s, loss was about %s EUR. Waiting for next buy opportunity' % (sellTimeStr, round(profitEstimationInFiat, 5))), True)
            self.pendingNotificationToSend = ('*STOPLOSS-SELL* at %s %s, loss was about *%s EUR*. ' % (round(sellPriceInFiat, 5), self.theSettings.SETT_GetSettings()['strFiatType'], round(profitEstimationInFiat, 5)))
        self.theUIGraph.UIGR_addMarker(2)
