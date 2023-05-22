import os
import numpy as np
from PySide6 import QtGui, QtCore, QtWidgets
import PyAero
import Airfoil
import FileDialog
import FileSystem
import SvpMethod
import SplineRefine
import TrailingEdge
import Meshing
import ContourAnalysis as ca
from Settings import ICONS_L
import logging


def valuechange(self):
    if (self.aoaf.value() >= self.aoat.value()):
        self.aoaf.setValue((self.aoat.value() - self.aoas.value()))
    if (self.aoat.value() <= self.aoaf.value()):
        self.aoat.setValue((self.aoaf.value() + self.aoas.value()))
    gas_constant = 287.14
    temperature = (self.temperature.value() + 273.15)
    self.density = ((self.pressure.value() / gas_constant) / temperature)
    num = int((((self.aoat.value() - self.aoaf.value()) / self.aoas.value()) + 1))
    self.aoa = np.linspace(self.aoaf.value(), self.aoat.value(), num=num, endpoint=True)

    def dynamic_viscosity(temperature):
        C = 120.0
        lamb = 1.512041288e-06
        vis = ((lamb * (temperature ** 1.5)) / (temperature + C))
        return vis
    self.dynamic_viscosity = dynamic_viscosity(temperature)
    self.kinematic_viscosity = (self.dynamic_viscosity / self.density)
    velocity = ((self.reynolds.value() / self.chord.value()) * self.kinematic_viscosity)
    uprime = ((velocity * self.turbulence.value()) / 100.0)
    tke = ((3.0 / 2.0) * (uprime ** 2))
    self.u_velocity = (velocity * np.cos(((self.aoa * np.pi) / 180.0)))
    self.v_velocity = (velocity * np.sin(((self.aoa * np.pi) / 180.0)))
    RE = self.reynolds.value()
    log10 = np.log10(RE)
    logRE = np.power(log10, 2.58)
    if (RE < 5100000.0):
        friction_coefficient = (0.455 / logRE)
    else:
        friction_coefficient = ((0.455 / logRE) - (1700.0 / RE))
    wall_shear_stress = (((friction_coefficient * 0.5) * self.density) * (velocity ** 2))
    friction_velocity = np.sqrt((wall_shear_stress / self.density))
    wall_distance = (((self.yplus.value() * self.dynamic_viscosity) / self.density) / friction_velocity)
    newline = '<br>'
    self.te_text = ('<b>CFD Boundary Conditions</b>' + newline)
    self.te_text += (f'Reynolds (-): {self.reynolds.value()}' + newline)
    self.te_text += (f'Pressure (Pa): {self.pressure.value()}' + newline)
    self.te_text += (f'Temperature (C): {self.temperature.value()}' + newline)
    self.te_text += (f'Temperature (K): {(self.temperature.value() + 273.15)}' + newline)
    self.te_text += (f'Density (kg/(m<sup>3</sup>)): {self.density}' + newline)
    self.te_text += (f'Dynamic viscosity (kg/(m.s)): {self.dynamic_viscosity}' + newline)
    self.te_text += (f'Kinematic viscosity (m/s) {self.kinematic_viscosity}:' + newline)
    self.te_text += (f'<b>1st cell layer thickness (m)</b>, for y<sup>+</sup>={self.yplus.value()}' + newline)
    self.te_text += ('{:16.8f}'.format(wall_distance) + newline)
    self.te_text += ('<b>TKE (m<sup>2</sup>/s<sup>2</sup>), Length-scale (m)</b>' + newline)
    self.te_text += ('{:16.8f} {:16.8f}'.format(tke, self.length_sc.value()) + newline)
    self.te_text += ('<b>AOA (°)   u-velocity (m/s)   v-velocity (m/s)</b>' + newline)
    for (i, _) in enumerate(self.u_velocity):
        self.te_text += '{: >5.2f} {: >16.8f} {: >16.8f}{}'.format(self.aoa[i], self.u_velocity[i], self.v_velocity[i], newline)
    self.textedit.setStyleSheet('font-family: Courier; font-size: 12px; ')
    self.textedit.setHtml(self.te_text)
