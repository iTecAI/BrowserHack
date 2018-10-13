from easygui import *

def run(url):
    query = enterbox('Enter Stackoverflow search query')
    if query != None:
        return 'self.addTab(url="https://www.google.com/search?q=' + query + ' site:stackoverflow.com")'
