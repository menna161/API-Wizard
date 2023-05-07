import os, re, sys, bpy, time, bmesh, mathutils
from . import common
import os, sys, urllib, zipfile, subprocess, urllib.request
import addon_utils
import re, urllib, datetime, urllib.request, xml.sax.saxutils


def draw(self, context):
    try:
        import re, urllib, datetime, urllib.request, xml.sax.saxutils
        response = urllib.request.urlopen('https://github.com/CM3Duser/Blender-CM3D2-Converter/commits/master.atom')
        html = response.read().decode('utf-8')
        titles = re.findall('\\<title\\>[\u3000\\s]*([^\u3000\\s][^\\<]*[^\u3000\\s])[\u3000\\s]*\\<\\/title\\>', html)[1:]
        updates = re.findall('\\<updated\\>([^\\<\\>]*)\\<\\/updated\\>', html)[1:]
        links = re.findall('<link [^\\<\\>]*href="([^"]+)"/>', html)[2:]
        version_datetime = datetime.datetime.strptime(((((((((((str(common.bl_info['version'][0]) + ',') + str(common.bl_info['version'][1])) + ',') + str(common.bl_info['version'][2])) + ',') + str(common.bl_info['version'][3])) + ',') + str(common.bl_info['version'][4])) + ',') + str(common.bl_info['version'][5])), '%Y,%m,%d,%H,%M,%S')
        output_data = []
        update_diffs = []
        for (title, update, link) in zip(titles, updates, links):
            title = xml.sax.saxutils.unescape(title, {'&quot;': '"'})
            rss_datetime = (datetime.datetime.strptime(update, '%Y-%m-%dT%H:%M:%SZ') + datetime.timedelta(hours=9))
            diff_seconds = (datetime.datetime.now() - rss_datetime)
            icon = 'SORTTIME'
            if ((((60 * 60) * 24) * 7) < diff_seconds.total_seconds()):
                icon = 'NLA'
            elif ((((60 * 60) * 24) * 3) < diff_seconds.total_seconds()):
                icon = 'COLLAPSEMENU'
            elif (((60 * 60) * 24) < diff_seconds.total_seconds()):
                icon = 'TIME'
            elif ((60 * 60) < diff_seconds.total_seconds()):
                icon = 'RECOVER_LAST'
            else:
                icon = 'PREVIEW_RANGE'
            if (((60 * 60) * 24) <= diff_seconds.total_seconds()):
                date_str = ('%d日前' % int((((diff_seconds.total_seconds() / 60) / 60) / 24)))
            elif ((60 * 60) <= diff_seconds.total_seconds()):
                date_str = ('%d時間前' % int(((diff_seconds.total_seconds() / 60) / 60)))
            elif (60 <= diff_seconds.total_seconds()):
                date_str = ('%d分前' % int((diff_seconds.total_seconds() / 60)))
            else:
                date_str = ('%d秒前' % diff_seconds.total_seconds())
            text = ((('(' + date_str) + ') ') + title)
            update_diff = abs((version_datetime - rss_datetime).total_seconds())
            output_data.append((text, icon, link, update_diff))
            update_diffs.append(update_diff)
        min_update_diff = sorted(update_diffs)[0]
        for (text, icon, link, update_diff) in output_data:
            if (update_diff == min_update_diff):
                text = ('Now! ' + text)
                icon = 'QUESTION'
            self.layout.operator('wm.url_open', text=text, icon=icon).url = link
    except:
        self.layout.label(text='更新の取得に失敗しました', icon='ERROR')
