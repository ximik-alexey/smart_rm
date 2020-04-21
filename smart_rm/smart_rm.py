#!/usr/bin/env python
# -*- coding: utf-8 -*-


import argparse
import datetime
import os
import logging
import sys

import remove

logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG)

parser = argparse.ArgumentParser()
parser.add_argument("-d", '--delete', help="удаление файла из корзины, производится по id")
parser.add_argument("-r", '--remove', help="перемещение файла в корзину")
parser.add_argument("-q", '--query', action='store_true', help="просмотр информации о корзине")
parser.add_argument("-c", '--clear', action='store_true', help="очистка корзины")
parser.add_argument("-rec", '--recovery', help="восстановление файла из корзины, производиться по id")

_trash_dir = f'/home/{os.getlogin()}/.trash_folder'

if __name__ == '__main__':
    trash = remove.RemoveToTrash(_trash_dir)
    args = parser.parse_args()
    time_start = datetime.datetime.now()
    if args.remove:
        try:
            if trash.remove(args.remove) != 'error 3':
                print(f'время переноса файла в корзину: {datetime.datetime.now() - time_start}')
            else:
                print(f' файл или каталог отсутствует : {args.remove}')
        except SystemExit:
            print(f'файл trash.json отсутствует в корзине.\nавтоматическое восстановление данных невозможно.\n'
                  f'очистите корзину, либо восстановите данные вручную.')
    if args.recovery:
        try:
            trash.recovery(int(args.recovery))
            print(f'время восстановления файла : {datetime.datetime.now() - time_start}')
        except SystemExit:
            print(f'файл trash.json отсутствует в корзине.\nавтоматическое восстановление данных невозможно.\n'
                  f'очистите корзину, либо восстановите данные вручную.')
        except:
            print(f'файла с id {args.recovery} не существует')
    if args.delete:
        try:
            trash.delete(int(args.delete))
            print(f'время удаления файла : {datetime.datetime.now() - time_start}')
        except SystemExit:
            print(f'файл trash.json отсутствует в корзине.\nавтоматическое восстановление данных невозможно.\n'
                  f'очистите корзину, либо восстановите данные вручную.')
        except:
            logging.warning(f'нет файла или каталога в корзине')
    if args.clear:
        trash.clear_trash()
        print(f'время очистки корзины : {datetime.datetime.now() - time_start}')
    if args.query:
        try:
            data = trash.parameters()
            if not data:
                print(' корзина пуста')
            for el in data:
                print(f'имя файла: {el["name"]} | размер файла: {el["size"]} | id : {el["id_trash"]} | дата удаления :'
                      f'{datetime.datetime.fromtimestamp(el["time_stamp"])}')
        except SystemExit:
            print(f'файл trash.json отсутствует в корзине.\nавтоматическое восстановление данных невозможно.\n'
                  f'очистите корзину, либо восстановите данные вручную.')


