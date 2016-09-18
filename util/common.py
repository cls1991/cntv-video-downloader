# coding: utf8

import re
import pycurl
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
