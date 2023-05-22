import copy
from numbers import Integral
import numpy as np
from . import rcParams
from .lines import Line2D
from .patches import Circle, Rectangle, Ellipse
from .transforms import blended_transform_factory


def __init__(self, targetfig, toolfig):
    '\n        *targetfig*\n            The figure instance to adjust.\n\n        *toolfig*\n            The figure instance to embed the subplot tool into. If\n            *None*, a default figure will be created. If you are using\n            this from the GUI\n        '
    self.targetfig = targetfig
    toolfig.subplots_adjust(left=0.2, right=0.9)

    class toolbarfmt():

        def __init__(self, slider):
            self.slider = slider

        def __call__(self, x, y):
            fmt = ('%s=%s' % (self.slider.label.get_text(), self.slider.valfmt))
            return (fmt % x)
    self.axleft = toolfig.add_subplot(711)
    self.axleft.set_title('Click on slider to adjust subplot param')
    self.axleft.set_navigate(False)
    self.sliderleft = Slider(self.axleft, 'left', 0, 1, targetfig.subplotpars.left, closedmax=False)
    self.sliderleft.on_changed(self.funcleft)
    self.axbottom = toolfig.add_subplot(712)
    self.axbottom.set_navigate(False)
    self.sliderbottom = Slider(self.axbottom, 'bottom', 0, 1, targetfig.subplotpars.bottom, closedmax=False)
    self.sliderbottom.on_changed(self.funcbottom)
    self.axright = toolfig.add_subplot(713)
    self.axright.set_navigate(False)
    self.sliderright = Slider(self.axright, 'right', 0, 1, targetfig.subplotpars.right, closedmin=False)
    self.sliderright.on_changed(self.funcright)
    self.axtop = toolfig.add_subplot(714)
    self.axtop.set_navigate(False)
    self.slidertop = Slider(self.axtop, 'top', 0, 1, targetfig.subplotpars.top, closedmin=False)
    self.slidertop.on_changed(self.functop)
    self.axwspace = toolfig.add_subplot(715)
    self.axwspace.set_navigate(False)
    self.sliderwspace = Slider(self.axwspace, 'wspace', 0, 1, targetfig.subplotpars.wspace, closedmax=False)
    self.sliderwspace.on_changed(self.funcwspace)
    self.axhspace = toolfig.add_subplot(716)
    self.axhspace.set_navigate(False)
    self.sliderhspace = Slider(self.axhspace, 'hspace', 0, 1, targetfig.subplotpars.hspace, closedmax=False)
    self.sliderhspace.on_changed(self.funchspace)
    self.sliderleft.slidermax = self.sliderright
    self.sliderright.slidermin = self.sliderleft
    self.sliderbottom.slidermax = self.slidertop
    self.slidertop.slidermin = self.sliderbottom
    bax = toolfig.add_axes([0.8, 0.05, 0.15, 0.075])
    self.buttonreset = Button(bax, 'Reset')
    sliders = (self.sliderleft, self.sliderbottom, self.sliderright, self.slidertop, self.sliderwspace, self.sliderhspace)

    def func(event):
        thisdrawon = self.drawon
        self.drawon = False
        bs = []
        for slider in sliders:
            bs.append(slider.drawon)
            slider.drawon = False
        for slider in sliders:
            slider.reset()
        for (slider, b) in zip(sliders, bs):
            slider.drawon = b
        self.drawon = thisdrawon
        if self.drawon:
            toolfig.canvas.draw()
            self.targetfig.canvas.draw()
    validate = toolfig.subplotpars.validate
    toolfig.subplotpars.validate = False
    self.buttonreset.on_clicked(func)
    toolfig.subplotpars.validate = validate
