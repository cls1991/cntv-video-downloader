# coding: utf8

import datetime
import json
import multiprocessing as mul
import subprocess as sub

from util.common import *
from share import const


def get_download_link(url, quality_type=2, get_dlink_only=True, is_merge=False, is_remain=True):
    """
    获取视频链接
    :param url: 源地址
    :param quality_type:分辨率类型(1: lowChapters 2: chapters 3: chapters2 4: chapters3 5: chapters4)
    :param get_dlink_only: 是否仅获取链接
    :param is_merge: 是否合并分段视频
    :param is_remain: 是否保留临时目录
    :return:
    """
    pid = get_pid_by_url(url)
    if not pid:
        return
    target_url = const.API_URL + '?pid=' + pid
    data = json.loads(get_html(target_url, const.USER_AGENT, const.REFER_URL))
    result = list()
    temp_list = list()
    if data['ack'] == 'no':
        return
    title = data['title']
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
        url = x['url']
        if isinstance(url, unicode):
            url = url.encode('utf8')
        result.append(url)
        temp_list.append('file\t' + '\'' + url.split('/')[-1] + '\'')

    if not result:
        return

    save_to_file(result, title + '.txt', const.BASE_VIDEO_DIR)
    save_to_file(temp_list, const.TMP_FILE, const.TMP_DIR)

    if not get_dlink_only:
        ext = r1(r'\.([^.]+)$', result[0])
        assert ext in ('flv', 'mp4')
        download_videos(title + '.%s' % ext, dlinks=result, is_merge=is_merge, is_remain=is_remain)


def wget_video(link_url):
    """
    wget下载视频
    :param link_url:
    :return:
    """
    video_name = link_url.split('/')[-1]
    print(u'*' * 40)
    print(u'正在下载%s' % video_name)
    cmd = '/usr/bin/wget --no-clobber -O ./%s/%s %s' % (const.TMP_DIR, video_name, link_url)
    print('wget cmd: %s' % cmd)
    sub.Popen(cmd, shell=True, stdout=sub.PIPE).stdout.read()


def merge_video(output_file):
    """
    ffmpeg合并视频
    :param output_file:
    :return:
    """
    cmd = '/usr/bin/ffmpeg -f concat -i ./%s/%s -c copy ./%s/"%s"' % (
        const.TMP_DIR, const.TMP_FILE, const.BASE_VIDEO_DIR, output_file)
    print(u'ffmpeg cmd: %s' % cmd)
    sub.Popen(cmd, shell=True, stdout=sub.PIPE).stdout.read()


def download_videos(title, dlinks=None, link_file=None, is_merge=False, is_remain=True):
    """
    下载所有视频
    :param title:
    :param dlinks:
    :param link_file:
    :param is_merge:
    :param is_remain:
    :return:
    """
    video_links = list()
    if dlinks:
        video_links = dlinks
    elif link_file:
        with open(const.BASE_VIDEO_DIR + link_file) as fp:
            for line in fp:
                if line:
                    video_links.append(line)
    if not video_links:
        return
    print(u'*' * 40)
    print(u'开始下载视频')
    print(datetime.datetime.now())
    pool = mul.Pool(const.PROCESS_MAX_NUM)
    pool.map(wget_video, video_links)
    print(u'*' * 40)
    print(datetime.datetime.now())
    print(u'视频全部下载完成')
    if is_merge:
        # 合并分段视频
        print(u'*' * 40)
        print(u'开始合并分段视频')
        merge_video(title)
        print(u'*' * 40)
        print(u'视频合并完成')
        # 删除分段视频
        if not is_remain:
            remove_dir(const.TMP_DIR)


def get_pid_by_url(url):
    """
    获取pid
    :param url:
    :return:
    """
    if re.match(r'http://tv\.cntv\.cn/video/(\w+)/(\w+)', url):
        pid = match1(url, r'http://tv\.cntv\.cn/video/\w+/(\w+)')
    elif re.match(r'http://tv\.cctv\.com/\d+/\d+/\d+/\w+.shtml', url):
        pid = r1(r'var guid = "(\w+)"', get_html(url, const.USER_AGENT, const.REFER_URL))
    elif re.match(r'http://\w+\.cntv\.cn/(\w+/\w+/(classpage/video/)?)?\d+/\d+\.shtml', url) or \
            re.match(r'http://\w+.cntv.cn/(\w+/)*VIDE\d+.shtml', url) or \
            re.match(r'http://(\w+).cntv.cn/(\w+)/classpage/video/(\d+)/(\d+).shtml', url) or \
            re.match(r'http://\w+.cctv.com/\d+/\d+/\d+/\w+.shtml', url) or \
            re.match(r'http://\w+.cntv.cn/\d+/\d+/\d+/\w+.shtml', url):
        page = get_html(url, const.USER_AGENT, const.REFER_URL)
        pid = r1(r'videoCenterId","(\w+)"', page)
        if pid is None:
            guid = re.search(r'guid\s*=\s*"([0-9a-z]+)"', page).group(1)
            pid = guid
    elif re.match(r'http://xiyou.cntv.cn/v-[\w-]+\.html', url):
        pid = r1(r'http://xiyou.cntv.cn/v-([\w-]+)\.html', url)
    else:
        pid = None

    return pid
