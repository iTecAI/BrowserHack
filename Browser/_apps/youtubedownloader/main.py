import pafy
from easygui import ccbox, diropenbox

def run(url):
    if url.startswith('https://www.youtube.com/watch'):
        vid = pafy.new(url)
        if ccbox('Downloading ' + vid.title + '. Confirm?'):
            best = vid.getbest(preftype='mp4')
            path = diropenbox('Select save directory')
            best.download(filepath=path, quiet=True)
