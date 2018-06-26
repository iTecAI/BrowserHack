import easygui, subprocess

def run(url):
    try:
        cfg = open('_apps\pipinstall\cfg.txt', 'r')
        path = cfg.read()
        cfg.close()
    except:
        pipath = easygui.enterbox('Enter the path to your Scripts directory')
        cfg = open('_apps\pipinstall\cfg.txt', 'w')
        cfg.write(pipath)
        cfg.close()
        cfg = open('_apps\pipinstall\cfg.txt', 'r')
        path = cfg.read()
        cfg.close()
    
    if url.startswith('https://pypi.org/project/') and easygui.ccbox('Install ' + url[25:len(url) - 1] + '?'):
        try:
            subprocess.call([path + '\\pip.exe', 'install', url[25:len(url) - 1]])
        except:
            easygui.exceptionbox()
    else:
        easygui.msgbox('You are not on pypi. Go to a pypi project main page and try again.')
