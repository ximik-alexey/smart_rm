#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os


def type_size(num):
    if 1024 > num / 1024 >= 1:
        return f'{num / 1024} KB'
    elif 1024 > num / 1024 ** 2 >= 1:
        return f'{round(num / 1024 ** 2, 1)} MB'
    elif 1024 > num / 1024 ** 3 >= 1:
        return f'{round(num / 1024 ** 3, 1)} GB'
    else:
        return f'{num} B'


def file_size(path):
    return os.path.getsize(path)


def folder_size(path):
    total = 0
    for entry in os.scandir(path):
        if entry.is_file():
            total += entry.stat().st_size
        elif entry.is_dir():
            total += folder_size(entry.path)
    return total


def free_disk_size(path):
    s_2 = os.statvfs(path)
    return (s_2.f_bsize * s_2.f_bavail) - s_2.f_frsize


def sise(path):
    if os.path.isfile(path):
        return file_size(path)
    elif os.path.isdir(path):
        return folder_size(path)
