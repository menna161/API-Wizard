import os
import sys
import re
import datetime
import psutil
import math
import subprocess
import time
import urlparse
import wc_utils as wc_utils
import wc_capture as wc_capture


def get_dash_mux_args(enc_params):
    segment_size = wc_utils.to_int(enc_params['output']['segment_size'])
    now = datetime.datetime.now()
    curr_time = ((str(now.hour) + str(now.minute)) + str(now.second))
    if (enc_params['output']['seg_in_subfolder'] == 'on'):
        chunk_name = ('%s/chunk-stream_\\$RepresentationID\\$-\\$Number%%05d\\$.\\$ext\\$' % curr_time)
        init_seg_name = ('%s/init-stream\\$RepresentationID\\$.\\$ext\\$' % curr_time)
    else:
        chunk_name = ('chunk-stream_%s_\\$RepresentationID\\$-\\$Number%%05d\\$.\\$ext\\$' % curr_time)
        init_seg_name = ('init-stream_%s_\\$RepresentationID\\$.\\$ext\\$' % curr_time)
    chunk_name = chunk_name.replace(':', '\\:')
    streaming = 0
    if (enc_params['output']['dash_chunked'] == 'on'):
        streaming = 1
    dash_cmd = ''
    dash_cmd += ('%s=%s' % ('f', 'dash'))
    dash_cmd += (":%s='%s'" % ('media_seg_name', chunk_name))
    dash_cmd += (":%s='%s'" % ('init_seg_name', init_seg_name))
    dash_cmd += (':%s=%s' % ('min_seg_duration', (int(segment_size) * 1000000)))
    dash_cmd += (':%s=%s' % ('window_size', 3))
    if (enc_params['output']['dash_segtimeline'] == 'on'):
        dash_cmd += (':%s=%s' % ('use_timeline', 1))
    else:
        dash_cmd += (':%s=%s' % ('use_timeline', 0))
    dash_cmd += (':%s=%s' % ('http_user_agent', enc_params['output']['user_agent']))
    dash_cmd += (':%s=%s' % ('streaming', streaming))
    dash_cmd += (':%s=%s' % ('index_correction', 1))
    dash_cmd += (':%s=%s' % ('timeout', 0.5))
    dash_cmd += (':%s=%s' % ('dash_segment_type', 'mp4'))
    dash_cmd += (':%s=%s' % ('method', 'PUT'))
    dash_cmd += (':%s=%s' % ('ignore_io_errors', '1'))
    if (enc_params['output']['lhls'] == 'on'):
        dash_cmd += (':%s=%s' % ('lhls', '1'))
    if (segment_size < 8):
        dash_cmd += (':%s=%s' % ('http_persistent', 1))
    if (enc_params['output']['out_type'] == 'CMAF'):
        dash_cmd += (':%s=%s' % ('hls_playlist', 1))
    dash_cmd += ' '
    return dash_cmd
