__author__ = 'LPC'

from fbin import Generator
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import os


exportDir = 'pics'
templateFile = 'template.html'
path = '.'
filename = "Hinweis.pps"
outFileName = 'index.html'
remotePicturePath = "www"

#Connection:
host = "informatik.fh-brandenburg.de"
user = "fbinews"
key = os.path.abspath('pass/id_rsa.sdx')


class MyHandler(FileSystemEventHandler):
    def __init__(self, filename):
        self.filename = filename
        print("Listening for " + filename)

    def on_modified(self, event):
        #print (event)
        if '\\' + self.filename in event.src_path:
            print(filename + " changed. Working...")
            time.sleep(4)
            gen = Generator(filename, templateFile, exportDir, outFileName, remotePicturePath)
            print("Picture upload")
            gen.picture_generator(host, user, key)
            print ("Pictures uploaded")
            gen.site_generator(host, user, key)
            print('Other files updated')
            gen.close_presentation()


if __name__ == "__main__":



    event_handler = MyHandler(filename)
    observer = Observer()
    observer.schedule(event_handler, path)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()