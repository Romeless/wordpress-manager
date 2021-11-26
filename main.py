from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import base64, requests,webbrowser
from wordpress import WordPress, WordPressSignals

class Ui_MainWindow(object):
    USER_DETAIL = {}
    WORDPRESS_TAG_LIST = {}
    WORDPRESS_CAT_LIST = {}
    WORDPRESS_LINK = {}
    WP_URL = ""
    CREDENTIALS = ""
    API_ACCESS = False
    API_APPEND = "/wp-json/wp/v2/"

    def setup(self, MainWindow):
        self.setupUi(MainWindow)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.refreshButton()
        self.retranslateUi(MainWindow)
        
        self.setupSignals()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Blog Manager")
        MainWindow.resize(1000, 800)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.formLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 10, 351, 91))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        
        self.credentials = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.credentials.setContentsMargins(0, 0, 0, 0)
        self.credentials.setObjectName("credentials")
        
        self.label_url = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_url.setObjectName("label_url")
        self.credentials.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_url)
        self.input_url = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.input_url.setObjectName("input_url")
        self.input_url.setText("")
        self.credentials.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.input_url)
        self.input_username = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.input_username.setObjectName("input_username")
        self.input_username.setText("")
        self.credentials.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.input_username)
        self.label_password = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_password.setObjectName("label_password")
        self.credentials.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_password)
        self.input_password = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.input_password.setObjectName("input_password")
        self.input_password.setText("")
        self.credentials.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.input_password)
        self.label_username = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_username.setObjectName("label_username")
        self.credentials.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_username)
        
        self.button_connect = QtWidgets.QPushButton(self.centralwidget)
        self.button_connect.setGeometry(QtCore.QRect(370, 15, 120, 65))
        self.button_connect.setCheckable(True)
        self.button_connect.setObjectName("button_connect")
    
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 120, 480, 450))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        self.layout_search = QtWidgets.QFormLayout()
        self.layout_search.setObjectName("layout_search")

        self.opt_search = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.opt_search.setObjectName("opt_search")
        self.opt_search.addItem("")
        #self.opt_search.addItem("")
        #self.opt_search.addItem("")
        self.layout_search.setWidget(0, QtWidgets.QFormLayout.SpanningRole, self.opt_search)
        self.label_qty = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_qty.setObjectName("label_qty")
        self.layout_search.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_qty)
        self.opt_qty = QtWidgets.QSpinBox(self.verticalLayoutWidget)
        self.opt_qty.setMinimum(1)
        self.opt_qty.setProperty("value", 25)
        self.opt_qty.setObjectName("opt_qty")
        self.layout_search.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.opt_qty)
        self.label_order = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_order.setObjectName("label_order")
        self.layout_search.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_order)
        self.opt_order = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.opt_order.setObjectName("opt_order")
        self.opt_order.addItem("")
        self.opt_order.addItem("")
        self.layout_search.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.opt_order)
        self.verticalLayout.addLayout(self.layout_search)

        self.layout_get = QtWidgets.QFormLayout()
        self.layout_get.setObjectName("layout_get")
        
        self.label_search = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_search.setObjectName("label_search")
        self.layout_get.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_search)
        self.input_search = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.input_search.setText("")
        self.input_search.setObjectName("input_search")
        self.layout_get.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.input_search)
        self.label_categories = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_categories.setObjectName("label_categories")
        self.layout_get.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_categories)
        self.opt_categories = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.opt_categories.setObjectName("opt_categories")
        self.opt_categories.addItem("")
        self.layout_get.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.opt_categories)
        self.label_tags = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_tags.setObjectName("label_tags")
        self.layout_get.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_tags)
        self.opt_tags = QtWidgets.QComboBox()
        self.opt_tags.setObjectName("opt_tags")
        self.opt_tags.addItem("")
        self.layout_get.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.opt_tags)
        self.label_status = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_status.setObjectName("label_status")
        self.layout_get.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_status)
        self.opt_status = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.opt_status.setObjectName("opt_status")
        self.opt_status.addItem("")
        self.opt_status.addItem("")
        self.opt_status.addItem("")
        self.opt_status.addItem("")
        self.opt_status.addItem("")
        self.opt_status.addItem("")
        self.layout_get.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.opt_status)
        self.filterByAuthor = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.filterByAuthor.setObjectName("filterByAuthor")
        self.layout_get.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.filterByAuthor)
        self.button_GET = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.button_GET.setObjectName("button_GET")
        self.layout_get.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.button_GET)
        self.verticalLayout.addLayout(self.layout_get)

        self.layout_update = QtWidgets.QFormLayout()
        self.layout_update.setContentsMargins(0,30,0,0)
        self.layout_update.setObjectName("layout_update")

        self.label_add_categories = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_add_categories.setObjectName("label_add_categories")
        self.layout_update.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_add_categories)
        self.opt_add_categories = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.opt_add_categories.setObjectName("opt_add_categories")
        self.opt_add_categories.addItem("")
        self.layout_update.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.opt_add_categories)
        self.label_delete_categories = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_delete_categories.setObjectName("label_delete_categories")
        self.layout_update.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_delete_categories)
        self.opt_del_categories = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.opt_del_categories.setObjectName("opt_del_categories")
        self.opt_del_categories.addItem("")
        self.opt_del_categories.addItem("")
        self.layout_update.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.opt_del_categories)
        self.label_add_tag = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_add_tag.setObjectName("label_add_tag")
        self.layout_update.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_add_tag)
        self.opt_add_tags = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.opt_add_tags.setObjectName("opt_add_tags")
        self.opt_add_tags.addItem("")
        self.layout_update.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.opt_add_tags)
        self.label_del_tag = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_del_tag.setObjectName("label_del_tag")
        self.layout_update.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_del_tag)
        self.opt_del_tags = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.opt_del_tags.setObjectName("opt_del_tags")
        self.opt_del_tags.addItem("")
        self.opt_del_tags.addItem("")
        self.layout_update.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.opt_del_tags)
        self.label_new_status = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_new_status.setObjectName("label_new_status")
        self.layout_update.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_new_status)
        self.opt_new_status = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.opt_new_status.setObjectName("opt_new_status")
        self.opt_new_status.addItem("")
        self.opt_new_status.addItem("")
        self.opt_new_status.addItem("")
        self.opt_new_status.addItem("")
        self.opt_new_status.addItem("")
        self.opt_new_status.addItem("")
        self.layout_update.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.opt_new_status)
        self.button_UPDATE = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.button_UPDATE.setObjectName("button_UPDATE")
        self.layout_update.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.button_UPDATE)
        self.verticalLayout.addLayout(self.layout_update)
        
        self.main_text_bar = QtWidgets.QTextBrowser(self.centralwidget)
        self.main_text_bar.setGeometry(QtCore.QRect(10, 590, 471, 150))
        self.main_text_bar.setObjectName("main_text_bar")
        self.main_text_bar.setOpenExternalLinks(True)

        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(500, 10, 490, 730))
        self.tableWidget.setLineWidth(1)
        self.tableWidget.setShowGrid(True)
        self.tableWidget.setWordWrap(False)
        self.tableWidget.setCornerButtonEnabled(True)
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 725, 21))
        self.menubar.setObjectName("menubar")
        self.menuAbout = QtWidgets.QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionGithub = QtWidgets.QAction(MainWindow)
        self.actionGithub.setObjectName("actionGithub")
        self.menuAbout.addAction(self.actionGithub)
        self.menubar.addAction(self.menuAbout.menuAction())

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Blog Manager"))
        self.label_url.setText(_translate("MainWindow", "Wordpress URL: "))
        self.label_password.setText(_translate("MainWindow", "Application Password: "))
        self.label_username.setText(_translate("MainWindow", "Wordpress Username: "))
        self.button_connect.setText(_translate("MainWindow", "Connect"))
        self.label_search.setToolTip(_translate("MainWindow", "<html><head/><body><p>Mencari data yang memiliki teks tertentu</p></body></html>"))
        self.label_search.setText(_translate("MainWindow", "Pencarian"))
        self.label_categories.setText(_translate("MainWindow", "Kategori"))
        self.opt_categories.setItemText(0, _translate("MainWindow", "Semua"))
        self.label_tags.setText(_translate("MainWindow", "Tag"))
        self.opt_tags.setItemText(0, _translate("MainWindow", "Semua"))
        self.label_status.setText(_translate("MainWindow", "Status"))
        self.opt_status.setItemText(0, _translate("MainWindow", "Semua"))
        self.opt_status.setItemText(1, _translate("MainWindow", "Publish"))
        self.opt_status.setItemText(2, _translate("MainWindow", "Future"))
        self.opt_status.setItemText(3, _translate("MainWindow", "Draft"))
        self.opt_status.setItemText(4, _translate("MainWindow", "Pending"))
        self.opt_status.setItemText(5, _translate("MainWindow", "Private"))
        self.filterByAuthor.setText(_translate("MainWindow", "Posting Anda?"))
        self.button_GET.setText(_translate("MainWindow", "Tarik Data"))
        self.label_add_categories.setText(_translate("MainWindow", "Tambah Kategori"))
        self.opt_add_categories.setItemText(0, _translate("MainWindow", "None"))
        self.label_delete_categories.setText(_translate("MainWindow", "Hapus Kategori"))
        self.opt_del_categories.setItemText(0, _translate("MainWindow", "None"))
        self.opt_del_categories.setItemText(1, _translate("MainWindow", "Semua"))
        self.label_add_tag.setText(_translate("MainWindow", "Tambah Tag"))
        self.opt_add_tags.setItemText(0, _translate("MainWindow", "None"))
        self.label_del_tag.setText(_translate("MainWindow", "Hapus Tag"))
        self.opt_del_tags.setItemText(0, _translate("MainWindow", "None"))
        self.opt_del_tags.setItemText(1, _translate("MainWindow", "Semua"))
        self.label_new_status.setText(_translate("MainWindow", "Status Baru"))
        self.opt_new_status.setItemText(0, _translate("MainWindow", "Tidak Berubah"))
        self.opt_new_status.setItemText(1, _translate("MainWindow", "Publish"))
        self.opt_new_status.setItemText(2, _translate("MainWindow", "Future"))
        self.opt_new_status.setItemText(3, _translate("MainWindow", "Draft"))
        self.opt_new_status.setItemText(4, _translate("MainWindow", "Pending"))
        self.opt_new_status.setItemText(5, _translate("MainWindow", "Private"))
        self.button_UPDATE.setText(_translate("MainWindow", "Update"))
        self.opt_search.setItemText(0, _translate("MainWindow", "Posts"))
        #self.opt_search.setItemText(1, _translate("MainWindow", "Categories"))
        #self.opt_search.setItemText(2, _translate("MainWindow", "Tags"))
        self.label_qty.setText(_translate("MainWindow", "Jumlah"))
        self.label_order.setText(_translate("MainWindow", "Urutan Listing"))
        self.opt_order.setItemText(0, _translate("MainWindow", "Descending"))
        self.opt_order.setItemText(1, _translate("MainWindow", "Ascending"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "id"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Judul"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Kategori"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Tag"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Status"))
        self.menuAbout.setTitle(_translate("MainWindow", "About"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionGithub.setText(_translate("MainWindow", "Github"))

    def setupWordpress(self):
        self.wordpress = WordPress()
        self.wordpress.signals.print.connect(self.print_output)
        self.wordpress.signals.table.connect(self.add_to_table)

    def openLink(self, item):
        if item.column() == 1:
            webbrowser.open(self.WORDPRESS_LINK[item.row()])

    def clear_output(self):
        self.main_text_bar.clear()

    def print_output(self, str):
        self.main_text_bar.append(str)

    def clear_table(self):
        self.WORDPRESS_LINK = {}
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)

    def add_to_table(self, dict):
        currentRowCount = self.tableWidget.rowCount()

        self.WORDPRESS_LINK[currentRowCount] = dict['link']

        self.tableWidget.insertRow(currentRowCount)
        self.tableWidget.setItem(currentRowCount, 0, QTableWidgetItem(str(dict['id']))) #id
        self.tableWidget.setItem(currentRowCount, 1, QTableWidgetItem(dict['title']['rendered'])) #title
        self.tableWidget.item(currentRowCount, 1).setForeground(QBrush(QColor(6,69,173)))
        self.tableWidget.setItem(currentRowCount, 2, QTableWidgetItem(self.getCategories(dict['categories']))) #categories
        self.tableWidget.setItem(currentRowCount, 3, QTableWidgetItem(self.getTags(dict['tags']))) #tag
        self.tableWidget.setItem(currentRowCount, 4, QTableWidgetItem(dict['status'])) #tag

    def getCategories(self, list_categories):
        result = ""
        for i in range(len(list_categories)):
            result += self.WORDPRESS_CAT_LIST[list_categories[i]] + " "
        return result

    def getTags(self, list_tags):
        result = ""
        for i in range(len(list_tags)):
            result += self.WORDPRESS_TAG_LIST[list_tags[i]] + " "
        return result

    def setupSignals(self):
        self.button_connect.clicked.connect(lambda: self.clicked("CONNECT"))
        self.button_GET.clicked.connect(lambda: self.clicked("GET"))
        self.button_UPDATE.clicked.connect(lambda: self.clicked("PUT"))
        self.tableWidget.itemDoubleClicked.connect(self.openLink)

    def clicked(self, click):
        if click == "CONNECT":
            self.print_output("Connecting...")
            self.connectWordPress()
            pass
        if click == "GET":
            self.print_output("Menarik data...")
            self.initiateGet()
            pass
        if click == "PUT":
            self.print_output("Menyimpan data...")
            self.initiatePut()
            pass

    def connectWordPress(self):
        cred_username = self.input_username.text()
        cred_password = self.input_password.text()

        self.WP_URL = self.input_url.text()
        self.CREDENTIALS = cred_username + ':' + cred_password

        token = base64.b64encode(self.CREDENTIALS.encode())
        header = {'Authorization': 'Basic ' + token.decode('utf-8')}
        get_user_details = self.WP_URL + self.API_APPEND + "users?search=" + cred_username
        get_blog_categories = self.WP_URL + self.API_APPEND + "categories?" + "per_page=99"
        get_blog_tag = self.WP_URL + self.API_APPEND + "tags?" + "per_page=99"

        user_response = requests.get(get_user_details, headers=header)
        self.parseMe(user_response.json()[0])

        self.WORDPRESS_CAT_LIST = {}

        page = 1
        while True:
            cat_response = requests.get(get_blog_categories + "&page=" + str(page), headers=header)
            self.parseCatJSON(cat_response.json())

            page += 1
            if (len(cat_response.json()) != 99):
                break

        self.WORDPRESS_TAG_LIST = {}

        page = 1
        while True:
            tag_response = requests.get(get_blog_tag + "&page=" + str(page), headers=header)
            self.parseTagJSON(tag_response.json())

            page += 1
            if (len(tag_response.json()) != 99):
                break

        self.print_output("Connected to " + self.input_url.text())

        self.API_ACCESS = True
        self.refresh()

    def parseMe(self, user_response):
        self.USER_DETAIL = {}
        self.USER_DETAIL['id'] = user_response['id']
        self.USER_DETAIL['name'] = user_response['name']

    def parseTagJSON(self, tag_response):
        for tag in tag_response:
            self.WORDPRESS_TAG_LIST[tag['id']] = tag['name']

    def parseCatJSON(self, cat_response):
        for tag in cat_response:
            self.WORDPRESS_CAT_LIST[tag['id']] = tag['name']

    def initiateGet(self):
        self.clear_table()
        url = self.WP_URL + self.API_APPEND
        opt = self.getOption()
        get_url = self.buildGetApi()

        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

        self.setupWordpress()
        self.wordpress.setup(   WP_URL = url, 
                                GET_URL = get_url, 
                                OPT = opt,
                                CREDENTIALS = self.CREDENTIALS, 
                                COMMAND = "GET"
                            )
        self.threadpool.start(self.wordpress)
        self.print_output("\n")

    def initiatePut(self):
        self.clear_table()
        url = self.WP_URL + self.API_APPEND
        opt = self.getOption()
        get_url = self.buildGetApi()

        add_cat = add_tag = del_cat = del_tag = False

        if self.opt_add_categories.currentText() != "None":
            add_cat = [k for k, v in self.WORDPRESS_CAT_LIST.items() if v == self.opt_add_categories.currentText()][0]
        
        if self.opt_del_categories.currentText() != "None":
            del_cat = [k for k, v in self.WORDPRESS_CAT_LIST.items() if v == self.opt_del_categories.currentText()][0]

        if self.opt_add_tags.currentText() != "None":
            add_tag = [k for k, v in self.WORDPRESS_TAG_LIST.items() if v == self.opt_add_tags.currentText()][0]

        if self.opt_del_tags.currentText() != "None":
            del_tag = [k for k, v in self.WORDPRESS_TAG_LIST.items() if v == self.opt_del_tags.currentText()][0]

        if self.opt_new_status.currentIndex() == 0:
            new_status = False
        else:
            new_status = self.opt_new_status.currentText().lower()


        print(f"{add_cat}, {del_cat}, {add_tag}, {del_tag}, {new_status}")

        
        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

        self.setupWordpress()

        self.wordpress.setup(
                                WP_URL = url, 
                                GET_URL = get_url, 
                                ADD_CAT = add_cat,
                                DEL_CAT = del_cat,
                                ADD_TAG = add_tag,
                                DEL_TAG = del_tag,
                                OPT = opt,
                                STATUS = new_status,
                                CREDENTIALS = self.CREDENTIALS, 
                                COMMAND = "UPDATE"
                            )
        self.threadpool.start(self.wordpress)

    def getOption(self):
        option = self.opt_search.currentIndex()
        
        if option == 1:
            return "categories"
        elif option == 2:
            return "tags"
        else:
            return "posts"        

    def buildGetApi(self):
        result = "per_page=" + str(self.opt_qty.value())

        cat_string = self.opt_categories.currentText()
        tag_string = self.opt_tags.currentText()

        if self.filterByAuthor.isChecked():
            result += "&author=" + str(self.USER_DETAIL['id'])

        if cat_string != "Semua":
            cat_id = [k for k, v in self.WORDPRESS_CAT_LIST.items() if v == cat_string][0]
            result += "&categories=" + str(cat_id)

        if tag_string != "Semua":
            tag_id = [k for k, v in self.WORDPRESS_TAG_LIST.items() if v == tag_string][0]
            result += "&tags=" + str(tag_id)

        if self.opt_status.currentIndex() != 0:
            result += "&status=" + self.opt_status.currentText().lower()

        if self.input_search.text() != "":
            result += "&search=" + self.input_search.text()

        if self.opt_order.currentIndex() == 1:
            result += "&order=asc" 

        return result

    def refresh(self):
        self.refreshCategoryComboBox()
        self.refreshTagComboBox()
        self.refreshButton()

    def refreshButton(self):
        self.button_GET.setEnabled(self.API_ACCESS)
        self.button_UPDATE.setEnabled(self.API_ACCESS)

    def refreshCategoryComboBox(self):
        categoryList = self.WORDPRESS_CAT_LIST.values()
        categoryList = list(map(str, list(categoryList)))

        self.opt_add_categories.clear()
        self.opt_del_categories.clear()
        self.opt_categories.clear()

        self.opt_categories.addItem("Semua")
        self.opt_add_categories.addItem("None")
        self.opt_del_categories.addItem("None")

        self.opt_add_categories.addItems(categoryList)
        self.opt_del_categories.addItems(categoryList)
        self.opt_categories.addItems(categoryList)

    def refreshTagComboBox(self):
        tagList = self.WORDPRESS_TAG_LIST.values()
        tagList = list(map(str, list(tagList)))

        self.opt_add_tags.clear()
        self.opt_del_tags.clear()
        self.opt_tags.clear()

        self.opt_tags.addItem("Semua")
        self.opt_add_tags.addItem("None")
        self.opt_del_tags.addItem("None")

        self.opt_add_tags.addItems(tagList)
        self.opt_del_tags.addItems(tagList)
        self.opt_tags.addItems(tagList)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setup(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
