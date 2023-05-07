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


def get_hls_mux_args(enc_params, hls_ingest_url):
    output_config = enc_params['output']
    segment_size = wc_utils.to_int(output_config['segment_size'])
    ffmpeg_out_url = hls_ingest_url
    now = datetime.datetime.now()
    ccgroup_name = 'cc'
    hls_args = ''
    hls_args += ('%s=%s' % ('f', 'hls'))
    var_stream_map = ''
    if (enc_params['output']['create_muxed_av'] == 'on'):
        for n in range(0, len(enc_params['video']['variants'])):
            var_stream_map += (' a\\:%d,v\\:%d' % (n, n))
            if (enc_params['video']['enable_cc'] == 'on'):
                var_stream_map += (',ccgroup\\:%s' % ccgroup_name)
    else:
        for aud_tag in enc_params['audio']:
            aud_id = wc_utils.to_int(enc_params['audio'].keys().index(aud_tag))
            var_stream_map += (' a\\:%d,agroup\\:%s' % (aud_id, aud_tag))
        for n in range(0, len(enc_params['video']['variants'])):
            var_stream_map += (' v\\:%d,agroup\\:%s' % (n, enc_params['video']['variants'][n]['audio_tag']))
            if (enc_params['video']['enable_cc'] == 'on'):
                var_stream_map += (',ccgroup\\:%s' % ccgroup_name)
    if (enc_params['output']['seg_in_subfolder'] == 'on'):
        hls_segment_filename = ('%s/variant_%%v/stream_%02d%02d%02d_%%d.ts' % (ffmpeg_out_url.replace(':', '\\:'), now.hour, now.minute, now.second))
    else:
        hls_segment_filename = ('%s/stream_%02d%02d%02d_%%v_%%d.ts' % (ffmpeg_out_url.replace(':', '\\:'), now.hour, now.minute, now.second))
    hls_flags = 'program_date_time+round_durations'
    hls_ts_options = 'mpegts_pmt_start_pid=480:mpegts_start_pid=481'
    hls_args += (":%s='%s'" % ('var_stream_map', var_stream_map))
    hls_args += (":%s='%s'" % ('hls_segment_filename', hls_segment_filename))
    hls_args += (':%s=%s' % ('hls_time', segment_size))
    hls_args += (':%s=%s' % ('hls_flags', hls_flags))
    hls_args += (":%s='%s'" % ('hls_ts_options', str(hls_ts_options).replace(':', '\\:')))
    hls_args += (':%s=%s' % ('http_persistent', 1))
    hls_args += (':%s=%s' % ('http_user_agent', enc_params['output']['user_agent']))
    hls_args += (':%s=%s' % ('hls_list_size', 6))
    hls_args += (":%s='%s'" % ('cc_stream_map', ('ccgroup\\:%s,instreamid\\:CC1' % ccgroup_name)))
    hls_args += (':%s=%s' % ('master_pl_name', enc_params['output']['hls_master_manifest']))
    hls_args += (':%s=%s' % ('master_pl_publish_rate', 100))
    hls_args += (':%s=%s' % ('timeout', 0.5))
    hls_args += (':%s=%s' % ('method', 'PUT'))
    hls_args += (':%s=%s' % ('ignore_io_errors', '1'))
    if (output_config['enable_abs_seg_path'] == 'on'):
        hls_args += (":%s='%s'" % ('hls_base_url', str(output_config['abs_seg_path_base_url']).replace(':', '\\:')))
    return hls_args
