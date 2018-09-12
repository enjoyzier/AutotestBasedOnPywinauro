#-*- coing=utf-8 -*-
import os
BASE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
CONFIG_PATH = os.path.join(BASE_PATH,'config')
TEST_DATA_PATH = os.path.join(BASE_PATH, 'test_data')
TEST_OUTPUT_PICTURE_PATH = os.path.join(BASE_PATH,'test_output_picture')
LOG_PATH = os.path.join(BASE_PATH, 'report','log')
REPORT_PATH = os.path.join(BASE_PATH, 'report')
STATIC_PATH = os.path.join(BASE_PATH,'static')
TEST_CASE_PATH = os.path.join(BASE_PATH,'test_case')
UTILS_PATH = os.path.join(BASE_PATH,'utils')
TEST_APP_PATH = r'C:\Users\wu\Desktop\releasebin_20180810\Z CAM WonderStitch.exe'
OUTPUT_PATH = r'C:\Users\wu\Desktop\work8-16'
OUTPUT_VIDEO_RESOLUTION = {
    '1080p':{'Videowidth':'1920','Videoheight':'960'},
    '1k':{'Videowidth':'960','Videoheight':'480'},
    '3k_dci':{'Videowidth':'3072','Videoheight':'1536'},
    '4k_uhd':{'Videowidth':'3840','Videoheight':'1920'},
    '4k_dci':{'Videowidth':'4096','Videoheight':'2048'},
    '5k_dci':{'Videowidth':'5120','Videoheight':'2560'},
    '6k_dci':{'Videowidth':'6144','Videoheight':'3072'},
    '6k_uhd':{'Videowidth':'5760','Videoheight':'2880'},
    '7k_dci':{'Videowidth':'7168','Videoheight':'3584'},
    '8k_uhd':{'Videowidth':'7680','Videoheight':'3840'},
    '1024_left_right':{'Videowidth':'2048','Videoheight':'1024'},
    '1280_left_right':{'Videowidth':'2560','Videoheight':'1280'},
    '1440_left_right':{'Videowidth':'2880','Videoheight':'1440'},
    '2048_left_right':{'Videowidth':'4096','Videoheight':'2048'},
    '2880_left_right':{'Videowidth':'5760','Videoheight':'2880'},
    '3072_left_right':{'Videowidth':'6144','Videoheight':'3072'},
    '1024_top_bottom':{'Videowidth':'1024','Videoheight':'2048'},
    '1280_top_bottom':{'Videowidth':'1280','Videoheight':'2560'},
    '1440_top_bottom':{'Videowidth':'1440','Videoheight':'2880'},
    '2048_top_bottom':{'Videowidth':'2048','Videoheight':'4096'},
    '2880_top_bottom':{'Videowidth':'2880','Videoheight':'5760'},
    '3072_top_bottom':{'Videowidth':'3072','Videoheight':'6144'},
    '2120_left_right':{'Videowidth':'4240','Videoheight':'1248'},
    '2120_top_bottom':{'Videowidth':'2120','Videoheight':'2496'},
}