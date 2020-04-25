#!/usr/bin/env python
# -*- coding: utf-8 -*-


class MyError(Exception):

    def __init__(self, text):
        self.text = text

    def __str__(self):
        if self.text == 'Error_1':
            return 'недостаточно пространства на жестком диске'
        if self.text == 'Error_2':
            return 'файл или каталог отсутствует'
        if self.text == 'Error_3':
            return 'директория для восстановления отсутствует'
        if self.text == 'Error_4':
            return 'доступ к trash.json отсутствует либо ограничен'
