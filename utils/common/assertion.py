"""Custom assertions"""
from config.globalconfig import OUTPUT_VIDEO_RESOLUTION
from utils.common import log
import os.path
filename= os.path.basename(os.path.realpath(__file__)).split('.')[0]
logger = log.Logger(filename).get_logger()
# def assert_video_infor(videoPath,ExpectedResolution,OutputType='video',ExpectedCodecType=None,):
#     """
#     :param videoPath:
#     :param ExpectedResolution: can be any in list ['1080p','1k(960*480)','3k(dci)','4k(uhd)','4k(dci)','5k(dci)','6k(dci)',
#     '6k(uhd)','7k(dci)','8k(uhd)','1024_left_right','1280_left_right','1440_left_right','2048_left_right','2880_left_right','3072_left_right',
#     '1024_top_bottom','1280_top_bottom','1440_top_bottom','2048_top_bottom','2880_top_bottom','3072_top_bottom','2120_left_right','2120_top_bottom']
#     :param OutputType: can be any of 'video','png'
#     :param ExpectedCodecType: can be any of 'H264','H265'
#     """
#     ExpectedCodecType = ExpectedCodecType.upper()
#     outputResolutionList = ['1080p','1k','3k_dci','4k_uhd','4k_dci','5k_dci','6k_dci', '6k_uhd','7k_dci','8k_uhd',
#                             '1024_left_right','1280_left_right','1440_left_right','2048_left_right','2880_left_right','3072_left_right',
#                             '1024_top_bottom','1280_top_bottom','1440_top_bottom','2048_top_bottom','2880_top_bottom','3072_top_bottom',
#                             '2120_left_right','2120_top_bottom']
#     codecTypelist = ['H264', 'H265']
#     ActualVideoinfor = getVideoPngInfor(videoPath)
#     if ExpectedResolution in outputResolutionList:
#         if (
#                 ActualVideoinfor['Videowidth'] != OUTPUT_VIDEO_RESOLUTION[ExpectedResolution]['Videowidth']
#             and ActualVideoinfor['Videoheight'] != OUTPUT_VIDEO_RESOLUTION[ExpectedResolution]['Videoheight']
#             ):
#             raise AssertionError('Output resolution error!')  # 抛出AssertionError，unittest会自动判别为用例Failure，不是Error
#     else:
#         logger.error('Parameter error! Please input the correct output resolution parameter.')
#
#     if ExpectedCodecType:
#         print('ExpectedCodecType:',ExpectedCodecType.upper())
#
#         if ExpectedCodecType not in codecTypelist:
#             logger.error('Parameter error! Please input the correct codec type parameter.')
#
#     if OutputType == 'video':
#         if ExpectedResolution in outputResolutionList:
#             if ActualVideoinfor['Videocodec'] != ExpectedCodecType:
#                 raise AssertionError('Output codecType error!')
#         else:
#             logger.error('Parameter error! Please input the correct output resolution parameter.')
#     elif OutputType == 'png':
#         pass
#     else:
#         logger.error('Parameter error! Please input the correct output type parameter.')
#
#
