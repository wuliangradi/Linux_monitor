# -*- coding: utf-8 -*-

import psutil


def main():
    mem = psutil.virtual_memory()
    print mem.percent


if __name__ == '__main__':
    main()
