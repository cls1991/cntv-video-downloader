# coding: utf8

import os
# 切换工作目录到项目根目录
project = os.path.split(os.path.realpath(__file__))[0]
os.chdir(project)

from lib.cntv import get_download_link


if __name__ == '__main__':
    # 测试用例
    if __name__ == '__main__':
        get_download_link('http://2016.cctv.com/2016/08/22/VIDEdMJX5lDjx1mLeLBLQtf2160822.shtml', quality_type=5)
