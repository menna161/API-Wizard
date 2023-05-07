from datetime import datetime
from PillowImage import PillowImage
from pdfconduit.modify.canvas.objects import CanvasObjects, CanvasStr, CanvasImg


def canvas(self):
    if (self.image is not None):
        self.obj.add(CanvasImg(self.image, opacity=self.opacity, x=0, y=253))
        if (self.text1 and self.text2 and self.copyright):
            self.obj.add(CanvasStr(('© copyright ' + str(datetime.now().year)), size=16, y=(- 170), opacity=self.opacity))
            self.obj.add(CanvasStr(self.text1, opacity=self.opacity, size=40, y=(- 360)))
            self.obj.add(CanvasStr(self.text2, opacity=self.opacity, size=40, y=(- 560)))
        elif (self.text1 and self.text2 and (not self.copyright)):
            self.obj.add(CanvasStr(self.text1, opacity=self.opacity, size=40, y=90))
            self.obj.add(CanvasStr(self.text2, opacity=self.opacity, size=40, y=0))
        elif self.text1:
            self.obj.add(CanvasStr(self.text1, opacity=self.opacity, size=40, y=(- 125)))
        elif self.copyright:
            self.obj.add(CanvasStr(self.text1, opacity=self.opacity, size=40, y=(- 125)))
    elif (self.text1 and self.text2 and self.copyright):
        self.obj.add(CanvasStr(self.text1, opacity=self.opacity, size=80, y=110))
        self.obj.add(CanvasStr(self.text2, opacity=self.opacity, size=80, y=20))
        self.obj.add(CanvasStr(('© copyright ' + str(datetime.now().year)), size=16, y=(- 30), opacity=self.opacity))
    elif (self.text1 and self.text2 and (not self.copyright)):
        self.obj.add(CanvasStr(self.text1, opacity=self.opacity, size=80, y=90))
        self.obj.add(CanvasStr(self.text2, opacity=self.opacity, size=80, y=0))
    elif self.text1:
        self.obj.add(CanvasStr(self.text1, opacity=self.opacity, size=40, y=(- 125)))
    elif self.copyright:
        self.obj.add(CanvasStr(('© copyright ' + str(datetime.now().year)), opacity=self.opacity, size=16, y=50))
    return self.objects
