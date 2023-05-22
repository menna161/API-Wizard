import xml.etree.ElementTree as ET
import xml.dom.minidom as DOM


def prettify(elem):
    'Return a pretty-printed XML string for the Element.\n    '
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = DOM.parseString(rough_string)
    return reparsed.toprettyxml(indent='\t')
