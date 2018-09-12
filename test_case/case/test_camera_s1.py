#-*- coing=utf-8 -*-
from test_case.common.WonderStitchCommonClass import *
import unittest
from utils.common.file_reader import *
from parameterized import parameterized,param
from utils.common.assertion import *
import sys
from utils.common.log import Logger
from utils.common.common_func import *

filename= os.path.basename(os.path.realpath(__file__))
loggername= filename.split('.')[0]
logger = Logger(loggername).get_logger()
test_data = os.path.join(TEST_DATA_PATH,'TestCase.xlsx')
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

# def custom_name_func(testcase_func, param_num, param):
#     return "%s_%s" %(
#         testcase_func.__name__,
#         parameterized.to_safe_name("_".join(str(x) for x in param.args[0:1])),
#     )

reader = ExcelReader(test_data, sheet=0, title_line=True)
testdata = reader.sheet_data
class S1BasicTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = app(backend='uia')
        cls.app.run(appPath=TEST_APP_PATH)

    @classmethod
    def tearDownClass(cls):
       cls.app = app(backend='uia')
       cls.app.connect(appPath=TEST_APP_PATH)
       cls.app.close()


    @parameterized.expand([
        ('1080p', testdata[0]['测试参数']),
        ('1k',testdata[0]['测试参数']),
        ('3k_dci', testdata[0]['测试参数']),
        ('4k_uhd', testdata[0]['测试参数']),
        ('4k_dci', testdata[0]['测试参数']),
        ('5k_dci', testdata[0]['测试参数']),
        ('6k_dci', testdata[0]['测试参数']),
        ('6k_uhd', testdata[0]['测试参数']),
    ],testcase_func_name=custom_name_func)

    @get_err_image
    def test_s1_case000001(self,outputResolution,testdata):
        """重点测试S1拼接方式为opticalflow-full时,能否正常输出各种分辨率('1080p','1k','3k_dci','4k_uhd','4k_dci','5k_dci','6k_dci','6k_uhd')的拼接视频"""
        testcasedata = eval(testdata)
        print("testcasedata:",testcasedata)
        stitch= StithWindowTest(TestOutPutResolution= outputResolution,**testcasedata)
        stitch.test_stitch_window()
        screenshot_img(stitch.StitchVideooutputPath)
        stitch.stitch_window.start_stitch()
        stitch_result = stitch.stitching_pane.stitching_log()
        stitch.stitching_pane.close_stitch()
        self.assertEqual(stitch_result['process_result'],'Process finish:success',msg='Stitch failed!')
        newOutputVideo = get_lately_video(stitch.StitchVideooutputPath)
        videoInfor = getVideoPngInfor(newOutputVideo)
        print(videoInfor)
        self.assertEqual(videoInfor['Videowidth'],OUTPUT_VIDEO_RESOLUTION[outputResolution]['Videowidth'],msg='Error of output video resolution ')
        self.assertEqual(videoInfor['Videoheight'],OUTPUT_VIDEO_RESOLUTION[outputResolution]['Videoheight'])
        self.assertEqual(videoInfor['Videocodec'],testcasedata[ 'codec_type'].upper(),msg='Output video coding is not consistent with expected coding.' )
        self.assertEqual(videoInfor['Videoaudio'],'true',msg='Audio signal loss in video!')

    @parameterized.expand([
        ('1080p', testdata[1]['测试参数']),
        ('1k', testdata[1]['测试参数']),
        ('3k_dci', testdata[1]['测试参数']),
        ('4k_uhd', testdata[1]['测试参数']),
        ('4k_dci', testdata[1]['测试参数']),
        ('5k_dci', testdata[1]['测试参数']),
        ('6k_dci', testdata[1]['测试参数']),
        ('6k_uhd', testdata[1]['测试参数']),
    ], testcase_func_name=custom_name_func)
    @get_err_image
    def test_s1_case000002(self, outputResolution, testdata):
        """重点测试S1拼接方式为opticalflow-hybrid时,能否正常输出各种分辨率('1080p','1k','3k_dci','4k_uhd','4k_dci','5k_dci','6k_dci','6k_uhd')的拼接视频"""
        testcasedata = eval(testdata)
        print("testcasedata:",testcasedata)
        stitch = StithWindowTest(TestOutPutResolution=outputResolution, **testcasedata)
        stitch.test_stitch_window()
        screenshot_img(stitch.StitchVideooutputPath)
        stitch.stitch_window.start_stitch()
        stitch_result = stitch.stitching_pane.stitching_log()
        stitch.stitching_pane.close_stitch()
        self.assertEqual(stitch_result['process_result'], 'Process finish:success', msg='Stitch failed!')
        newOutputVideo = get_lately_video(stitch.StitchVideooutputPath)
        videoInfor = getVideoPngInfor(newOutputVideo)
        print(videoInfor)
        self.assertEqual(videoInfor['Videowidth'], OUTPUT_VIDEO_RESOLUTION[outputResolution]['Videowidth'],
                         msg='Error of output video resolution ')
        self.assertEqual(videoInfor['Videoheight'], OUTPUT_VIDEO_RESOLUTION[outputResolution]['Videoheight'])
        self.assertEqual(videoInfor['Videocodec'], testcasedata['codec_type'].upper(),
                         msg='Output video coding is not consistent with expected coding.')
        self.assertEqual(videoInfor['Videoaudio'], 'true', msg='Audio signal loss in video!')

    @parameterized.expand([
        ('1080p', testdata[2]['测试参数']),
        ('1k', testdata[2]['测试参数']),
        ('3k_dci', testdata[2]['测试参数']),
        ('4k_uhd', testdata[2]['测试参数']),
        ('4k_dci', testdata[2]['测试参数']),
        ('5k_dci', testdata[2]['测试参数']),
        ('6k_dci', testdata[2]['测试参数']),
        ('6k_uhd', testdata[2]['测试参数']),
    ], testcase_func_name=custom_name_func)
    @get_err_image
    def test_s1_case000003(self, outputResolution, testdata):
        """重点测试S1拼接方式为expressmode时,能否正常输出各种分辨率('1080p','1k','3k_dci','4k_uhd','4k_dci','5k_dci','6k_dci','6k_uhd')的拼接视频"""
        testcasedata = eval(testdata)
        print("testcasedata:",testcasedata)
        stitch = StithWindowTest(TestOutPutResolution=outputResolution, **testcasedata)
        stitch.test_stitch_window()
        screenshot_img(stitch.StitchVideooutputPath)
        stitch.stitch_window.start_stitch()
        stitch_result = stitch.stitching_pane.stitching_log()
        stitch.stitching_pane.close_stitch()
        self.assertEqual(stitch_result['process_result'], 'Process finish:success', msg='Stitch failed!')
        newOutputVideo = get_lately_video(stitch.StitchVideooutputPath)
        videoInfor = getVideoPngInfor(newOutputVideo)
        print(videoInfor)
        self.assertEqual(videoInfor['Videowidth'], OUTPUT_VIDEO_RESOLUTION[outputResolution]['Videowidth'],
                         msg='Error of output video resolution ')
        self.assertEqual(videoInfor['Videoheight'], OUTPUT_VIDEO_RESOLUTION[outputResolution]['Videoheight'])
        self.assertEqual(videoInfor['Videocodec'], testcasedata['codec_type'].upper(),
                         msg='Output video coding is not consistent with expected coding.')
        self.assertEqual(videoInfor['Videoaudio'], 'true', msg='Audio signal loss in video!')

    @parameterized.expand([
        ('1080p', testdata[3]['测试参数']),
        ('1k', testdata[3]['测试参数']),
        ('3k_dci', testdata[3]['测试参数']),
        ('4k_uhd', testdata[3]['测试参数']),
        ('4k_dci', testdata[3]['测试参数']),
        ('5k_dci', testdata[3]['测试参数']),
        ('6k_dci', testdata[3]['测试参数']),
        ('6k_uhd', testdata[3]['测试参数']),
    ], testcase_func_name=custom_name_func)
    @get_err_image
    def test_s1_case000004(self, outputResolution, testdata):
        """重点测试S1拼接方式为opticalflow-full时,能否正常输出各种分辨率('1080p','1k','3k_dci','4k_uhd','4k_dci','5k_dci','6k_dci','6k_uhd')的拼接图片"""
        testcasedata = eval(testdata)
        print("testcasedata:", testcasedata)
        stitch = StithWindowTest(TestOutPutResolution=outputResolution, **testcasedata)
        stitch.test_stitch_window()
        OutputPngPath = os.path.join(stitch.StitchVideooutputPath, stitch.TestVideoName + '_pano')
        screenshot_img(stitch.StitchVideooutputPath)
        stitch.stitch_window.start_stitch()
        stitch_result = stitch.stitching_pane.stitching_log()
        stitch.stitching_pane.close_stitch()
        self.assertEqual(stitch_result['process_result'], 'Process finish:success', msg='Stitch failed!')
        pnglist = os.listdir(OutputPngPath)
        png = pnglist[0]
        png = os.path.join(OutputPngPath,png)
        #print('png:',png)
        pngInfor = getVideoPngInfor(png)
        print(pngInfor)
        self.assertEqual(pngInfor['Videowidth'], OUTPUT_VIDEO_RESOLUTION[outputResolution]['Videowidth'],
                         msg='Error of output video resolution ')
        self.assertEqual(pngInfor['Videoheight'], OUTPUT_VIDEO_RESOLUTION[outputResolution]['Videoheight'])

    @parameterized.expand([
        ('1080p', testdata[4]['测试参数']),
        ('1k', testdata[4]['测试参数']),
        ('3k_dci', testdata[4]['测试参数']),
        ('4k_uhd', testdata[4]['测试参数']),
        ('4k_dci', testdata[4]['测试参数']),
        ('5k_dci', testdata[4]['测试参数']),
        ('6k_dci', testdata[4]['测试参数']),
        ('6k_uhd', testdata[4]['测试参数']),
    ], testcase_func_name=custom_name_func)
    @get_err_image
    def test_s1_case000005(self, outputResolution, testdata):
        """重点测试S1拼接方式为opticalflow-hybrid时,能否正常输出各种分辨率('1080p','1k','3k_dci','4k_uhd','4k_dci','5k_dci','6k_dci','6k_uhd')的拼接图片"""
        testcasedata = eval(testdata)
        print("testcasedata:", testcasedata)
        stitch = StithWindowTest(TestOutPutResolution=outputResolution, **testcasedata)
        stitch.test_stitch_window()
        OutputPngPath = os.path.join(stitch.StitchVideooutputPath, stitch.TestVideoName + '_pano')
        screenshot_img(stitch.StitchVideooutputPath)
        stitch.stitch_window.start_stitch()
        stitch_result = stitch.stitching_pane.stitching_log()
        stitch.stitching_pane.close_stitch()
        self.assertEqual(stitch_result['process_result'], 'Process finish:success', msg='Stitch failed!')
        pnglist = os.listdir(OutputPngPath)
        png = pnglist[0]
        png = os.path.join(OutputPngPath,png)
        #print('png:',png)
        pngInfor = getVideoPngInfor(png)
        print(pngInfor)
        self.assertEqual(pngInfor['Videowidth'], OUTPUT_VIDEO_RESOLUTION[outputResolution]['Videowidth'],
                         msg='Error of output video resolution ')
        self.assertEqual(pngInfor['Videoheight'], OUTPUT_VIDEO_RESOLUTION[outputResolution]['Videoheight'])

    @parameterized.expand([
        ('1080p', testdata[5]['测试参数']),
        ('1k', testdata[5]['测试参数']),
        ('3k_dci', testdata[5]['测试参数']),
        ('4k_uhd', testdata[5]['测试参数']),
        ('4k_dci', testdata[5]['测试参数']),
        ('5k_dci', testdata[5]['测试参数']),
        ('6k_dci', testdata[5]['测试参数']),
        ('6k_uhd', testdata[5]['测试参数']),
    ], testcase_func_name=custom_name_func)

    @get_err_image
    def test_s1_case000006(self, outputResolution, testdata):
        """重点测试S1拼接方式为expressmode时,能否正常输出各种分辨率('1080p','1k','3k_dci','4k_uhd','4k_dci','5k_dci','6k_dci','6k_uhd')的拼接图片"""
        testcasedata = eval(testdata)
        print("testcasedata:", testcasedata)
        stitch = StithWindowTest(TestOutPutResolution=outputResolution, **testcasedata)
        stitch.test_stitch_window()
        OutputPngPath = os.path.join(stitch.StitchVideooutputPath, stitch.TestVideoName + '_pano')
        screenshot_img(stitch.StitchVideooutputPath)
        stitch.stitch_window.start_stitch()
        stitch_result = stitch.stitching_pane.stitching_log()
        stitch.stitching_pane.close_stitch()
        self.assertEqual(stitch_result['process_result'], 'Process finish:success', msg='Stitch failed!')
        pnglist = os.listdir(OutputPngPath)
        png = pnglist[0]
        png = os.path.join(OutputPngPath,png)
        #print('png:',png)
        pngInfor = getVideoPngInfor(png)
        print(pngInfor)
        self.assertEqual(pngInfor['Videowidth'], OUTPUT_VIDEO_RESOLUTION[outputResolution]['Videowidth'],
                         msg='Error of output video resolution ')
        self.assertEqual(pngInfor['Videoheight'], OUTPUT_VIDEO_RESOLUTION[outputResolution]['Videoheight'])

    @parameterized.expand([
        ('1080p', testdata[6]['测试参数']),
        ('1k', testdata[6]['测试参数']),
        ('3k_dci', testdata[6]['测试参数']),
        ('4k_uhd', testdata[6]['测试参数']),
        ('4k_dci', testdata[6]['测试参数']),
        ('5k_dci', testdata[6]['测试参数']),
        ('6k_dci', testdata[6]['测试参数']),
        ('6k_uhd', testdata[6]['测试参数']),
    ], testcase_func_name=custom_name_func)

    @get_err_image
    def test_s1_case000007(self, outputResolution, testdata):
        """重点测试S1的源图片在拼接方式为opticalflow-full时,能否正常输出各种分辨率('1080p','1k','3k_dci','4k_uhd','4k_dci','5k_dci','6k_dci','6k_uhd')的拼接图片"""
        testcasedata = eval(testdata)
        print("testcasedata:", testcasedata)
        stitch = StithWindowTest(TestOutPutResolution=outputResolution, **testcasedata)
        stitch.test_stitch_window()
        fileList = list_only_files_recursive(src_dir=stitch.InputFileDirectory)
        inputPngList = find_file_endwith_specified_character(fileList,endstr='.JPG')
        oneInputPngDirName = inputPngList[0].split('\\')[-2]
        OneOutputPngPath = os.path.join(stitch.StitchVideooutputPath, oneInputPngDirName + '_pano')
        screenshot_img(stitch.StitchVideooutputPath)
        stitch.stitch_window.start_stitch()
        stitch_result = stitch.stitching_pane.stitching_log()
        stitch.stitching_pane.close_stitch()
        self.assertEqual(stitch_result['process_result'], 'Process finish:success', msg='Stitch failed!')
        files = os.listdir(OneOutputPngPath)
        outputPnglist = find_file_endwith_specified_character(files,endstr='.png')
        png = outputPnglist[0]
        png = os.path.join(OneOutputPngPath, png)
        pngInfor = getVideoPngInfor(png)
        print(pngInfor)
        self.assertEqual(pngInfor['Videowidth'], OUTPUT_VIDEO_RESOLUTION[outputResolution]['Videowidth'],
                         msg='Error of output video resolution ')
        self.assertEqual(pngInfor['Videoheight'], OUTPUT_VIDEO_RESOLUTION[outputResolution]['Videoheight'])

    @parameterized.expand([
        ('1080p', testdata[7]['测试参数']),
        ('1k', testdata[7]['测试参数']),
        ('3k_dci', testdata[7]['测试参数']),
        ('4k_uhd', testdata[7]['测试参数']),
        ('4k_dci', testdata[7]['测试参数']),
        ('5k_dci', testdata[7]['测试参数']),
        ('6k_dci', testdata[7]['测试参数']),
        ('6k_uhd', testdata[7]['测试参数']),
    ], testcase_func_name=custom_name_func)

    @get_err_image
    def test_s1_case000008(self, outputResolution, testdata):
        """重点测试S1的源图片在拼接方式为opticalflow-hybrid时,能否正常输出各种分辨率('1080p','1k','3k_dci','4k_uhd','4k_dci','5k_dci','6k_dci','6k_uhd')的拼接图片"""
        testcasedata = eval(testdata)
        print("testcasedata:", testcasedata)
        stitch = StithWindowTest(TestOutPutResolution=outputResolution, **testcasedata)
        stitch.test_stitch_window()
        fileList = list_only_files_recursive(src_dir=stitch.InputFileDirectory)
        inputPngList = find_file_endwith_specified_character(fileList, endstr='.JPG')
        oneInputPngDirName = inputPngList[0].split('\\')[-2]
        OneOutputPngPath = os.path.join(stitch.StitchVideooutputPath, oneInputPngDirName + '_pano')
        screenshot_img(stitch.StitchVideooutputPath)
        stitch.stitch_window.start_stitch()
        stitch_result = stitch.stitching_pane.stitching_log()
        stitch.stitching_pane.close_stitch()
        self.assertEqual(stitch_result['process_result'], 'Process finish:success', msg='Stitch failed!')
        files = os.listdir(OneOutputPngPath)
        outputPnglist = find_file_endwith_specified_character(files, endstr='.png')
        png = outputPnglist[0]
        png = os.path.join(OneOutputPngPath, png)
        pngInfor = getVideoPngInfor(png)
        print(pngInfor)
        self.assertEqual(pngInfor['Videowidth'], OUTPUT_VIDEO_RESOLUTION[outputResolution]['Videowidth'],
                         msg='Error of output video resolution ')
        self.assertEqual(pngInfor['Videoheight'], OUTPUT_VIDEO_RESOLUTION[outputResolution]['Videoheight'])

    @parameterized.expand([
        ('1080p', testdata[8]['测试参数']),
        ('1k', testdata[8]['测试参数']),
        ('3k_dci', testdata[8]['测试参数']),
        ('4k_uhd', testdata[8]['测试参数']),
        ('4k_dci', testdata[8]['测试参数']),
        ('5k_dci', testdata[8]['测试参数']),
        ('6k_dci', testdata[8]['测试参数']),
        ('6k_uhd', testdata[8]['测试参数']),
    ], testcase_func_name=custom_name_func)

    @get_err_image
    def test_s1_case000009(self, outputResolution, testdata):
        """重点测试S1的源图片在拼接方式为expressmode时,能否正常输出各种分辨率('1080p','1k','3k_dci','4k_uhd','4k_dci','5k_dci','6k_dci','6k_uhd')的拼接图片"""
        testcasedata = eval(testdata)
        print("testcasedata:", testcasedata)
        stitch = StithWindowTest(TestOutPutResolution=outputResolution, **testcasedata)
        stitch.test_stitch_window()
        fileList = list_only_files_recursive(src_dir=stitch.InputFileDirectory)
        inputPngList = find_file_endwith_specified_character(fileList, endstr='.JPG')
        oneInputPngDirName = inputPngList[0].split('\\')[-2]
        OneOutputPngPath = os.path.join(stitch.StitchVideooutputPath, oneInputPngDirName + '_pano')
        screenshot_img(stitch.StitchVideooutputPath)
        stitch.stitch_window.start_stitch()
        stitch_result = stitch.stitching_pane.stitching_log()
        stitch.stitching_pane.close_stitch()
        self.assertEqual(stitch_result['process_result'], 'Process finish:success', msg='Stitch failed!')
        files = os.listdir(OneOutputPngPath)
        outputPnglist = find_file_endwith_specified_character(files, endstr='.png')
        png = outputPnglist[0]
        png = os.path.join(OneOutputPngPath, png)
        pngInfor = getVideoPngInfor(png)
        print(pngInfor)
        self.assertEqual(pngInfor['Videowidth'], OUTPUT_VIDEO_RESOLUTION[outputResolution]['Videowidth'],
                         msg='Error of output video resolution ')
        self.assertEqual(pngInfor['Videoheight'], OUTPUT_VIDEO_RESOLUTION[outputResolution]['Videoheight'])


class S1AdvanceTest(unittest.TestCase):
    pass