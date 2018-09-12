from parameterized import parameterized
from subprocess import PIPE, Popen
import random
from functools import wraps
import utils.common.log as log
from PIL import ImageGrab
from config.globalconfig import BASE_PATH,STATIC_PATH,REPORT_PATH
import os.path
from utils.common.file_reader import Config
from utils.common.mail import Email

#import traceback

filename= os.path.basename(os.path.realpath(__file__)).split('.')[0]
logger = log.Logger(logname=filename).get_logger()
def custom_name_func(testcase_func, param_num, param):
    return "%s_%s" %(
        testcase_func.__name__,
        parameterized.to_safe_name("_".join(str(x) for x in param.args[0:1])),
    )

def getVideoPngInfor(videoPath):
    #exampe:videoinfor = getVideoPngInfor(r'C:\Users\wu\Desktop\work8-14\15030010001_chuxi_08_17_2018__10_40_54.mp4')
    #print(videoinfor)
   # output:{'Videoframenum': '11', 'Audioframenum': '17', 'Videofps': '29.97', 'Videowidth': '960', 'Videoheight': '480',
    # 'Videocodec': 'H264', 'Videoprofile': '100', 'Videolevel': '42', 'VideopixFmt': '0', 'Videobitrate': '4M', 'Videoaudio': 'true'}
    #"""
    if not os.path.exists(videoPath):
        logger.error('Video not exsist!')
        return None
    videoInforfilePath = os.path.dirname(videoPath)
    videoInforfilePath = os.path.join(videoInforfilePath,'videoinfor.txt')
    cmd = STATIC_PATH +'\VideoInfo.exe "{0}"'.format(videoPath)
    current_process = Popen(cmd, shell=True,stdout=PIPE)
    lines = []
    videoInfor={}
    while current_process.poll() == None:
        line = current_process.stdout.readline().decode()
        lines.append(line)
    current_process.communicate()
    current_process.wait()
    with open(videoInforfilePath ,'w+') as file:
        for line in lines:
                file.write(line)
    for line in lines[1:]:
        if line != '':
            line = ''.join(line.split())
            split_list = line.split(':')
            videoInfor[split_list[0]]=split_list[1]
    return videoInfor

def get_lately_video(videoPath):
    filelist = os.listdir(videoPath)
    videolist = []
    if not filelist:
        return None
    else:
        for file in filelist:
            if file.endswith(".mp4"):
                videolist.append(file)
    videolist = sorted(videolist, key=lambda x: os.path.getmtime(os.path.join(videoPath, x)))
    latelyVideo = os.path.join(videoPath,videolist[-1])
    return latelyVideo

def get_err_image(function):
    @wraps(function)
    def getErrImage(self,*args, **kwargs):
        try:
            result = function(self,*args, **kwargs)
        except Exception as e:
            picture_num = str(random.randint(10000000, 99999999))
            print(args[0])
            print(str(args[0]),type(function.__class__))
            path = os.path.join(
                BASE_PATH,
                "report",
                "tempimg",
                function.__module__
                + "."
                + self.__class__.__name__
                + "."
                + function.__name__
                + "_"
                + str(args[0])
                + "_"
                + picture_num
                + ".png",
            )
            pic = ImageGrab.grab()
            pic.save(path)
            logger.info("%s not pass！" % (function.__name__))
            raise e
        else:
            logger.info ("Script %s running normally！" %(function.__name__))
            return result
    return getErrImage

def screenshot_img(imgPath):
    if not os.path.exists(imgPath):
        os.makedirs(imgPath)
    picture_num = str(random.randint(10000000, 99999999))
    img = os.path.join(imgPath,picture_num+'.png')
    pic = ImageGrab.grab()
    pic.save(img)

def list_only_files_recursive(src_dir):
  fileslist = []
  for (root, dirs, files) in os.walk(src_dir):
    for fn in files:
        if fn[0] != ".":
            fileslist.append(os.path.join(root, fn))
  return fileslist


def find_file_endwith_specified_character(inputlist,endstr=''):
    filelist = []
    for file in inputlist:
        if file.endswith(endstr):
            filelist.append(file)
    return filelist

def send_email():
    mail_host = Config.SMTPServer
    sender = Config.emailSender
    password = Config.emialPasswd
    receivers = Config.receivers
    files = list_only_files_recursive(REPORT_PATH)
    htmlfiles = find_file_endwith_specified_character(files,endstr='.html')
    e = Email(title='测试报告',
                message='',
                receiver= receivers,
                  server=mail_host,
                  sender=sender,
                  password=password,
                  htmlReportList= htmlfiles
                  )
    e.send()
