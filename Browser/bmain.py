from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import *
import sip
import sys
import os
from functools import partial
import easygui as gui
eb = gui.exceptionbox
import _apps
from getpass import getuser

class Browser(QMainWindow):
    def __init__(self):
        self.url = 'about:blank'
        self.page = QWebEnginePage
        self.stage = 0
        super(Browser, self).__init__()
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.closeTab)
        self.tab1 = QWidget()
        self.tabWebView = []
        self.lNameLine = []
        self.tabs.addTab(self.tab1,"New Tab")
        self.tab1UI(self.tab1)
        self.closeTab(0)
        self.addTab()
        self.stage = 1
        self.setWindowTitle("BrowserHack")
        self.setWindowIcon(QIcon('main_icn.png'))
        self.setCentralWidget(self.tabs)
        self.showMaximized()
        QShortcut(QKeySequence("Ctrl+T"), self, self.addTab)

    def addTab(self, url=None):
        try:
            tab = QWidget()
            self.tabs.addTab(tab,"New Tab")
            self.tab1UI(tab)
            
            index = self.tabs.currentIndex()
            self.tabs.setCurrentIndex( index + 1 )
            if type(url) == type(''):
                self.tabWebView[self.tabs.currentIndex()].load(QUrl(url))
            else:
                self.tabWebView[self.tabs.currentIndex()].load(QUrl('https://www.google.com'))
        except:
            eb()

    def goBack(self):
      index = self.tabs.currentIndex()
      self.tabWebView[index].back()

    def goNext(self):
      index = self.tabs.currentIndex()
      self.tabWebView[index].forward()

    def goRefresh(self):
      index = self.tabs.currentIndex()
      self.tabWebView[index].reload()

    def changePage(self):
        index = self.tabs.currentIndex()
        pageTitle = self.sender().title()[:15]
        self.pg = self.sender().title()
        self.url = str(self.sender().url())[19:].strip("')")
        self.tabs.setTabText(index, pageTitle);        
        self.lNameLine[self.tabs.currentIndex()].setText(self.sender().url().url())

    def load_started(self):
        return
    def makeFav(self):
        try:
            favs = open('favorites.bhk', 'r')
            flist = favs.read().splitlines()
            if self.pg + '~' + self.url in flist and gui.ccbox('Remove this favorite?'):
                favs.close()
                favs = open('favorites.bhk', 'w')
                for i in flist:
                    if i != self.pg + '~' + self.url:
                        print(i, file=favs)
                favs.close()
                    
            else:
                favs.close()
                favs = open('favorites.bhk', 'a')
                print(self.pg + '~' + self.url, file=favs)
                favs.close()
        except:
            eb()
    def retFav(self):
        favorites = []
        try:
            ffavs = open('favorites.bhk', 'r')
            favs = ffavs.read().splitlines()
            ffavs.close()
            favdict = {}
            for i in favs:
                favdict[i.split('~')[0]] = i.split('~')[1]
            fav_to_open = gui.choicebox('Select Favorite', choices=favdict.keys())
            if type(fav_to_open) == type(''):
                try:
                    self.addTab(url=favdict[fav_to_open])
                except:
                    pass
        except FileNotFoundError:
            gui.msgbox('You have no favorites. Oh well.')
    def onDownloadRequested(self, d):
        try:
            dpath = open('dpath.bhk', 'r')
            path = dpath.read()
            dpath.close()
        except FileNotFoundError:
            dpath = open('dpath.bhk', 'w')
            path = gui.diropenbox('Select default download directory')
            if path != None:
                dpath.write(path)
            dpath.close()
        print(d.url().url())
        try:
            if '\\' in d.path():
                prevpath = d.path().split('\\')
            else:
                prevpath = d.path().split('/')
        except:
            eb()
        try:
            d.setPath(path + '\\' + prevpath[len(prevpath) - 1])
            d.accept()
            print(d.path())
        except:
            eb()
        
    def tab1UI(self,tabName):
        webView = QWebEngineView()

        backButton = QPushButton("")
        backIcon = QIcon()
        backIcon.addPixmap(QPixmap("back.png"))
        backButton.setIcon(backIcon)
        backButton.setFlat(True)
        backButton.setToolTip('Go Back')

        favButton = QPushButton("")
        favIcon = QIcon()
        favIcon.addPixmap(QPixmap("fav.png"))
        favButton.setIcon(favIcon)
        favButton.setFlat(True)
        favButton.clicked.connect(self.makeFav)
        favButton.setToolTip('Add or remove this page from your Favorites')

        rfavButton = QPushButton("")
        rfavIcon = QIcon()
        rfavIcon.addPixmap(QPixmap("fav-ret.png"))
        rfavButton.setIcon(rfavIcon)
        rfavButton.setFlat(True)
        rfavButton.clicked.connect(self.retFav)
        rfavButton.setToolTip('Open or view your Favorites')
        
        nextButton = QPushButton("")
        nextIcon = QIcon()
        nextIcon.addPixmap(QPixmap("next.png"))
        nextButton.setIcon(nextIcon)
        nextButton.setFlat(True)
        nextButton.setToolTip('Go Forward')

        refreshButton = QPushButton("")
        refreshIcon = QIcon()
        refreshIcon.addPixmap(QPixmap("ref.png"))
        refreshButton.setIcon(refreshIcon)
        refreshButton.setFlat(True)
        refreshButton.setToolTip('Refresh')

        backButton.clicked.connect(self.goBack)
        nextButton.clicked.connect(self.goNext)
        refreshButton.clicked.connect(self.goRefresh)

        self.ntButton = QPushButton("")
        ntIcon = QIcon()
        ntIcon.addPixmap(QPixmap("add-tab.png"))
        self.ntButton.setIcon(ntIcon)
        self.ntButton.setFlat(True)
        #self.destroyTabButton = QPushButton("-")
        self.tabWidget = QTabWidget()
        self.ntButton.clicked.connect(self.addTab)
        self.ntButton.setToolTip('New Tab')

        navigationFrame = QWidget()
        navigationFrame.setMaximumHeight(32)
        navigationGrid = QGridLayout(navigationFrame)
        navigationGrid.setSpacing(0)
        navigationGrid.setContentsMargins(0,0,0,0)
        
        #load apps
        apps = os.listdir('_apps')
        self.verified_apps = []
        for i in apps:
            try:
                exec('import _apps.' + i + '.main')
                try:
                    x = open('_apps/' + i + '/icon.png', 'r')
                    x.close()
                    self.verified_apps.append({'app':i, 'icn':'_apps/' + i + '/icon.png'})
                    
                except FileNotFoundError:
                    pass
            except ImportError:
                pass
        buttons = []
        pos = 1
        for i in self.verified_apps:
            button = QPushButton("")
            buttonIcon = QIcon()
            buttonIcon.addPixmap(QPixmap(i['icn']))
            button.setIcon(buttonIcon)
            button.setFlat(True)
            button.setToolTip(i['app'])
            buttons.append(button)
            buttons[len(buttons) - 1].clicked.connect(partial(self.runApp, i['app']))
            navigationGrid.addWidget(buttons[len(buttons) - 1],1,pos)
            pos += 1
    
        #Finish loading apps
        
        nameLine = QLineEdit()
        nameLine.returnPressed.connect(self.requestUri)

        tabGrid = QGridLayout()

        tabGrid.setContentsMargins(0,0,0,0)

        
        navigationGrid.addWidget(backButton,0,1)
        navigationGrid.addWidget(nextButton,0,2)
        navigationGrid.addWidget(refreshButton,0,3)
        navigationGrid.addWidget(nameLine,0,6)
        navigationGrid.addWidget(favButton,0,7)
        navigationGrid.addWidget(rfavButton,0,8)
        navigationGrid.addWidget(self.ntButton,0,5)

        self.page().profile().downloadRequested.connect(self.onDownloadRequested)
        
        tabGrid.addWidget(navigationFrame)

        webView = QWebEngineView()
        htmlhead = "<head><style>body{ background-color: #fff; }</style></head><body></body>";
        webView.setHtml(htmlhead)

        #webView.loadProgress.connect(self.loading)
        webView.loadFinished.connect(self.changePage)

        frame = QFrame()
        frame.setFrameStyle(QFrame.Panel)

        gridLayout = QGridLayout(frame);
        #gridLayout.setObjectName(QStringLiteral("gridLayout"));
        gridLayout.setContentsMargins(0, 0, 0, 0);
        gridLayout.addWidget(webView, 0, 0, 1, 1);
        frame.setLayout(gridLayout)

        self.tabWebView.append(webView)
        self.tabWidget.setCurrentWidget(webView)        
        self.lNameLine.append(nameLine)
        tabGrid.addWidget(frame)
        tabName.setLayout(tabGrid)

    def runApp(self, _app_):
        try:
            exec('_apps.' + _app_ + '.main.run("' + self.url + '")')
        except:
            eb()
        
    def tab2UI(self):
        vbox = QVBoxLayout()
        tbl1 = QTableWidget()
        tbl1.setRowCount(5)
        tbl1.setColumnCount(5)
        vbox.addWidget(tbl1)
        tbl1.setItem(0, 0, QTableWidgetItem("1")) # row, col
        self.tab2.setLayout(vbox)

    def requestUri(self):
        if self.tabs.currentIndex() != -1:

            urlText = self.lNameLine[self.tabs.currentIndex()].text()

            ########################## 
            # no protocol?    
            if 'http' not in urlText:
                url = QUrl('http://google.com/search?q=' + urlText)
                urlt = 'http://google.com/search?q=' + urlText
            else:
                url = QUrl(self.lNameLine[self.tabs.currentIndex()].text())
                urlt = self.lNameLine[self.tabs.currentIndex()].text()

            #print(self.tabs.currentIndex())
            if url.isValid():
                self.tabWebView[self.tabs.currentIndex()].load(url)
            else:
                print("Url not valid")
        else:
            print("No tabs open, open one first.")

    def closeTab(self,tabId):
        #print(tabId)
        del self.lNameLine[tabId]
        del self.tabWebView[tabId]
        self.tabs.removeTab(tabId)
        if len(self.tabWebView) == 0 and self.stage == 1:
            self.addTab()


def main():
    app = QApplication(sys.argv)
    ex = Browser()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
