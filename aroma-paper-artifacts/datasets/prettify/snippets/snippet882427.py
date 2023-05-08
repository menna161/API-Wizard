import adsk.core
import adsk.fusion
import traceback
import xml.etree.ElementTree as ET
import math
import xml.dom.minidom as DOM
import os, errno, sys
from collections import defaultdict
from .helpers import *


def exportCASPRbodies(self):
    file = open((((self.fileDir + '/caspr/') + self.modelName) + '_bodies.xml'), 'w')
    file.write('<?xml version="1.0" encoding="utf-8"?>\n')
    file.write('<!DOCTYPE bodies_system SYSTEM "../../../templates/bodies.dtd">\n')
    bodies_system = ET.Element('bodies_system')
    links = ET.SubElement(bodies_system, 'links')
    links.set('display_range', '-0.3 0.3 0.0 1.0 -0.3 0.3')
    links.set('view_angle', '-37 32')
    for (parent_name, (child_name, joint)) in self.joints.items():
        link_rigid = ET.SubElement(links, 'link_rigid')
        link_rigid.set('num', '1')
        link_rigid.set('name', parent_name)
        joi = ET.SubElement(link_rigid, 'joint')
        joi.set('type', 'R_xyx')
        vector = joint.jointMotion.rotationAxisVector
        joi.set('axis', vectorToString(vector.x, vector.y, vector.z))
        joi.set('q_min', str(joint.jointMotion.rotationLimits.minimumValue))
        joi.set('q_max', str(joint.jointMotion.rotationLimits.maximumValue))
        physical = ET.SubElement(link_rigid, 'physical')
        mass = ET.SubElement(physical, 'mass')
        mass.text = str(self.totalMass[parent_name])
        joint_origin = joint.geometryOrOriginOne.origin
        com_origin = self.COM[parent_name]
        com_location = ET.SubElement(physical, 'com_location')
        com_location.text = ((((str(((com_origin.x - joint_origin.x) / 100.0)) + ' ') + str(((com_origin.y - joint_origin.y) / 100.0))) + ' ') + str(((com_origin.z - joint_origin.z) / 100.0)))
        end_location = ET.SubElement(physical, 'end_location')
        end_location.text = '0 0 0'
        inertia = ET.SubElement(physical, 'inertia')
        inertia.set('ref', 'com')
        Ixx = ET.SubElement(inertia, 'Ixx')
        Ixx.text = str(self.inertias[parent_name][0])
        Iyy = ET.SubElement(inertia, 'Iyy')
        Iyy.text = str(self.inertias[parent_name][1])
        Izz = ET.SubElement(inertia, 'Izz')
        Izz.text = str(self.inertias[parent_name][2])
        Ixy = ET.SubElement(inertia, 'Ixy')
        Ixy.text = str(self.inertias[parent_name][3])
        Ixz = ET.SubElement(inertia, 'Ixz')
        Ixz.text = str(self.inertias[parent_name][5])
        Iyz = ET.SubElement(inertia, 'Iyz')
        Iyz.text = str(self.inertias[parent_name][4])
        print(((parent_name + ' ') + str(joint.geometryOrOriginOne.origin.asArray())))
        print(((child_name + ' ') + str(joint.geometryOrOriginTwo.origin.asArray())))
        parent = ET.SubElement(link_rigid, 'parent')
        num = ET.SubElement(parent, 'num')
        num.text = child_name
        location = ET.SubElement(parent, 'location')
        location.text = ((((str((joint_origin.x / 100.0)) + ' ') + str((joint_origin.y / 100.0))) + ' ') + str((joint_origin.z / 100.0)))
    operational_spaces = ET.SubElement(bodies_system, 'operational_spaces')
    operational_spaces.set('default_operational_set', 'test')
    operational_set = ET.SubElement(operational_spaces, 'operational_set')
    operational_set.set('id', 'test')
    position = ET.SubElement(operational_set, 'position')
    position.set('marker_id', '1')
    position.set('name', 'test1')
    link = ET.SubElement(position, 'link')
    link.text = '2'
    offset = ET.SubElement(position, 'offset')
    offset.text = '0.0 0.0 0.0'
    axes = ET.SubElement(position, 'axes')
    axes.set('active_axes', 'x')
    file.write(prettify(bodies_system))
    file.close()
