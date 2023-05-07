import sys, os
import qtpy
import pyqtgraph as pg
import datetime as dt
import numpy as np
import traceback
import pandas as pd
from qtpy import QtGui, QtCore
from pyqtgraph.Point import Point


def plotInfo(self, xAxis, yAxis):
    '\n        被嵌入的plotWidget在需要的时候通过调用此方法显示K线信息\n        '
    if (self.datas is None):
        return
    try:
        data = self.datas[xAxis]
        lastdata = self.datas[(xAxis - 1)]
        tickDatetime = data['datetime']
        openPrice = data['open']
        closePrice = data['close']
        lowPrice = data['low']
        highPrice = data['high']
        volume = int(data['volume'])
        openInterest = int(data['openInterest'])
        preClosePrice = lastdata['close']
        MA_S = 0
        if ((len(self.ma_s_values) > 0) and (self.master.MA_SHORT_show == True)):
            MA_S = self.ma_s_values[xAxis]
        MA_L = 0
        if ((len(self.ma_l_values) > 0) and (self.master.MA_LONG_show == True)):
            MA_L = self.ma_l_values[xAxis]
        tradePrice = 0
        if ((cmp(self.master.listSig_deal_DIRECTION[xAxis], '-') == 0) or (cmp(self.master.listSig_deal_OFFSET[xAxis], '-') == 0)):
            tradePrice = 0
        else:
            tradePrice = closePrice
    except Exception as e:
        return
    if isinstance(tickDatetime, dt.datetime):
        datetimeText = dt.datetime.strftime(tickDatetime, '%Y-%m-%d %H:%M:%S')
        dateText = dt.datetime.strftime(tickDatetime, '%Y-%m-%d')
        timeText = dt.datetime.strftime(tickDatetime, '%H:%M:%S')
    else:
        '\n            datetimeText = ""\n            dateText     = ""\n            timeText     = ""\n            '
        datetimeText = dt.datetime.strftime(pd.to_datetime(pd.to_datetime(tickDatetime)), '%Y-%m-%d %H:%M:%S')
        dateText = dt.datetime.strftime(pd.to_datetime(pd.to_datetime(tickDatetime)), '%Y-%m-%d')
        timeText = dt.datetime.strftime(pd.to_datetime(pd.to_datetime(tickDatetime)), '%H:%M:%S')
    html = u'<div style="text-align: right">'
    for sig in self.master.sigData:
        val = self.master.sigData[sig][xAxis]
        col = self.master.sigColor[sig]
        html += (u'<span style="color: %s;  font-size: 12px;">&nbsp;&nbsp;%s：%.2f</span>' % (col, sig, val))
    html += u'</div>'
    self.__textSig.setHtml(html)
    html = u'<div style="text-align: right">'
    for sig in self.master.subSigData:
        val = self.master.subSigData[sig][xAxis]
        col = self.master.subSigColor[sig]
        html += (u'<span style="color: %s;  font-size: 12px;">&nbsp;&nbsp;%s：%.2f</span>' % (col, sig, val))
    html += u'</div>'
    self.__textSubSig.setHtml(html)
    cOpen = ('red' if (openPrice > preClosePrice) else 'green')
    cClose = ('red' if (closePrice > preClosePrice) else 'green')
    cHigh = ('red' if (highPrice > preClosePrice) else 'green')
    cLow = ('red' if (lowPrice > preClosePrice) else 'green')
    self.__textInfo.setHtml((u'<div style="text-align: center; background-color:#000">                                <span style="color: white;  font-size: 12px;">日期</span><br>                                <span style="color: yellow; font-size: 12px;">%s</span><br>                                <span style="color: white;  font-size: 12px;">价格</span><br>                                <span style="color: %s;     font-size: 12px;">(开) %d</span><br>                                <span style="color: %s;     font-size: 12px;">(高) %d</span><br>                                <span style="color: %s;     font-size: 12px;">(低) %d</span><br>                                <span style="color: %s;     font-size: 12px;">(收) %d</span><br>                                <span style="color: white;  font-size: 12px;">成交价</span><br>                                <span style="color: yellow; font-size: 12px;">(价) %d</span><br>                                <span style="color: white;  font-size: 12px;">指标</span><br>                                <span style="color: yellow; font-size: 12px;">(NOW) %.0f</span><br>                                <span style="color: yellow; font-size: 12px;">(BEF) %.0f</span><br>                            </div>' % (dateText, cOpen, openPrice, cHigh, highPrice, cLow, lowPrice, cClose, closePrice, tradePrice, MA_S, MA_L)))
    self.__textDate.setHtml(('<div style="text-align: center">                                <span style="color: yellow; font-size: 12px;">%s</span>                            </div>' % dateText))
    self.__textVolume.setHtml(('<div style="text-align: right">                                <span style="color: white; font-size: 12px;">VOL : %d</span>                            </div>' % volume))
    rightAxisWidth = self.views[0].getAxis('right').width()
    bottomAxisHeight = self.views[2].getAxis('bottom').height()
    offset = QtCore.QPointF(rightAxisWidth, bottomAxisHeight)
    tl = [self.views[i].vb.mapSceneToView(self.rects[i].topLeft()) for i in range(3)]
    br = [self.views[i].vb.mapSceneToView((self.rects[i].bottomRight() - offset)) for i in range(3)]
    for i in range(3):
        if self.showHLine[i]:
            self.textPrices[i].setHtml(('<div style="text-align: right">                             <span style="color: yellow; font-size: 12px;">                               %d                             </span>                         </div>' % (yAxis if (i == 0) else self.yAxises[i])))
            self.textPrices[i].setPos(br[i].x(), (yAxis if (i == 0) else self.yAxises[i]))
            self.textPrices[i].show()
        else:
            self.textPrices[i].hide()
    self.__textInfo.setPos(tl[0])
    self.__textSig.setPos(br[0].x(), tl[0].y())
    self.__textSubSig.setPos(br[2].x(), tl[2].y())
    self.__textVolume.setPos(br[1].x(), tl[1].y())
    self.__textDate.anchor = (Point((1, 1)) if (xAxis > self.master.index) else Point((0, 1)))
    self.__textDate.setPos(xAxis, br[2].y())
