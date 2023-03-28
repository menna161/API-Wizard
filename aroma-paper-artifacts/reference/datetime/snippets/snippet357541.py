import time
from datetime import datetime
import threading
from GDAXControler import GDAXControler
from UIGraph import UIGraph
import TradingBotConfig as theConfig
import Notifier as theNotifier


def TRNM_SellNow(self, isStopLossSell):
    if ((self.theGDAXControler.GDAX_IsConnectedAndOperational() == 'True') or (theConfig.CONFIG_INPUT_MODE_IS_REAL_MARKET == False)):
        if (self.currentBuyAmountInCryptoWithoutFee >= theConfig.MIN_CRYPTO_AMOUNT_REQUESTED_TO_SELL):
            bOrderIsSuccessful = False
            self.FiatAccountBalance = self.theGDAXControler.GDAX_GetFiatAccountBalance()
            self.CryptoAccountBalance = self.theGDAXControler.GDAX_GetCryptoAccountBalance()
            print(('TRNM - Sell Now (fiat balance is %s, crypto balance is %s)' % (self.FiatAccountBalance, self.CryptoAccountBalance)))
            if (theConfig.CONFIG_INPUT_MODE_IS_REAL_MARKET == True):
                bOrderIsSuccessful = self.theGDAXControler.GDAX_SendSellOrder((self.CryptoAccountBalance - theConfig.CONFIG_CRYPTO_PRICE_QUANTUM))
                self.averageSellPriceInFiat = self.theGDAXControler.GDAX_GetRealTimePriceInEUR()
            else:
                self.averageSellPriceInFiat = self.theMarketData.MRKT_GetLastRefPrice()
            [profitEstimationInFiat, sellPriceWithFeeInFiat] = self.computeProfitEstimation(True, self.currentBuyAmountInCryptoWithFee)
            if (theConfig.CONFIG_INPUT_MODE_IS_REAL_MARKET == False):
                self.FIATAccountBalanceSimulated = (self.FIATAccountBalanceSimulated + sellPriceWithFeeInFiat)
                self.cryptoAccountBalanceSimulated = 0
                self.theUIGraph.UIGR_updateAccountsBalance(round(self.FIATAccountBalanceSimulated, 5), round(self.cryptoAccountBalanceSimulated, 5))
                bOrderIsSuccessful = True
            sellTimeInTimestamp = time.time()
            sellTimeStr = datetime.fromtimestamp(int(sellTimeInTimestamp)).strftime('%Hh%M')
            if (bOrderIsSuccessful == True):
                self.theoricalProfit = (self.theoricalProfit + profitEstimationInFiat)
                if (theConfig.CONFIG_INPUT_MODE_IS_REAL_MARKET == True):
                    currentMidMarketPrice = self.theGDAXControler.GDAX_GetRealTimePriceInEUR()
                else:
                    currentMidMarketPrice = self.theMarketData.MRKT_GetLastRefPrice()
                print(('=== SELL %s at %s EUR. Profit made : %s' % (self.currentBuyAmountInCryptoWithFee, currentMidMarketPrice, profitEstimationInFiat)))
                self.performSellDisplayActions(False, isStopLossSell, currentMidMarketPrice, profitEstimationInFiat)
                self.currentBuyAmountInCryptoWithoutFee = 0
                self.currentBuyAmountInCryptoWithFee = 0
                self.currentSoldAmountInCryptoViaLimitOrder = 0
                self.averageSellPriceInFiat = 0
                self.currentBuyInitialPriceInEUR = 0
                self.buyTimeInTimeStamp = 0
                self.TRNM_RefreshAccountBalancesAndProfit()
            else:
                self.theUIGraph.UIGR_updateInfoText(('%s: Sell order error' % sellTimeStr), True)
            return bOrderIsSuccessful
        else:
            print('TRNM - Trying to sell but no more BTC on the account. Aborted')
            return False
    else:
        print('TRNM - Trying to buy but GDAX Controler not operational. Aborted.')
        return False
