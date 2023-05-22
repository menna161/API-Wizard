import copy
import csv
import io
import json
import logging
import math
import numpy as np
import pyproj
import zipfile
from auvsi_suas.models import distance
from auvsi_suas.models import mission_evaluation
from auvsi_suas.models import units
from auvsi_suas.models.mission_config import MissionConfig
from auvsi_suas.models.takeoff_or_landing_event import TakeoffOrLandingEvent
from auvsi_suas.models.uas_telemetry import UasTelemetry
from auvsi_suas.patches.simplekml_patch import AltitudeMode
from auvsi_suas.patches.simplekml_patch import Color
from auvsi_suas.patches.simplekml_patch import Kml
from auvsi_suas.patches.simplekml_patch import RefreshMode
from auvsi_suas.proto import interop_api_pb2
from auvsi_suas.views.decorators import require_login
from auvsi_suas.views.decorators import require_superuser
from auvsi_suas.views.json import ProtoJsonEncoder
from datetime import timedelta
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseForbidden
from django.http import HttpResponseNotFound
from django.http import HttpResponseServerError
from django.template.loader import get_template
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.views.generic import View
from google.protobuf import json_format


def mission_kml(mission, kml, kml_doc):
    '\n    Appends kml nodes describing the mission.\n\n    Args:\n        mission: The mission to add to the KML.\n        kml: A simpleKML Container to which the mission data will be added\n        kml_doc: The simpleKML Document to which schemas will be added\n\n    Returns:\n        The KML folder for the mission data.\n    '
    mission_name = 'Mission {}'.format(mission.pk)
    kml_folder = kml.newfolder(name=mission_name)
    wgs_to_utm = pyproj.transformer.Transformer.from_proj(distance.proj_wgs84, distance.proj_utm(mission.home_pos.latitude, mission.home_pos.longitude))
    wgs_to_web_mercator = pyproj.transformer.Transformer.from_proj(distance.proj_wgs84, distance.proj_web_mercator)
    fly_zone_folder = kml_folder.newfolder(name='Fly Zones')
    for flyzone in mission.fly_zones.all():
        fly_zone_kml(flyzone, fly_zone_folder)
    locations = [('Home', mission.home_pos, KML_HOME_ICON), ('Emergent LKP', mission.emergent_last_known_pos, KML_ODLC_ICON), ('Off Axis', mission.off_axis_odlc_pos, KML_ODLC_ICON), ('Air Drop', mission.air_drop_pos, KML_DROP_ICON), ('Map Center', mission.map_center_pos, KML_MAP_CENTER_ICON)]
    for (key, point, icon) in locations:
        gps = (point.longitude, point.latitude)
        p = kml_folder.newpoint(name=key, coords=[gps])
        p.iconstyle.icon.href = icon
        p.description = str(point)
    oldc_folder = kml_folder.newfolder(name='ODLCs')
    for odlc in mission.odlcs.select_related().all():
        name = ('ODLC %d' % odlc.pk)
        gps = (odlc.location.longitude, odlc.location.latitude)
        p = oldc_folder.newpoint(name=name, coords=[gps])
        p.iconstyle.icon.href = KML_ODLC_ICON
        p.description = name
    waypoints_folder = kml_folder.newfolder(name='Waypoints')
    linestring = waypoints_folder.newlinestring(name='Waypoints')
    waypoints = []
    for (i, waypoint) in enumerate(mission.mission_waypoints.order_by('order')):
        coord = (waypoint.longitude, waypoint.latitude, units.feet_to_meters(waypoint.altitude_msl))
        waypoints.append(coord)
        p = waypoints_folder.newpoint(name=('Waypoint %d' % (i + 1)), coords=[coord])
        p.iconstyle.icon.href = KML_WAYPOINT_ICON
        p.description = str(waypoint)
        p.altitudemode = AltitudeMode.absolute
        p.extrude = 1
    linestring.coords = waypoints
    linestring.altitudemode = AltitudeMode.absolute
    linestring.extrude = 1
    linestring.style.linestyle.color = Color.green
    linestring.style.polystyle.color = Color.changealphaint(100, Color.green)
    search_area = []
    for point in mission.search_grid_points.order_by('order'):
        coord = (point.longitude, point.latitude, units.feet_to_meters(point.altitude_msl))
        search_area.append(coord)
    if search_area:
        search_area.append(search_area[0])
        pol = kml_folder.newpolygon(name='Search Area')
        pol.outerboundaryis = search_area
        pol.style.linestyle.color = Color.blue
        pol.style.linestyle.width = 2
        pol.style.polystyle.color = Color.changealphaint(50, Color.blue)
    (map_x, map_y) = wgs_to_web_mercator.transform(mission.map_center_pos.longitude, mission.map_center_pos.latitude)
    map_height = units.feet_to_meters(mission.map_height_ft)
    map_width = ((map_height * 16) / 9)
    map_points = [((map_x - (map_width / 2)), (map_y - (map_height / 2))), ((map_x + (map_width / 2)), (map_y - (map_height / 2))), ((map_x + (map_width / 2)), (map_y + (map_height / 2))), ((map_x - (map_width / 2)), (map_y + (map_height / 2))), ((map_x - (map_width / 2)), (map_y - (map_height / 2)))]
    map_points = [wgs_to_web_mercator.transform(px, py, direction=pyproj.enums.TransformDirection.INVERSE) for (px, py) in map_points]
    map_points = [(x, y, 0) for (x, y) in map_points]
    map_pol = kml_folder.newpolygon(name='Map')
    map_pol.outerboundaryis = map_points
    map_pol.style.linestyle.color = Color.green
    map_pol.style.linestyle.width = 2
    map_pol.style.polystyle.color = Color.changealphaint(50, Color.green)
    stationary_obstacles_folder = kml_folder.newfolder(name='Stationary Obstacles')
    for obst in mission.stationary_obstacles.all():
        (cx, cy) = wgs_to_utm.transform(obst.longitude, obst.latitude)
        rm = units.feet_to_meters(obst.cylinder_radius)
        hm = units.feet_to_meters(obst.cylinder_height)
        obst_points = []
        for angle in np.linspace(0, (2 * math.pi), num=KML_OBST_NUM_POINTS):
            px = (cx + (rm * math.cos(angle)))
            py = (cy + (rm * math.sin(angle)))
            (lon, lat) = wgs_to_utm.transform(px, py, direction=pyproj.enums.TransformDirection.INVERSE)
            obst_points.append((lon, lat, hm))
        pol = stationary_obstacles_folder.newpolygon(name=('Obstacle %d' % obst.pk))
        pol.outerboundaryis = obst_points
        pol.altitudemode = AltitudeMode.absolute
        pol.extrude = 1
        pol.style.linestyle.color = Color.yellow
        pol.style.linestyle.width = 2
        pol.style.polystyle.color = Color.changealphaint(50, Color.yellow)
    return kml_folder
