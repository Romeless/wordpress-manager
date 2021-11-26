from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from pathlib import Path
import requests, os, traceback, sys, base64

class WordPressSignals(QObject):
    error = pyqtSignal(tuple)
    progress = pyqtSignal(int)
    print = pyqtSignal(str)
    table = pyqtSignal(dict)
    total_image = pyqtSignal(int)

class WordPress(QRunnable):

    def __init__(self, **kwargs):
        super(WordPress, self).__init__()
        self.signals = WordPressSignals()

        self.WP_URL = ""
        self.GET_URL = ""
        self.OPT = "posts"
        self.ADD_CAT = False
        self.DEL_CAT = False
        self.ADD_TAG = False
        self.DEL_TAG = False
        self.STATUS = False
        self.CREDENTIALS = ""
        self.COMMAND = "GET"

        if 'WP_URL' in kwargs:
            self.WP_URL = kwargs['WP_URL']
        if 'GET_URL' in kwargs:
            self.GET_URL = kwargs['GET_URL']
        if 'OPT' in kwargs:
            self.OPT = kwargs['OPT']
        if 'ADD_CAT' in kwargs:
            self.ADD_CAT = kwargs['ADD_CAT']
        if 'DEL_CAT' in kwargs:
            self.DEL_CAT = kwargs['DEL_CAT']
        if 'ADD_TAG' in kwargs:
            self.ADD_TAG = kwargs['ADD_TAG']
        if 'DEL_TAG' in kwargs:
            self.DEL_TAG = kwargs['DEL_TAG']
        if 'STATUS' in kwargs:
            self.STATUS = kwargs['STATUS']
        if 'CREDENTIALS' in kwargs:
            self.CREDENTIALS = kwargs['CREDENTIALS']
        if 'COMMAND' in kwargs:
            self.COMMAND = kwargs['COMMAND']

    def setup(self, **kwargs):
        if 'WP_URL' in kwargs:
            self.WP_URL = kwargs['WP_URL']
        if 'GET_URL' in kwargs:
            self.GET_URL = kwargs['GET_URL']
        if 'OPT' in kwargs:
            self.OPT = kwargs['OPT']
        else:
            self.OPT = "posts"
        if 'ADD_CAT' in kwargs:
            self.ADD_CAT = kwargs['ADD_CAT']
        if 'DEL_CAT' in kwargs:
            self.DEL_CAT = kwargs['DEL_CAT']
        if 'ADD_TAG' in kwargs:
            self.ADD_TAG = kwargs['ADD_TAG']
        if 'DEL_TAG' in kwargs:
            self.DEL_TAG = kwargs['DEL_TAG']
        if 'STATUS' in kwargs:
            self.STATUS = kwargs['STATUS']
        if 'CREDENTIALS' in kwargs:
            self.CREDENTIALS = kwargs['CREDENTIALS']
        if 'COMMAND' in kwargs:
            self.COMMAND = kwargs['COMMAND']
        else:
            self.COMMAND = 'GET'

    @pyqtSlot()
    def run(self):
        try:
            token = base64.b64encode(self.CREDENTIALS.encode())
            header = {'Authorization': 'Basic ' + token.decode('utf-8')}
            url = self.WP_URL + self.OPT + "?" + self.GET_URL

            response = requests.get(url, headers=header)    
            

            if self.COMMAND == 'GET':
                self.signals.print.emit(f"GET {url}")

                for data in response.json():
                    self.signals.table.emit(data)
            elif self.COMMAND == 'UPDATE':
                for data in response.json():
                    emit_print = f"#{data['id']} <a href=\"{data['link']}\">'{data['title']['rendered']}</a>'"
                    
                    categories = data['categories']
                    tags = data['tags']

                    if self.ADD_CAT:
                        emit_print += "\nAdded Category: " + str(self.ADD_CAT)
                        categories.append(self.ADD_CAT)

                    if self.ADD_TAG:
                        emit_print += "\nAdded Tag: " + str(self.ADD_TAG)
                        tags.append(self.ADD_TAG)

                    if self.DEL_CAT:
                        emit_print += "\nRemoved Category: " + str(self.DEL_CAT)
                        categories = [cat for cat in categories if cat != self.DEL_CAT]

                    if self.DEL_TAG:
                        emit_print += "\nRemoved Tag: " + str(self.DEL_TAG)
                        tags = [tag for tag in tags if tag != self.DEL_TAG]

                    put = {
                            'categories' : categories,
                            'tags' : tags,
                        }

                    if self.STATUS:
                        emit_print += "\nNew Status: " + self.STATUS
                        put['status'] = self.STATUS
                    
                    print(self.WP_URL + self.OPT + "/" + str(data['id']))
                    print(put)

                    
                    put_url = self.WP_URL + self.OPT + "/" + str(data['id'])
                    
                    put_response = requests.put(put_url, headers=header, json=put)

                    self.signals.print.emit(f"PUT {put_url}")
                    self.signals.table.emit(put_response.json())
            
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))