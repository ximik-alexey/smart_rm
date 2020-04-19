#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import datetime
import shutil
import logging
import os
import tarfile
import json

logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG)

parser = argparse.ArgumentParser()
parser.add_argument("-d", '--delete', help="удаление файла из корзины производится по id")
parser.add_argument("-r", '--remove', help="перемещение файла в корзину")
parser.add_argument("-q", '--query', action='store_true', help="просмотр информации о корзине")
parser.add_argument("-c", '--clear', action='store_true', help="очистка корзины")
parser.add_argument("-rec", '--recovery', help="восстановление файла из корзины, производиться по id")

_user = os.getlogin()
_trash_dir = os.path.expanduser('/home/' + _user + '/.trash_folder')



class Rm:
    def __init__(self):
        self.data = []

    def _load_data(self):
        logging.debug('start _load_data')
        if not os.path.isdir(_trash_dir):
            os.mkdir(_trash_dir)

        for i in os.listdir(_trash_dir):
            if i == 'trash.json':
                try:
                    with open(_trash_dir + '/trash.json', 'r') as file:
                        self.data = json.load(file)
                        break
                except:
                    logging.error('нет доступа к trash.json')
        else:
            self.data = []
        logging.debug('_load_data completed')

    def _save_data(self):
        logging.debug('start _save_data')
        try:
            with open(_trash_dir + '/trash.json', 'w') as file:
                json.dump(self.data, file)
        except:
            logging.error('нет доступа к trash.json')
        logging.debug('_save_data completed')

    def remove(self, link):
        logging.debug('start remove')
        self._load_data()
        try:
            id_trash = self.data[-1]['id_trash'] + 1
        except:
            id_trash = 0
        path = os.path.split(link)
        link_to_file = path[0]
        link = os.path.abspath(link)
        time_stamp = datetime.datetime.timestamp(datetime.datetime.now())
        time = str(int(time_stamp))
        name = os.path.basename(link)
        name_archive = f'{name}_{time}.tar.gz'
        link_archive = f'{_trash_dir}/{name_archive}'
        with tarfile.open(f'{_trash_dir}/{name_archive}', 'w:gz') as archive:
            archive.add(name)
        if os.path.isdir(link):
            shutil.rmtree(link, ignore_errors=False)
        else:
            os.remove(link)
        size = os.path.getsize(link_archive)
        self.data.append({'name': name, 'size': size, 'link_to_file': link_to_file,
                          'time_stamp': time_stamp, 'link': link,
                          'name_archive': name_archive,
                          'link_archive': link_archive,
                          'id_trash': id_trash})
        self._save_data()
        logging.debug('remove completed')

    def recovery(self, id_trash):
        logging.debug('start recovery')
        self._load_data()
        index_file = None
        if self.data:
            for index, el in enumerate(self.data):
                if el['id_trash'] == id_trash:
                    index_file = index
                    break
        link_archive = self.data[index_file]['link_archive']
        link = self.data[index_file]['link_to_file']
        name_archive = self.data[index_file]['name_archive']
        with tarfile.open(f'{_trash_dir}/{name_archive}', 'r:gz') as archive:
            archive.extractall(link)
        os.remove(link_archive)
        del self.data[index_file]
        if self.data:
            for index, el in enumerate(self.data):
                self.data[index]['id_trash'] = index
        self._save_data()
        logging.debug('recovery completed')

    def delete(self, id_trash):
        logging.debug('start delete')
        self._load_data()
        index_file = None
        if self.data:
            for index, el in enumerate(self.data):
                if el['id_trash'] == id_trash:
                    index_file = index
                    break
        link_archive = self.data[index_file]['link_archive']
        link = self.data[index_file]['link']
        name_archive = self.data[index_file]['name_archive']
        os.remove(link_archive)
        del self.data[index_file]
        if self.data:
            for index, el in enumerate(self.data):
                self.data[index]['id_trash'] = index
        self._save_data()
        logging.debug('delete completed')

    def parameters(self):
        logging.debug('load parameters')
        self._load_data()
        logging.debug('load parameters completed')
        return self.data

    def clear_trash(self):
        logging.debug('start clear_trash')
        if os.listdir(_trash_dir):
            shutil.rmtree(_trash_dir, ignore_errors=False)
        logging.debug('trash clear completed')


if __name__ == '__main__':
    trash = Rm()
    args = parser.parse_args()
    time_start = datetime.datetime.now()
    if args.remove:
        try:
            trash.remove(args.remove)
            print(f'время переноса файла в корзину: {datetime.datetime.now() - time_start}')
        except:
            logging.warning(f'нет файла или каталога  {args.remove}')

    if args.recovery:
        try:
            trash.recovery(int(args.recovery))
            print(f'время востановления файла : {datetime.datetime.now() - time_start}')
        except:
            logging.warning('корзина пуста')
    if args.delete:
        try:
            trash.delete(int(args.delete))
            print(f'время удаления файла : {datetime.datetime.now() - time_start}')
        except:
            logging.warning(f'нет файла или каталога в корзине')
    if args.clear:
        trash.clear_trash()
        print(f'время очистки корзины : {datetime.datetime.now() - time_start}')
    if args.query:
        data = trash.parameters()
        if not data:
            print(' корзина пуста')
        for el in data:
            print(f'имя файла: {el["name"]} | размер файла: {el["size"]} | id : {el["id_trash"]} | дата удаления :'
                  f'{datetime.datetime.fromtimestamp(el["time_stamp"])}')
