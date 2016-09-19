# coding: utf8

import os
import re
import pycurl
import shutil
from StringIO import StringIO


def match1(text, *patterns):
    """Scans through a string for substrings matched some patterns (first-subgroups only).
    Args:
        text: A string to be scanned.
        patterns: Arbitrary number of regex patterns.
    Returns:
        When only one pattern is given, returns a string (None if no match found).
        When more than one pattern are given, returns a list of strings ([] if no match found).
    """

    if len(patterns) == 1:
        pattern = patterns[0]
        match = re.search(pattern, text)
        if match:
            return match.group(1)
        else:
            return None
    else:
        ret = []
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                ret.append(match.group(1))
        return ret


# DEPRECATED in favor of match1()
def r1(pattern, text):
    m = re.search(pattern, text)
    if m:
        return m.group(1)


def get_html(url, user_agent, refer_url):
    """
    curl html
    :param url:
    :param user_agent:
    :param refer_url:
    :return:
    """
    curl = pycurl.Curl()
    curl.setopt(pycurl.USERAGENT, user_agent)
    curl.setopt(pycurl.REFERER, refer_url)

    buffers = StringIO()
    curl.setopt(pycurl.URL, url)
    curl.setopt(pycurl.WRITEDATA, buffers)
    curl.perform()
    body = buffers.getvalue()
    buffers.close()
    curl.close()

    return body


def save_to_file(d_links, file_name, base_dir):
    """
    存储下载链接
    :param d_links:
    :param file_name:
    :param base_dir:
    :return
    """
    try:
        if not d_links:
            return
        if not os.path.exists(base_dir):
            os.mkdir(base_dir)
        file_object = open('./%s/%s' % (base_dir, file_name), 'w')

        for item in d_links:
            file_object.write(item)
            file_object.write('\n')
        file_object.close()
    except IOError:
        print('file not exist!')


def remove_dir(dir_name):
    """
    删除目录树
    :param dir_name:
    :return:
    """
    try:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
    except IOError:
        print('dir not exist!')
