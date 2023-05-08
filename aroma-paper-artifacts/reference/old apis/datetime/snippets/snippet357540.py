import time
from datetime import datetime
import threading
from GDAXControler import GDAXControler
from UIGraph import UIGraph
import TradingBotConfig as theConfig
import Notifier as theNotifier


def TRNM_BuyNow(self):
    if ((self.theGDAXControler.GDAX_IsConnectedAndOperational() == 'True') or (theConfig.CONFIG_INPUT_MODE_IS_REAL_MARKET == False)):
        if (self.currentBuyAmountInCryptoWithoutFee == 0):
            bOrderIsSuccessful = False
            bAmountIsAboveMinimumRequested = False
            self.FiatAccountBalance = self.theGDAXControler.GDAX_GetFiatAccountBalance()
            self.CryptoAccountBalance = self.theGDAXControler.GDAX_GetCryptoAccountBalance()
            BuyCapabilityInCrypto = self.computeBuyCapabilityInCrypto(False)
            print(('TRNM - Buy Now, capability is: %s Crypto (fiat balance is %s, crypto balance is %s)' % (BuyCapabilityInCrypto, self.FiatAccountBalance, self.CryptoAccountBalance)))
            if (theConfig.CONFIG_INPUT_MODE_IS_REAL_MARKET == True):
                self.currentBuyInitialPriceInEUR = self.theGDAXControler.GDAX_GetRealTimePriceInEUR()
            else:
                self.currentBuyInitialPriceInEUR = self.theMarketData.MRKT_GetLastRefPrice()
            ratioOfCryptoCapabilityToBuy = (float(self.theSettings.SETT_GetSettings()['investPercentage']) * 0.01)
            self.currentBuyAmountInCryptoWithoutFee = (BuyCapabilityInCrypto * ratioOfCryptoCapabilityToBuy)
            self.currentBuyAmountInCryptoWithFee = ((BuyCapabilityInCrypto * ratioOfCryptoCapabilityToBuy) * (1 - self.platformTakerFeeInPercent))
            print(('TRNM - Buy Now, amount is: %s Crypto' % self.currentBuyAmountInCryptoWithoutFee))
            bAmountIsAboveMinimumRequested = self.theGDAXControler.GDAX_IsAmountToBuyAboveMinimum(self.currentBuyAmountInCryptoWithoutFee)
            print(('TRNM - Amount to buy is above minimum possible ? %s' % bAmountIsAboveMinimumRequested))
            if (bAmountIsAboveMinimumRequested == True):
                if (theConfig.CONFIG_INPUT_MODE_IS_REAL_MARKET == True):
                    bOrderIsSuccessful = self.theGDAXControler.GDAX_SendBuyOrder(self.currentBuyAmountInCryptoWithoutFee)
                else:
                    self.FIATAccountBalanceSimulated = (self.FIATAccountBalanceSimulated - (self.FIATAccountBalanceSimulated * ratioOfCryptoCapabilityToBuy))
                    self.cryptoAccountBalanceSimulated = self.currentBuyAmountInCryptoWithFee
                    self.theUIGraph.UIGR_updateAccountsBalance(round(self.FIATAccountBalanceSimulated, 5), round(self.cryptoAccountBalanceSimulated, 5))
                    bOrderIsSuccessful = True
            self.buyTimeInTimeStamp = time.time()
            print(('TRNM - === BUY %s Crypto at %s Fiat' % (self.currentBuyAmountInCryptoWithoutFee, self.currentBuyInitialPriceInEUR)))
            buyTimeStr = datetime.fromtimestamp(int(self.buyTimeInTimeStamp)).strftime('%H:%M')
            if (bOrderIsSuccessful == True):
                self.performBuyDisplayActions(False)
            else:
                self.currentBuyAmountInCryptoWithoutFee = 0
                self.currentBuyAmountInCryptoWithFee = 0
                self.currentSoldAmountInCryptoViaLimitOrder = 0
                self.averageSellPriceInFiat = 0
                self.currentBuyInitialPriceInEUR = 0
                if (bAmountIsAboveMinimumRequested == False):
                    self.theUIGraph.UIGR_updateInfoText(('%s: Buy order error: amount is too low, increase your %s balance' % (buyTimeStr, self.theSettings.SETT_GetSettings()['strFiatType'])), True)
                else:
                    self.theUIGraph.UIGR_updateInfoText(('%s: Buy order error' % buyTimeStr), True)
            return bOrderIsSuccessful
        else:
            print("TRNM - Trying to buy but there's already a pending buy. Aborted.")
            return False
    else:
        print('TRNM - Trying to buy but GDAX Controler not operational. Aborted.')
        return False
