#!/usr/bin/env python

# -*- coding: utf-8 -*-


import argparse
import datetime
from . import error
from . import size as s
import os
import logging
from . import remove

_trash_dir = f'/home/{os.getlogin()}/.trash_folder'

logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG)
parser = argparse.ArgumentParser()
parser.add_argument("-d", '--delete', help="удаление файла из корзины, производится по id")
parser.add_argument("-r", '--remove', help="перемещение файла в корзину")
parser.add_argument("-q", '--query', action='store_true', help="просмотр информации о корзине")
parser.add_argument("-c", '--clear', action='store_true', help="очистка корзины")
parser.add_argument("-rec", '--recovery', help="восстановление файла из корзины, производиться по id")


def main():
    trash = remove.RemoveToTrash(_trash_dir)
    args = parser.parse_args()
    time_start = datetime.datetime.now()
    if args.remove:
        try:
            trash.remove(args.remove)
            print(f'время переноса файла в корзину: {datetime.datetime.now() - time_start}')
        except error.MyError as e:
            if e.text == 'Error_1':
                print(e)
            if e.text == 'Error_2':
                print(f'{e}: {args.remove}')
            if e.text == 'Error_4':
                print(e)

        except SystemExit:
            print(f'файл trash.json отсутствует в корзине.\nавтоматическое восстановление данных невозможно.\n'
                  f'очистите корзину, либо восстановите данные вручную.')
    if args.recovery:
        try:
            trash.recovery(int(args.recovery))
            print(f'время восстановления файла : {datetime.datetime.now() - time_start}')
        except error.MyError as e:
            if e.text == 'Error_1' or e.text == 'Error_3':
                print(f'{e}\nвведите 1 чтобы продолжить, либо ввод чтобы прекратить операцию')
                if input('>>>  ') == '1':
                    id = input('введите id >>>>>   ')
                    new_link = input('введите новую директорию для восстановления (/home/users) >>>> ')
                    time_start = datetime.datetime.now()
                    trash.recovery(int(id), new_link)
                    print(f'время восстановления файла : {datetime.datetime.now() - time_start}')
            if e.text == 'Error_4':
                print(e)
        except SystemExit:
            print(f'файл trash.json отсутствует в корзине.\nавтоматическое восстановление данных невозможно.\n'
                  f'очистите корзину, либо восстановите данные вручную.')
        except TypeError:
            print(f'файла с id {args.recovery} не существует')
    if args.delete:
        try:
            trash.delete(int(args.delete))
            print(f'время удаления файла : {datetime.datetime.now() - time_start}')
        except SystemExit:
            print(f'файл trash.json отсутствует в корзине.\nавтоматическое восстановление данных невозможно.\n'
                  f'очистите корзину, либо восстановите данные вручную.')

        except TypeError:
            print(f'файла с id {args.delete} не существует')
    if args.clear:
        trash.clear_trash()
        print(f'время очистки корзины : {datetime.datetime.now() - time_start}')
    if args.query:
        try:
            data = trash.parameters()
            if not data:
                print(' корзина пуста')
            print(f'свободного места в корзине: {s.type_size(s.free_disk_size(_trash_dir))} |'
                  f' размер корзины: {s.type_size(s.folder_size(_trash_dir))} |'
                  f' количество файлов в корзине: {len(data)}')
            for el in data:
                print(f'имя: {el["name"]} | размер: {s.type_size(el["size"])} | id: {el["id_trash"]} | дата удаления:'
                      f'{datetime.datetime.fromtimestamp(el["time_stamp"])}')
        except SystemExit:
            print(f'файл trash.json отсутствует в корзине.\nавтоматическое восстановление данных невозможно.\n'
                  f'очистите корзину, либо восстановите данные вручную.')


if __name__ == '__main__':
    main()
