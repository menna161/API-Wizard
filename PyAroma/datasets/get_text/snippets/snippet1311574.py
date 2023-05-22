import copy
from matplotlib import artist, lines as mlines, axis as maxis, patches as mpatches, rcParams
from . import art3d, proj3d
import numpy as np


@artist.allow_rasterization
def draw(self, renderer):
    self.label._transform = self.axes.transData
    renderer.open_group('axis3d')
    majorTicks = self.get_major_ticks()
    majorLocs = self.major.locator()
    info = self._axinfo
    index = info['i']
    (locmin, locmax) = self.get_view_interval()
    if (locmin > locmax):
        (locmin, locmax) = (locmax, locmin)
    majorLocs = [loc for loc in majorLocs if (locmin <= loc <= locmax)]
    self.major.formatter.set_locs(majorLocs)
    majorLabels = [self.major.formatter(val, i) for (i, val) in enumerate(majorLocs)]
    (mins, maxs, centers, deltas, tc, highs) = self._get_coord_info(renderer)
    minmax = np.where(highs, maxs, mins)
    juggled = info['juggled']
    edgep1 = minmax.copy()
    edgep1[juggled[0]] = get_flip_min_max(edgep1, juggled[0], mins, maxs)
    edgep2 = edgep1.copy()
    edgep2[juggled[1]] = get_flip_min_max(edgep2, juggled[1], mins, maxs)
    pep = proj3d.proj_trans_points([edgep1, edgep2], renderer.M)
    centpt = proj3d.proj_transform(centers[0], centers[1], centers[2], renderer.M)
    self.line.set_data((pep[0][0], pep[0][1]), (pep[1][0], pep[1][1]))
    self.line.draw(renderer)
    xyz0 = []
    for val in majorLocs:
        coord = minmax.copy()
        coord[index] = val
        xyz0.append(coord)
    peparray = np.asanyarray(pep)
    (dx, dy) = (self.axes.transAxes.transform([peparray[(0:2, 1)]]) - self.axes.transAxes.transform([peparray[(0:2, 0)]]))[0]
    lxyz = (0.5 * (edgep1 + edgep2))
    ax_scale = (self.axes.bbox.size / self.figure.bbox.size)
    ax_inches = np.multiply(ax_scale, self.figure.get_size_inches())
    ax_points_estimate = sum((72.0 * ax_inches))
    deltas_per_point = (48 / ax_points_estimate)
    default_offset = 21.0
    labeldeltas = (((self.labelpad + default_offset) * deltas_per_point) * deltas)
    axmask = [True, True, True]
    axmask[index] = False
    lxyz = move_from_center(lxyz, centers, labeldeltas, axmask)
    (tlx, tly, tlz) = proj3d.proj_transform(lxyz[0], lxyz[1], lxyz[2], renderer.M)
    self.label.set_position((tlx, tly))
    if self.get_rotate_label(self.label.get_text()):
        angle = art3d.norm_text_angle(np.rad2deg(np.arctan2(dy, dx)))
        self.label.set_rotation(angle)
    self.label.set_va(info['label']['va'])
    self.label.set_ha(info['label']['ha'])
    self.label.draw(renderer)
    if (juggled[2] == 2):
        outeredgep = edgep1
        outerindex = 0
    else:
        outeredgep = edgep2
        outerindex = 1
    pos = copy.copy(outeredgep)
    pos = move_from_center(pos, centers, labeldeltas, axmask)
    (olx, oly, olz) = proj3d.proj_transform(pos[0], pos[1], pos[2], renderer.M)
    self.offsetText.set_text(self.major.formatter.get_offset())
    self.offsetText.set_position((olx, oly))
    angle = art3d.norm_text_angle(np.rad2deg(np.arctan2(dy, dx)))
    self.offsetText.set_rotation(angle)
    self.offsetText.set_rotation_mode('anchor')
    if (centpt[info['tickdir']] > peparray[(info['tickdir'], outerindex)]):
        if ((centpt[index] <= peparray[(index, outerindex)]) and ((len(highs.nonzero()[0]) % 2) == 0)):
            if ((highs.tolist() == [False, True, True]) and (index in (1, 2))):
                align = 'left'
            else:
                align = 'right'
        else:
            align = 'left'
    elif ((centpt[index] > peparray[(index, outerindex)]) and ((len(highs.nonzero()[0]) % 2) == 0)):
        if (index == 2):
            align = 'right'
        else:
            align = 'left'
    else:
        align = 'right'
    self.offsetText.set_va('center')
    self.offsetText.set_ha(align)
    self.offsetText.draw(renderer)
    if (len(xyz0) > 0):
        xyz1 = copy.deepcopy(xyz0)
        newindex = ((index + 1) % 3)
        newval = get_flip_min_max(xyz1[0], newindex, mins, maxs)
        for i in range(len(majorLocs)):
            xyz1[i][newindex] = newval
        xyz2 = copy.deepcopy(xyz0)
        newindex = ((index + 2) % 3)
        newval = get_flip_min_max(xyz2[0], newindex, mins, maxs)
        for i in range(len(majorLocs)):
            xyz2[i][newindex] = newval
        lines = list(zip(xyz1, xyz0, xyz2))
        if self.axes._draw_grid:
            self.gridlines.set_segments(lines)
            self.gridlines.set_color(([info['grid']['color']] * len(lines)))
            self.gridlines.set_linewidth(([info['grid']['linewidth']] * len(lines)))
            self.gridlines.set_linestyle(([info['grid']['linestyle']] * len(lines)))
            self.gridlines.draw(renderer, project=True)
    tickdir = info['tickdir']
    tickdelta = deltas[tickdir]
    if highs[tickdir]:
        ticksign = 1
    else:
        ticksign = (- 1)
    for (tick, loc, label) in zip(majorTicks, majorLocs, majorLabels):
        if (tick is None):
            continue
        pos = copy.copy(edgep1)
        pos[index] = loc
        pos[tickdir] = (edgep1[tickdir] + ((info['tick']['outward_factor'] * ticksign) * tickdelta))
        (x1, y1, z1) = proj3d.proj_transform(pos[0], pos[1], pos[2], renderer.M)
        pos[tickdir] = (edgep1[tickdir] - ((info['tick']['inward_factor'] * ticksign) * tickdelta))
        (x2, y2, z2) = proj3d.proj_transform(pos[0], pos[1], pos[2], renderer.M)
        default_offset = 8.0
        labeldeltas = (((tick.get_pad() + default_offset) * deltas_per_point) * deltas)
        axmask = [True, True, True]
        axmask[index] = False
        pos[tickdir] = edgep1[tickdir]
        pos = move_from_center(pos, centers, labeldeltas, axmask)
        (lx, ly, lz) = proj3d.proj_transform(pos[0], pos[1], pos[2], renderer.M)
        tick_update_position(tick, (x1, x2), (y1, y2), (lx, ly))
        tick.tick1line.set_linewidth(info['tick']['linewidth'])
        tick.tick1line.set_color(info['tick']['color'])
        tick.set_label1(label)
        tick.set_label2(label)
        tick.draw(renderer)
    renderer.close_group('axis3d')
    self.stale = False
