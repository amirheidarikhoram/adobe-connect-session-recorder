from argparse import ArgumentParser
from selenium import webdriver
from threading import Thread
from time import sleep
import time
import sys


class Controller:

    isRecording = False

    def __init__(self):
        pass

    def start(self):
        self.isRecording = True

    def stop(self):
        self.isRecording = False


# setup script args
argParser = ArgumentParser(description="Record Adobe Connect Classroom")

argParser.add_argument("link", metavar="LINK",
                       help="Classroom link with session token", action="store")
argParser.add_argument("duration", metavar="DURATION",
                       type=float, help="Classroom duration", action="store")
argParser.add_argument("-o", "--open", dest="openText", action="store", default="Open in browser",
                       help="Open classroom in brower link element text", metavar="LINK_TEXT")
argParser.add_argument("-i", "--iframe-id", dest="iframeId", action="store", default="html-meeting-frame",
                       help="Classroom iframe id", metavar="IFRAME_ID")
argParser.add_argument("-n", "--iframe-name", dest="iframeName", action="store", default="html-meeting-view-frame",
                       help="Classroom iframe id", metavar="IFRAME_NAME")
argParser.add_argument("-p", "--play", dest="playId", action="store", default="play-recording-shim-button",
                       help="Play recorded class button id", metavar="BUTTON_ID")
argParser.add_argument("-k", "--playpause", dest="playPauseId", action="store", default="playPause",
                       help="Play and Pause button id", metavar="BUTTON_ID")
argParser.add_argument("-f", "--forward", dest="forwardId", action="store", default="forward15",
                       help="Forward 15 secs button id", metavar="BUTTON_ID")
argParser.add_argument("-b", "--backward", dest="backwardId", action="store", default="backward15",
                       help="Backward 15 secs button id", metavar="BUTTON_ID")

options = vars(argParser.parse_args())

# setup selenium driver and user agent
driverProfile = webdriver.FirefoxProfile()
driverProfile.set_preference("general.useragent.override",
                             "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0")
driver = webdriver.Firefox(firefox_profile=driverProfile)

# open classroom link
driver.get(options['link'])

# open classroom
openButton = driver.find_element_by_link_text(options['openText'])
openButton.click()

# getting existing frames inside a document to recognize if page is loaded completely - there is always a single frame present and available
frames = driver.find_elements_by_id(options['iframeId'])
while len(frames) == 0:
    sleep(1)
    frames = driver.find_elements_by_id(options['iframeId'])

# switch to iframe
driver.switch_to.frame(options['iframeName'])

# wait for 60 seconds to be sure of complete and proper page load
sleep(60)

# get controll buttons
playButton = driver.find_element_by_id(options['playId'])
playPause = driver.find_element_by_id(options['playPauseId'])
backward15 = driver.find_element_by_id(options['backwardId'])
forward15 = driver.find_element_by_id(options['forwardId'])

# again wait - no purpose, I just decided to wait here with no reason
sleep(60)

# play
playButton.click()

# define a function to handle timing in another frame


def waitAndStopRecording(controller, duration):
    firstTic = time.perf_counter()
    toc = time.perf_counter()
    while toc - firstTic < duration and controller.isRecording:
        toc = time.perf_counter()
    controller.stop()


# create an instance of controller
controller = Controller()

# create thread and start it
timeThread = Thread(target=waitAndStopRecording, kwargs=dict(
    controller=controller, duration=options['duration']))
timeThread.start()

# set recording state
controller.start()
counter = 0
try:
    while controller.isRecording:
        print('\r recording %d' % (counter))
        """ while using glob pattern without formatting the name of frames correctly,
        frames would not be sorted so video was frame jumping compared to original video """
        driver.save_screenshot('shots/%s.png' % ("{:020d}".format(counter)))
        counter += 1
except:
    controller.stop()
    print("An error occured")
    exit(1)
# close driver
driver.close()

# print frames count to standart output
sys.stdout.write(str(counter/options['duration']))

# exit with code 0
exit(0)