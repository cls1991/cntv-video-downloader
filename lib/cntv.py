# coding: utf8

import json

from util.common import *
from share import const


def get_download_link(url, quality_type=2):
    """
    获取视频链接
    :param p_id:
    :param quality_type:分辨率类型(1: lowChapters 2: chapters 3: chapters2 4: chapters3 5: chapters4)
    :return:
    """
    pid = get_pid_by_url(url)
    if not pid:
        return
    target_url = const.API_URL + '?pid=' + pid
    data = json.loads(get_html(target_url, const.USER_AGENT, const.REFER_URL))
    result = list()
    if data['ack'] == 'no':
        return
    title = data['title'] + '.txt'
    video = data['video']
    valid_chapter_num = video['validChapterNum']
    chapters = [x for x in video.keys() if 'hapters' in x]
    chapters[1:] = sorted(chapters[1:])
    if quality_type < 1:
        quality_type = 1
    if quality_type > valid_chapter_num:
        quality_type = valid_chapter_num
    video_list = video[chapters[quality_type - 1]]
    for x in video_list:
        result.append(x['url'])

    if result:
        save_to_file(result, title)


def get_pid_by_url(url):
    """
    获取pid
    :param url:
    :return:
    """
    if re.match(r'http://tv\.cntv\.cn/video/(\w+)/(\w+)', url):
        pid = match1(url, r'http://tv\.cntv\.cn/video/\w+/(\w+)')
    elif re.match(r'http://\w+\.cntv\.cn/(\w+/\w+/(classpage/video/)?)?\d+/\d+\.shtml', url) or \
            re.match(r'http://\w+.cntv.cn/(\w+/)*VIDE\d+.shtml', url) or \
            re.match(r'http://(\w+).cntv.cn/(\w+)/classpage/video/(\d+)/(\d+).shtml', url) or \
            re.match(r'http://\w+.cctv.com/\d+/\d+/\d+/\w+.shtml', url) or \
            re.match(r'http://\w+.cntv.cn/\d+/\d+/\d+/\w+.shtml', url):
        pid = r1(r'videoCenterId","(\w+)"', get_html(url, const.USER_AGENT, const.REFER_URL))
    elif re.match(r'http://xiyou.cntv.cn/v-[\w-]+\.html', url):
        pid = r1(r'http://xiyou.cntv.cn/v-([\w-]+)\.html', url)
    else:
        pid = None

    return pid
