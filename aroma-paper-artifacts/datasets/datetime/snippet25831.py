from datetime import datetime
from PillowImage import PillowImage
from pdfconduit.modify.canvas.objects import CanvasObjects, CanvasStr, CanvasImg


def img(self):
    with PillowImage() as img:
        if (self.image is not None):
            img.draw_img(self.image, x=0, y=50, opacity=self.opacity)
            if (self.text1 and self.text2 and self.copyright):
                img.draw_text(self.text1, font_size=40, y=416, opacity=self.opacity)
                img.draw_text(self.text2, font_size=40, y=466, opacity=self.opacity)
                img.draw_text(('© copyright ' + str(datetime.now().year)), font_size=16, y='center')
            elif (self.text1 and self.text2 and (not self.copyright)):
                img.draw_text(self.text1, font_size=40, y=416, opacity=self.opacity)
                img.draw_text(self.text2, font_size=40, y=466, opacity=self.opacity)
            elif self.text1:
                self.obj.add(CanvasStr(self.text1, opacity=self.opacity, size=40, y=(- 125)))
            elif self.copyright:
                img.draw_text(('© copyright ' + str(datetime.now().year)), font_size=16, y='center')
        elif (self.text1 and self.text2 and self.copyright):
            img.draw_text(('© copyright ' + str(datetime.now().year)), font_size=16, y=350)
            img.draw_text(self.text1, font_size=80, y=106, opacity=self.opacity)
            img.draw_text(self.text2, font_size=80, y=206, opacity=self.opacity)
        elif (self.text1 and self.text2 and (not self.copyright)):
            img.draw_text(self.text1, font_size=80, y=106, opacity=self.opacity)
            img.draw_text(self.text2, font_size=80, y=206, opacity=self.opacity)
        elif self.text1:
            img.draw_text(self.text1, font_size=80, y=106, opacity=self.opacity)
        elif self.copyright:
            img.draw_text(('© copyright ' + str(datetime.now().year)), font_size=16, y=350)
        img.rotate(self.rotate)
        self.rotate = 0
        i = img.save(destination=self.tempdir)
        self.obj.add(CanvasImg(i, opacity=1, centered=True))
        return self.objects
