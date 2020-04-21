#!/usr/bin/env python
# -*- coding: utf-8 -*-


import logging
import datetime
import os
import tarfile
import json


class RemoveToTrash:
    def __init__(self, trash_dir):
        self.data = []
        self.trash_dir = trash_dir

    def _load_data(self):
        logging.debug('start _load_data')
        if not os.path.isdir(self.trash_dir):
            os.mkdir(self.trash_dir)

        for i in os.listdir(self.trash_dir):
            if i == 'trash.json':
                try:
                    with open(self.trash_dir + '/trash.json', 'r') as file:
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
            with open(self.trash_dir + '/trash.json', 'w') as file:
                json.dump(self.data, file)
        except:
            logging.error('нет доступа к trash.json')
        logging.debug('_save_data completed')

    def _file_address(self, link):
        folder = []
        for i in os.walk(link):
            folder.append(i)
        files = []
        folders = []
        address = []
        for address, dirs, files in folder:
            for file in files:
                files.append(f'{address}/{file}')
                address.append(f'{address}')
        for address, dirs, files in folder:
            for dirs in folder:
                folder.append(f'{address}/{dirs}')
        return files, reversed(folders), address

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
        link_archive = f'{self.trash_dir}/{name_archive}'
        with tarfile.open(f'{self.trash_dir}/{name_archive}', 'w:gz') as archive:
            archive.add(name)
        if os.path.isdir(link):
            for file, directories in self._file_address(link):
                os.remove(file)
                os.rmdir(directories)
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
        with tarfile.open(f'{self.trash_dir}/{name_archive}', 'r:gz') as archive:
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
        # link = self.data[index_file]['link']
        # name_archive = self.data[index_file]['name_archive']
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
        for file in os.listdir(self.trash_dir):
            os.remove(file)
            logging.debug(f'remove :{file}')
        os.rmdir(self.trash_dir)
        logging.debug('trash clear completed')
