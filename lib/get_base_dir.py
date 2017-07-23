# coding=utf-8
import os
import sys


def get_base_dir():
    # #
    # cwd = os.getcwd()
    # dir_list = [
    #     os.path.dirname(sys.executable),
    #     os.path.dirname(__file__),
    #     # os.path.dirname在windows cmd下无效
    #     os.path.abspath(__file__).rpartition("\\")[0],
    # ]
    # for dir_name in dir_list:
    #     if cwd in dir_name:
    #         return dir_name
    return os.path.dirname(os.path.abspath(sys.argv[0]))

if __name__ == '__main__':
    print get_base_dir()
