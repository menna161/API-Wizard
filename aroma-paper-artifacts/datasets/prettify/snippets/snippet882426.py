import adsk.core
import adsk.fusion
import traceback
import xml.etree.ElementTree as ET
import math
import xml.dom.minidom as DOM
import os, errno, sys
from collections import defaultdict
from .helpers import *


def exportCASPRcables(self):
    file = open((((self.fileDir + '/caspr/') + self.modelName) + '_cables.xml'), 'w')
    file.write('<?xml version="1.0" encoding="utf-8"?>\n')
    file.write('<!DOCTYPE cables SYSTEM "../../../templates/cables.dtd">\n')
    cables = ET.Element('cables')
    cables.set('default_cable_set', 'WORKING')
    cable_set = ET.SubElement(cables, 'cable_set')
    cable_set.set('id', 'WORKING')
    i = 0
    for myo in self.myoMuscles:
        cable_ideal = ET.SubElement(cable_set, 'cable_ideal')
        cable_ideal.set('name', ('cable ' + str(i)))
        i = (i + 1)
        cable_ideal.set('attachment_reference', 'com')
        properties = ET.SubElement(cable_ideal, 'properties')
        force_min = ET.SubElement(properties, 'force_min')
        force_min.text = '10'
        force_max = ET.SubElement(properties, 'force_max')
        force_max.text = '80'
        attachments = ET.SubElement(cable_ideal, 'attachments')
        allViaPoints = myo.viaPoints
        allViaPoints.sort(key=(lambda x: x.number))
        for via in allViaPoints:
            attachment = ET.SubElement(attachments, 'attachment')
            link = ET.SubElement(attachment, 'link')
            link.text = via.link
            location = ET.SubElement(attachment, 'location')
            location.text = via.coordinates
    file.write(prettify(cables))
    file.close()
