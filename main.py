# -*- coding=utf-8 -*-
import argparse
import sys
import traceback
import time
from LgbConfig import ACCOUNT

class Logger(object):
    def __init__(self, filename="Default.log"):
        self.terminal = sys.stdout
        self.log = open(filename, "a")
    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)
    def flush(self):
        pass

def parser_arguments():
    """
    参数解析
    :param argv:
    :return:
    """
    parser = argparse.ArgumentParser(description='链工宝让平凡的人懂得安全生产')
    parser.add_argument('-i', '--interface_call', action='store_true',
                        default=False, help='使用接口POST/GET运行')
    parser.add_argument('-v', '--visualization', action='store_true',
                        default=False, help='使用浏览器可视化运行')
    parser.add_argument('-a', '--adb_ocr', action='store_true',
                        default=False, help='使用ADB工具连接手机运行')
    return parser


if __name__ == '__main__':
    sys.stdout = Logger('info.log')
    print('+++++++++++++++++++++++++++++++++++++++++++++')
    print(time.strftime('%Y-%m-%d %H:%M:%S'))
    parser = parser_arguments()
    args = parser.parse_args(sys.argv[1:])
    if args.interface_call:
        from init.interface_call import InterfaceCall
        app = InterfaceCall()
    elif args.visualization:
        from init.visualization import Visualization
        app = Visualization()
    elif args.adb_ocr:
        from init.adb_ocr import ADBOCR
        app = ADBOCR()
    else:
        parser.print_help()
        sys.exit(0)

    for ac in ACCOUNT:
        user = ac.get("USER")
        passwd = ac.get("PWD")
        print("开始答题: ", user, passwd)
        try:
            app.main(user, passwd)
        except:
            traceback.print_exc()
            print("还继续答题嘛？ q退出")
            if input().upper() == 'Q':
                break
    print("全部用户答题结束！！！")
