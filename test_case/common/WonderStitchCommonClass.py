#-*- coing=utf-8 -*-
from pywinauto import Application
from pywinauto.keyboard import *
from pywinauto import actionlogger
import utils.common.log as log
from utils.common.file_reader import Config
from uiautomation import *
import os.path
from pywinauto.findwindows import ElementNotFoundError

filename = os.path.basename(os.path.realpath(__file__)).split('.')[0]
logger = log.Logger(filename).get_logger()
config = Config()
TEST_APP_PATH = Config.testAppPath

#==========================conmmon class=================================
class app(object):

    def __init__(self,backend='uia'):
        """Initialization method, initializing a app
        :param appPath: Program name, support path
        """
        self.backend=backend
        self.app = Application(self.backend)

    def run(self,appPath):
        """start the application"""
        self.app.start(appPath)
        time.sleep(3)

    def connect(self,appPath):
        """collect the application"""
        self.app.connect(path=appPath)

    def close(self):
        try:
            self.app.kill()
            time.sleep(1)
        except Exception as e:
            ws_dlg = self.app.window(class_name='Qt5QWindowIcon', )
            ws_dlg.Button3.click()

class common_control(object):
    @classmethod
    def scroll_controll(self,direction='up'):
        """:param direction: can be any of "up", "down", """
        direction=direction.lower()
        scrollController=Control(searchDepth=0x00000008, ControlType=ControlType.ScrollBarControl,foundIndex=1)
        if direction=='down':
            scrollController.WheelDown(wheelTimes = 4,waitTime=2)
        elif direction == 'up':
            scrollController.WheelUp(wheelTimes = 4,waitTime=2)
        else:
            logger.error('Parameter error! The optional parameter of scroll_controll values are "up","down",')

    @classmethod
    def ok_enter_botton(self):
        OkEnterBottonController = Control( ControlType=ControlType.ButtonControl,Name = "Ok Enter")
        if WaitForExist(OkEnterBottonController,timeout=1):
            OkEnterBottonController.Click()


class current_value(object):
    """仅适用于s1,s1pro,v1,v1pro的拼接界面"""
    @classmethod
    def get_corrent_outputValue(self):
        outputCustomControl = Control(searchDepth=0x0000000C, Name="Output", ControlType=ControlType.CustomControl,
                                      foundIndex=3)

        outputType = Control(searchFromControl=outputCustomControl, name=" Down",
                             ControlType=ControlType.ComboBoxControl)
        outputValue = outputType.AccessibleCurrentValue()
        return outputValue

    @classmethod
    def get_corrent_cameraModelValue(self):
        cameraTypeCustomControl = Control(searchDepth=0x0000000C, Name="Camera Type", ControlType=ControlType.CustomControl,
                                      foundIndex=1)

        cameraModel= Control(searchFromControl=cameraTypeCustomControl, name=" Down",
                             ControlType=ControlType.ComboBoxControl)
        cameraModelValue = cameraModel.AccessibleCurrentValue()
        return cameraModelValue

    @classmethod
    def get_corrent_inputValue(self):
        inputCustomControl = Control(searchDepth=0x0000000C, Name="Input", ControlType=ControlType.CustomControl,
                                      foundIndex=1)

        inputType = Control(searchFromControl=inputCustomControl, name=" Down",
                             ControlType=ControlType.ComboBoxControl)
        inputTypeValue = inputType.AccessibleCurrentValue()
        return inputTypeValue


    @classmethod
    def get_corrent_stitchTypeValue(self):
        outputValue = current_value.get_corrent_outputValue()
        if outputValue == 'PNG':
            BasicSettingsCustomControl = Control(searchDepth=0x0000000C, Name="Basic Settings", ControlType=ControlType.CustomControl,
                                      foundIndex=2)
        else:
            BasicSettingsCustomControl = Control(searchDepth=0x0000000C, Name="Basic Settings",
                                        ControlType=ControlType.CustomControl,
                                        foundIndex=4)
        sitchType = Control(searchFromControl=BasicSettingsCustomControl, name=" Down",
                             ControlType=ControlType.ComboBoxControl)
        sitchTypeValue = sitchType.AccessibleCurrentValue()
        return sitchTypeValue


class stitch_window_page(object):
    """仅适用于s1,s1pro,v1,v1pro的拼接界面,使用该类的方法需要先转到stitch界面,可以通过choose_stitch_tab()方法转到stitch界面"""

    def __init__(self):
        self.app = Application(backend='uia').connect(path=TEST_APP_PATH)

    def get_ws_dlg(self):
        stitch_window_dlg=Control( ClassName='Qt5QWindowIcon',ControlType=ControlType.WindowControl,searchDepth=0x01)
        if WaitForExist(stitch_window_dlg,60):
            ws_dlg = self.app.window(class_name='Qt5QWindowIcon', )
        else:
            ws_dlg=None
            logger.error('stitch window NotFoundError')
        return ws_dlg

    def choose_stitch_tab(self):
        ws_dlg=self.get_ws_dlg()
        if ws_dlg != None:
            #choose stitchTabControlWrapper
            stitch_window = ws_dlg.child_window(title="Stitch", control_type="Tab").StitchTabItem.select()
            stitch_window.click_input()
            time.sleep(1)

    def choose_encode_tab(self):
        ws_dlg = self.get_ws_dlg()
        if ws_dlg != None:
            # choose EcodeTabControlWrapper
            encode_window = ws_dlg.child_window(title="Stitch", control_type="Tab").EncodeTabItem.select()
            encode_window.click_input()
            time.sleep(1)

    def camera_model(self,cameraModel):
        cameraModel=cameraModel.lower()
        ws_dlg=self.get_ws_dlg()
        if ws_dlg != None:
            # choose child_window(title="Camera TypeCustom", control_type="Custom")
            CameraTypeCustom1 = ws_dlg['Camera TypeCustom1']
            cameraModelControl = CameraTypeCustom1.DownComboBox
            if cameraModelControl.is_enabled():
                cameraModelControl.invoke()
                if cameraModel == 's1':
                    #select model=s1
                    cameraModelControl.child_window(title="S1", control_type="ListItem").click_input()

                elif cameraModel == 's1pro':
                    # select model=s1pro
                    cameraModelControl.child_window(title="S1 Pro", control_type="ListItem").click_input()

                elif cameraModel == 'v1':
                    #select model=v1
                    cameraModelControl.child_window(title="V1", control_type="ListItem").click_input()

                elif cameraModel == 'v1pro':
                    #select model=v1pro
                    cameraModelControl.child_window(title="V1 Pro", control_type="ListItem").click_input()

                elif cameraModel == 'k1pro':
                    # select model=k1pro
                    cameraModelControl.child_window(title="K1 Pro", control_type="ListItem").click_input()

                else:
                    logger.error('Parameter error! The optional parameter values of camera-model are "s1","s1pro","v1","v1pro","k1pro"')

                time.sleep(2)
            else:
                logger.error('Current camera_model  ComboBoxControl is in a gray state, and you can not operate it.')

    def camera_id(self,cameraId):
        ws_dlg = self.get_ws_dlg()
        if ws_dlg != None:
            #choose child_window(title="Camera TypeCustom2", control_type="Custom")
            CameraTypeCustom2 = ws_dlg['Camera TypeCustom2']
            #choose Camera IDEdit
            cameraIdEditControl= CameraTypeCustom2.Edit1
            if cameraIdEditControl.is_enabled():
                cameraIdEditControl.invoke()
                # ctrl+A
                cameraIdEditControl.type_keys('^a^c')
                cameraIdEditControl.type_keys(cameraId)
                cameraIdEditControl.type_keys('{VK_RETURN}')
                time.sleep(1)
            else:
                logger.error('Current camera_id EditControl is in a gray state, and you can not operate it.')

    def clear_config(self):
        ws_dlg = self.get_ws_dlg()
        if ws_dlg != None:
            ws_dlg.child_window(title="Clear Config", control_type="Button").click()
            time.sleep(1)

    def input_type(self,inputType='video'):
        inputType=inputType.lower()
        ws_dlg = self.get_ws_dlg()
        if ws_dlg != None:
            InputCustom = ws_dlg['InputCustom']
            #open input_type ComboBoxWrapper
            inputTypeControl=InputCustom.DownComboBox2
            if inputTypeControl.is_enabled():
                inputTypeControl.invoke()
                if inputType == 'video':
                    ##select input_type = video
                    inputTypeControl.child_window(title="Video", control_type="ListItem").click_input()
                elif inputType == 'photo':
                    inputTypeControl.child_window(title="Photo", control_type="ListItem").click_input()
                else:
                    logger.error('Parameter error! The optional parameter of input_type values are "video","photo",')
                time.sleep(2)
            else:
                logger.error('Current  input_type ComboBoxControl is in a gray state, and you can not operate it.')

    def input_file_directory(self,inputPath):
        ws_dlg = self.get_ws_dlg()
        if ws_dlg != None:
            #choose child_window(title="InputCustom2", control_type="Custom")
            InputCustom2=ws_dlg['InputCustom2']
            #choose input file directory edit
            inputFileDirectoryEdit= InputCustom2.Edit2.invoke()
            # ctrl+A
            inputFileDirectoryEdit.type_keys('^a^c')
            inputFileDirectoryEdit.type_keys(inputPath,with_spaces=True)
            inputFileDirectoryEdit.type_keys('{VK_RETURN}')
            time.sleep(5)
            common_control.ok_enter_botton()


    def stitch_frame(self,startFrame,endFrame):
        ws_dlg = self.get_ws_dlg()
        if ws_dlg != None:
            if startFrame <= endFrame:
                InputCustom3=ws_dlg['InputCustom3']
                startFrameEdit=InputCustom3.Edit3
                endFrameEdit = InputCustom3.Edit2
                # ctrl+A
                startFrameEdit.invoke()
                startFrameEdit.type_keys('^a^c')
                startFrameEdit.type_keys(startFrame)
                startFrameEdit.type_keys('{VK_RETURN}')
                time.sleep(2)
                endFrameEdit.invoke()
                endFrameEdit.type_keys('^a^c')
                endFrameEdit.type_keys(endFrame)
                endFrameEdit.type_keys('{VK_RETURN}')
                time.sleep(2)
            else:
                logger.error('startFrame should not greater than endFrame ')

    def destination_directory(self,outputPath):
        if not os.path.exists(outputPath):
            os.makedirs(outputPath)
        ws_dlg = self.get_ws_dlg()
        if ws_dlg != None:
            OutputCustom1=ws_dlg['OutputCustom1']
            destinationDirectoryEdit=OutputCustom1.Edit5.invoke()
            destinationDirectoryEdit.type_keys('^a^c')
            destinationDirectoryEdit.type_keys(outputPath)
            destinationDirectoryEdit.type_keys('{VK_RETURN}')

            time.sleep(2)
            common_control.ok_enter_botton()

    def output_resolution(self,outputResolution='4K_uhd'):
        outputResolution=outputResolution.lower()
        ws_dlg = self.get_ws_dlg()
        if ws_dlg != None:
            cametaModelValue = current_value.get_corrent_cameraModelValue()
            stitchTypeValue = current_value.get_corrent_stitchTypeValue()
            OutputCustom2 = ws_dlg['OutputCustom2']
            OutputResolutionControl = OutputCustom2.DownComboBox3
            if OutputResolutionControl.is_enabled():
                try:
                    OutputResolutionControl.invoke()
                    if outputResolution == '1k':
                        OutputResolutionControl.child_window(title="1K(960x480)", control_type="ListItem").click_input()
                    elif outputResolution == '1080p':
                        OutputResolutionControl.child_window(title="1080P", control_type="ListItem").click_input()
                    elif outputResolution == '3k_dci':
                        OutputResolutionControl.child_window(title="3K(DCI)", control_type="ListItem").click_input()
                    elif outputResolution == '4k_uhd':
                        OutputResolutionControl.child_window(title="4K(UHD)", control_type="ListItem").click_input()
                    elif outputResolution == '4k_dci':
                        OutputResolutionControl.child_window(title="4K(DCI)", control_type="ListItem").click_input()
                    elif outputResolution == '5k_dci':
                        OutputResolutionControl.child_window(title="5K(DCI)", control_type="ListItem").click_input()
                    elif outputResolution == '6k_dci':
                        OutputResolutionControl.child_window(title="6K(DCI)", control_type="ListItem").click_input()
                    elif outputResolution == '6k_uhd':
                        OutputResolutionControl.child_window(title="6K(UHD)", control_type="ListItem").click_input()
                    elif outputResolution == '7k_dci':
                        OutputResolutionControl.child_window(title="7K(DCI)", control_type="ListItem").click_input()
                    elif outputResolution == '8k_uhd':
                        OutputResolutionControl.child_window(title="8K(UHD)", control_type="ListItem").click_input()
                    else:
                        logger.error('Parameter error! The optional parameter values of output_resolution are "1k","1080p","3k_dci","4k_uhd","5k_dci","6k_dci","6k_uhd","7K_dci","8k_uhd"')
                    time.sleep(2)
                except Exception as e:
                    logger.error('while cameralMode = %s,stitichType = %s, output resolution: %s not exist ',cametaModelValue,stitchTypeValue,outputResolution)
            else:
                logger.error('Current output_resolution ComboBoxControl is in a gray state, and you can not operate it.')

    def output_type(self,outputType='Video'):
        outputType=outputType.lower()
        ws_dlg = self.get_ws_dlg()
        if ws_dlg != None:
            OutputCustom3 = ws_dlg['OutputCustom3']
            OutputTypeControl =  OutputCustom3.DownComboBox4
            if OutputTypeControl.is_enabled():
                OutputTypeControl.invoke()
                if outputType == 'video':
                    OutputTypeControl.child_window(title="Video", control_type="ListItem").click_input()
                elif outputType == 'png':
                    OutputTypeControl.child_window(title="PNG", control_type="ListItem").click_input()
                else:
                    logger.error('Parameter error! The optional parameter values of output_type are "video","png",')
                time.sleep(1)
            else:
                logger.error('Current output_type ComboBoxControl is in a gray state, and you can not operate it.')

    def multi_process(self,multiProcess='Off'):
        multiProcess=multiProcess.lower()
        ws_dlg = self.get_ws_dlg()
        if ws_dlg != None:
            outputValue = current_value.get_corrent_outputValue()
            if outputValue== 'PNG':
                BasicSettingsCustom0 = ws_dlg['Basic SettingsCustom0']
                multiProcessControl = BasicSettingsCustom0.DownComboBox5
            else:
                BasicSettingsCustom3 = ws_dlg['Basic SettingsCustom3']
                multiProcessControl = BasicSettingsCustom3.DownComboBox7

            if multiProcessControl.is_enabled():
                multiProcessControl.invoke()
                if multiProcess == 'on':
                    multiProcessControl.child_window(title="On", control_type="ListItem").click_input()
                elif multiProcess == 'off':
                    multiProcessControl.child_window(title="Off", control_type="ListItem").click_input()
                else:
                    logger.error('Parameter error! The optional parameter values of multi_process are "on","off",')

                time.sleep(1)
            else:
                logger.error('Current multi_process ComboBoxControl is in a gray state, and you can not operate it.')

    def stitch_type(self,stitchType='OpticalFlow-Full'):
        stitchType=stitchType.lower()
        ws_dlg = self.get_ws_dlg()
        if ws_dlg != None:
            outputValue = current_value.get_corrent_outputValue()
            cameraModelValue = current_value.get_corrent_cameraModelValue()
            if outputValue == 'PNG':
                BasicSettingsCustom2 = ws_dlg['Basic SettingsCustom2']
                stitchTypeControl = BasicSettingsCustom2.DownComboBox6
            else:
                BasicSettingsCustom4 = ws_dlg['Basic SettingsCustom4']
                stitchTypeControl = BasicSettingsCustom4.DownComboBox8
            if stitchTypeControl.is_enabled():
                stitchTypeControl.invoke()
                try:
                    if stitchType == 'opticalflow-full':
                        stitchTypeControl.child_window(title="Optical Flow - Full", control_type="ListItem").click_input()
                    elif stitchType == 'opticalflow-hybrid':
                        stitchTypeControl.child_window(title="Optical Flow - Hybrid", control_type="ListItem").click_input()
                    elif stitchType == 'expressmode':
                        stitchTypeControl.child_window(title="Express Mode", control_type="ListItem").click_input()
                    elif stitchType == 'stereo':
                        stitchTypeControl.child_window(title="Stereo", control_type="ListItem").click_input()
                    elif stitchType == 'stereonv':
                        stitchTypeControl.child_window(title="Stereo NV", control_type="ListItem").click_input()
                    elif stitchType == 'expressmodenv':
                        stitchTypeControl.child_window(title="ExpressMode NV", control_type="ListItem").click_input()
                    else:
                        logger.error('Parameter error! The optional parameter values of stitch_type are "opticalflow-full","opticalflow-hybrid","ExpressMode","stereo","StereoNV","ExpressModeNV"')

                    time.sleep(1)
                except ElementNotFoundError as e:
                    logger.error('%s does not contain the StitchType: %s ',cameraModelValue,stitchType)
            else:
                logger.error('Current stitch_type ComboBoxControl is in a gray state, and you can not operate it.')

    def stitch_engine(self,stitchEngine='GPU'):
        stitchEngine=stitchEngine.lower()
        ws_dlg = self.get_ws_dlg()
        if ws_dlg != None:
            outputValue = current_value.get_corrent_outputValue()
            if outputValue == 'PNG':
                stitchEngineControl = ws_dlg['Basic SettingsCustom3']
                stitchEngineControl.DownComboBox7.invoke()
            else:
                stitchEngineControl = ws_dlg['Basic SettingsCustom5']
                stitchEngineControl.DownComboBox9.invoke()
            try:
                if stitchEngine == 'cpu':
                    stitchEngineControl.child_window(title="CPU", control_type="ListItem").click_input()
                elif stitchEngine == 'gpu':
                    stitchEngineControl.child_window(title="GPU", control_type="ListItem").click_input()
                else:
                    logger.error('Parameter error! The optional parameter values of stitch_engine are "cpu","gpu",')
                time.sleep(1)
            except Exception as e:
                logger.error('sorroy, your computer does not contain stitch engine %s',stitchEngine)

    def codec_type(self,codecType):
        codecType=codecType.lower()
        ws_dlg = self.get_ws_dlg()
        if ws_dlg != None:
            outputValue = current_value.get_corrent_outputValue()
            if outputValue == 'Video':
                codecTypeControl = ws_dlg['Basic SettingsCustom1']
                codecTypeControl.DownComboBox5.invoke()
                if codecType == 'h264':
                    codecTypeControl.child_window(title="H264", control_type="ListItem").click_input()
                elif codecType == 'h265':
                    codecTypeControl.child_window(title="H265", control_type="ListItem").click_input()
                else:
                    logger.error('Parameter error! The optional parameter values of codec_type are "h264","h265",')
                time.sleep(1)
            else:
                logger.error('PNG outputType no codec type...!')

    def quality(self,Quality):
        Quality = Quality.lower()
        ws_dlg = self.get_ws_dlg()
        if ws_dlg != None:
            outputValue = current_value.get_corrent_outputValue()
            if outputValue == 'Video':
                qualityControl = ws_dlg['Basic SettingsCustom2']
                qualityControl.DownComboBox6.invoke()
                if Quality == 'high':
                    qualityControl.child_window(title="High(VBR)", control_type="ListItem").click_input()
                elif Quality == 'medium':
                    qualityControl.child_window(title="Medium(VBR)", control_type="ListItem").click_input()
                elif Quality == 'low':
                    qualityControl.child_window(title="Low(VBR)", control_type="ListItem").click_input()
                elif Quality == '120m':
                    qualityControl.child_window(title="120M(CBR)", control_type="ListItem").click_input()
                elif Quality == '80m':
                    qualityControl.child_window(title="80M(CBR)", control_type="ListItem").click_input()
                elif Quality == '50m':
                    qualityControl.child_window(title="50M(CBR)", control_type="ListItem").click_input()
                else:
                    logger.error(
                        'Parameter error! The optional parameter values of codec_quality are "high","medium","low","120M","80M","50M",')
                time.sleep(2)

            else:
                logger.error('PNG outputType no codec quality...!')

    def enable_brightness_adjustment(self,status=0):
        """The toggle state is represented by an integer
            status=0 - unchecked
            status=1 - checked
        """
        status=str(status)
        ws_dlg = self.get_ws_dlg()
        if ws_dlg != None:
            common_control.scroll_controll(direction='down')
            brightnessControl=ws_dlg['Basic SettingsGroupBox']
            EnableBrightnessAdjustmentControl=brightnessControl.child_window(title="Enable Brightness Adjustment", control_type="CheckBox")
            EnableBrightnessAdjustmentControl.wait(wait_for='ready',timeout=60)
            EnableBrightnessAdjustmentControl.set_focus()
            correntStatus=EnableBrightnessAdjustmentControl.get_toggle_state()
            print(correntStatus)
            if status=='1':
                if correntStatus == 1:
                    pass
                else:
                    EnableBrightnessAdjustmentControl.toggle()
            elif status == '0':
                if correntStatus == 1:
                    EnableBrightnessAdjustmentControl.toggle()
                else:
                    pass
            else:
                logger.error('Parameter error! the status of checkbox is represented by an integer，status=0:unchecked,status=1:checked')
            time.sleep(1)
            common_control.scroll_controll(direction='up')

    def enable_HDR(self,status=0):
        """The toggle state is represented by an integer
            status=0 - unchecked
            status=1 - checked
        """
        status = str(status)
        ws_dlg = self.get_ws_dlg()
        if ws_dlg != None:
            common_control.scroll_controll(direction='down')
            brightnessControl = ws_dlg['Basic SettingsGroupBox']
            EnableHDRControl=brightnessControl.child_window(title="Enable HDR", control_type="CheckBox")
            if EnableHDRControl.is_enabled():
                EnableHDRControl.set_focus()
                correntStatus=EnableHDRControl.get_toggle_state()
                print(correntStatus)
                if status == '1':
                    if correntStatus == 1:
                        pass
                    else:
                        EnableHDRControl.toggle()
                elif status == '0':
                    if correntStatus == 1:
                        EnableHDRControl.toggle()
                    else:
                        pass
                else:
                    logger.error('Parameter error! the status of checkbox is represented by an integer，status=0:unchecked,status=1:checked')
                time.sleep(1)

            else:
                logger.error('Current enable_HDR CheckBoxControl is in a gray state, and you can not operate it.')
            common_control.scroll_controll(direction='up')

    def brightness_reference(self,BrightnessReference='CameraB'):
        BrightnessReference=BrightnessReference.lower()
        ws_dlg = self.get_ws_dlg()
        if ws_dlg != None:
            common_control.scroll_controll(direction='down')
            brightnessControl = ws_dlg['Basic SettingsGroupBox']
            BrightnessReferenceConrtol=brightnessControl.child_window(title="Brightness Down", control_type="ComboBox")
            if BrightnessReferenceConrtol.is_enabled():
                BrightnessReferenceConrtol.set_focus()
                BrightnessReferenceConrtol.invoke()
                if BrightnessReference == 'cameraa':
                    BrightnessReferenceConrtol.child_window(title="Camera A", control_type="ListItem").click_input()
                elif BrightnessReference == 'camerab':
                    BrightnessReferenceConrtol.child_window(title="Camera B", control_type="ListItem").click_input()
                elif BrightnessReference == 'camerac':
                    BrightnessReferenceConrtol.child_window(title="Camera C", control_type="ListItem").click_input()
                elif BrightnessReference == 'camerad':
                    BrightnessReferenceConrtol.child_window(title="Camera D", control_type="ListItem").click_input()
                else:
                    logger.error('Parameter error! The optional parameter values of brightness_reference are "CameraA","CameraB","CameraC","CameraD",')

                time.sleep(1)
            else:
                logger.error('Current brightness_reference ComboBoxControl is in a gray state, and you can not operate it.')

            common_control.scroll_controll(direction='up')

    def start_stitch(self):
        ws_dlg = self.get_ws_dlg()
        if ws_dlg != None:
            startControl=ws_dlg.child_window(title="Start", control_type="Button")
            startControl.click()
            time.sleep(1)

    def reset(self):
        ws_dlg = self.get_ws_dlg()
        if ws_dlg != None:
            common_control.scroll_controll(direction='down')
            resetBotton=ws_dlg.child_window(title="Reset", control_type="Button")
            resetBotton.wait(wait_for='ready',timeout=60)
            resetBotton.click()
            time.sleep(1)
            common_control.scroll_controll(direction='up')

    def advance_options(self):
        ws_dlg = self.get_ws_dlg()
        if ws_dlg != None:
            common_control.scroll_controll(direction='down')
            advanceOptionsBotton=ws_dlg.child_window(title="Advance Options", control_type="Button")
            advanceOptionsBotton.wait('ready',timeout=60)
            advanceOptionsBotton.click()
            time.sleep(1)
            common_control.scroll_controll(direction='up')

    def stitch_preview(self,stitchPreviewImagePath):
        ws_dlg = self.get_ws_dlg()
        if ws_dlg != None:
            FramePreviewCustom2 = ws_dlg['Frame PreviewCustom2']
            stitchPreviewBotton = FramePreviewCustom2.child_window(title="Stitching Preview", control_type="Button")
            stitchPreviewBotton.click()
            time.sleep(1)
            FramePreviewCustom3 = Control(searchDepth=0x0000000B, ControlType=ControlType.CustomControl,Name='Frame Preview',foundIndex=3)

            stitchPreviewImage= Control(ControlType=ControlType.ImageControl,searchFromControl=FramePreviewCustom3)
            if WaitForExist(stitchPreviewImage,60):
                logger.info('stitch preview successful!')
                if not os.path.exists(stitchPreviewImagePath):
                    os.makedirs(stitchPreviewImagePath)
                now_time = time.strftime('%Y-%m-%d-%H-%M-%S-')
                stitchPreviewImagePath=os.path.join(stitchPreviewImagePath,now_time+'StitchPrevImg.png')
                stitchPreviewImage.CaptureToImage(stitchPreviewImagePath)
            else:
                logger.info("stitch preview image does not exist after 60 seconds")


class k1pro_stitch_window_page(object):
    """使用该类的方法需要先转到cameraModel=k1pro的stitch界面"""
    def __init__(self):
        self.app = Application(backend='uia').connect(path=TEST_APP_PATH)

    def get_k1pro_ws_dlg(self):
        stitch_window_dlg=Control( ClassName='Qt5QWindowIcon',ControlType=ControlType.WindowControl,searchDepth=0x01)
        if WaitForExist(stitch_window_dlg,60):
            k1_ws_dlg = self.app.window(class_name='Qt5QWindowIcon', )
        else:
            k1_ws_dlg=None
            logger.error('k1pro stitch window NotFoundError')
        return k1_ws_dlg

    def k1pro_input_config_file(self,configPath):
        currentCameraModelValue = current_value.get_corrent_cameraModelValue()
        k1pro_ws_dlg = self.get_k1pro_ws_dlg()
        if k1pro_ws_dlg != None:
            if currentCameraModelValue == 'K1 Pro':
                CameraTypeCustom3 = k1pro_ws_dlg['Camera TypeCustom3']
                inputConfigurationFileControl = CameraTypeCustom3.Edit2
                inputConfigurationFileControl.invoke()
                # ctrl+A
                inputConfigurationFileControl.type_keys('^a^c')
                inputConfigurationFileControl.type_keys(configPath)
                inputConfigurationFileControl.type_keys('{VK_RETURN}')
                time.sleep(1)
                common_control.ok_enter_botton()
                common_control.ok_enter_botton()
            else:
                logger.error('cameral mode %s does not contain the control:k1pro_input_config_file...',currentCameraModelValue)

    def k1pro_input_file_directory(self,inputFilePath):
        currentCameraModelValue = current_value.get_corrent_cameraModelValue()
        k1pro_ws_dlg = self.get_k1pro_ws_dlg()
        if k1pro_ws_dlg != None:
            if currentCameraModelValue == 'K1 Pro':
                InputCustom1 = k1pro_ws_dlg['InputCustom1']
                inputFileDirectoryEdit = InputCustom1.Edit3
                inputFileDirectoryEdit.invoke()
                # ctrl+A
                inputFileDirectoryEdit.type_keys('^a^c')
                inputFileDirectoryEdit.type_keys(inputFilePath)
                inputFileDirectoryEdit.type_keys('{VK_RETURN}')
                time.sleep(1)
                common_control.ok_enter_botton()
            else:
                logger.error('k1pro_input_file_directory method is only applicable to k1pro!')

    def k1pro_stitch_frame(self,startFrame,endFrame):
        currentCameraModelValue = current_value.get_corrent_cameraModelValue()
        k1pro_ws_dlg = self.get_k1pro_ws_dlg()

        if startFrame <= endFrame:
            if k1pro_ws_dlg != None:
                if currentCameraModelValue == 'K1 Pro':
                    InputCustom2 = k1pro_ws_dlg['InputCustom2']
                    startFrameEdit = InputCustom2.Edit1
                    endFrameEdit = InputCustom2.Edit2
                    startFrameEdit.invoke()
                    # ctrl+A
                    startFrameEdit.type_keys('^a^c')
                    startFrameEdit.type_keys(startFrame)
                    startFrameEdit.type_keys('{VK_RETURN}')
                    time.sleep(2)
                    endFrameEdit.invoke()
                    endFrameEdit.type_keys('^a^c')
                    endFrameEdit.type_keys(endFrame)
                    endFrameEdit.type_keys('{VK_RETURN}')
                    time.sleep(2)
                else:
                    logger.error(' k1pro_stitch_frame method is only applicable to k1pro!')
        else:
            logger.error('startFrame should not greater than endFrame ')

    def k1pro_destination_directory(self,outputPath):
        currentCameraModelValue = current_value.get_corrent_cameraModelValue()
        k1pro_ws_dlg = self.get_k1pro_ws_dlg()
        if k1pro_ws_dlg != None:
            if currentCameraModelValue == 'K1 Pro':
                OutputCustom1=k1pro_ws_dlg['OutputCustom0']
                destinationDirectoryEdit = OutputCustom1.Edit6
                destinationDirectoryEdit.invoke()
                destinationDirectoryEdit.type_keys('^a^c')
                destinationDirectoryEdit.type_keys(outputPath)
                destinationDirectoryEdit.type_keys('{VK_RETURN}')
                time.sleep(2)
                common_control.ok_enter_botton()
            else:
                logger.error('k1pro_destination_directory method is only applicable to k1pro!')

    def k1pro_output_resolution(self,outputResolution='1280'):
        currentCameraModelValue = current_value.get_corrent_cameraModelValue()
        k1pro_ws_dlg = self.get_k1pro_ws_dlg()
        if k1pro_ws_dlg != None:
            outputResolution = str(outputResolution)
            currentOutputTypeValue = Control(name=" Down", ControlType=ControlType.ComboBoxControl,
                                             foundIndex=3).AccessibleCurrentValue()
            if currentCameraModelValue == 'K1 Pro':
                OutputCustom2 = k1pro_ws_dlg['OutputCustom2']
                outputResolutionControl = OutputCustom2.DownComboBox2
                if outputResolutionControl.is_enabled():
                    outputResolutionControl.invoke()
                    try:
                        if outputResolution == '1024':
                            outputResolutionControl.child_window(title="1024", control_type="ListItem").click_input()
                        elif outputResolution == '1280':
                            outputResolutionControl.child_window(title="1280", control_type="ListItem").click_input()
                        elif outputResolution == '1440':
                            outputResolutionControl.child_window(title="1440", control_type="ListItem").click_input()
                        elif outputResolution == '2120':
                            outputResolutionControl.child_window(title="2120", control_type="ListItem").click_input()
                        elif outputResolution == '2048':
                            outputResolutionControl.child_window(title="2048", control_type="ListItem").click_input()
                        elif outputResolution == '2880':
                            outputResolutionControl.child_window(title="2880", control_type="ListItem").click_input()
                        elif outputResolution == '3072':
                            outputResolutionControl.child_window(title="3072", control_type="ListItem").click_input()
                        else:
                            logger.error('Parameter error! The optional parameter values of k1pro_output_resolution are 1024,1280,1440,2120,2048,2880,3072')
                        time.sleep(1)
                    except Exception as e:
                        logger.error('while OutputType = %s, Current input resolution video does not contain the output resolution: %s ',currentOutputTypeValue,outputResolution)
                else:
                    logger.error('Current k1pro_output_resolution ComboBoxControl is in a gray state, and you can not operate it.')

            else:
                logger.error('k1pro_output_resolution method is only applicable to k1pro!')

    def k1pro_output_type(self,outputType='equi'):
        currentCameraModelValue = current_value.get_corrent_cameraModelValue()
        k1pro_ws_dlg = self.get_k1pro_ws_dlg()
        if k1pro_ws_dlg != None:
            if currentCameraModelValue == 'K1 Pro':
                outputType = outputType.lower()
                OutputCustom3 = k1pro_ws_dlg['OutputCustom3']
                outputTypeControl = OutputCustom3.DownComboBox3
                outputTypeControl.invoke()
                if outputType == 'equi':
                    outputTypeControl.child_window(title="VR180(Equi)", control_type="ListItem").click_input()
                elif outputType == 'mesh':
                    outputTypeControl.child_window(title="VR180(Mesh)", control_type="ListItem").click_input()
                elif outputType == 'png':
                    outputTypeControl.child_window(title="PNG", control_type="ListItem").click_input()
                else:
                    logger.error('Parameter error! The optional parameter values of k1pro_output_type are "equi","mesh","png",')
                time.sleep(1)
            else:
                logger.error('k1pro_output_type method is only applicable to k1pro!')

    def k1pro_layout(self,layout='left_right'):
        currentCameraModelValue = current_value.get_corrent_cameraModelValue()
        k1pro_ws_dlg = self.get_k1pro_ws_dlg()
        if k1pro_ws_dlg != None:
            if currentCameraModelValue == 'K1 Pro':
                layout = layout.lower()
                OutputCustom4 = k1pro_ws_dlg['OutputCustom4']
                layoutControl = OutputCustom4.DownComboBox4
                layoutControl.invoke()
                if layout == 'left_right':
                    layoutControl.child_window(title="LEFT_RIGHT", control_type="ListItem").click_input()
                elif layout == 'top_bottom':
                    layoutControl.child_window(title="TOP_BOTTOM", control_type="ListItem").click_input()
                else:
                    logger.error(
                        'Parameter error! The optional parameter values of k1pro_layout are "left_right","top_bottom",')
                time.sleep(1)
            else:
                logger.error('k1pro_layout method is only applicable to k1pro!')

    def k1pro_codec_type(self,codecType='h264'):
        currentCameraModelValue = current_value.get_corrent_cameraModelValue()
        k1pro_ws_dlg = self.get_k1pro_ws_dlg()
        if k1pro_ws_dlg != None:
            if currentCameraModelValue == 'K1 Pro':
                codecType = codecType.lower()
                currentOutputTypeValue = Control( name=" Down",ControlType=ControlType.ComboBoxControl,foundIndex=3).AccessibleCurrentValue()
                OutputValueList=['VR180(Equi)','VR180(Mesh)']
                if currentOutputTypeValue in OutputValueList:
                    BasicSettingsCustom0 = k1pro_ws_dlg['Basic SettingsCustom0']
                    codecTypeControl = BasicSettingsCustom0.DownComboBox5
                    codecTypeControl.invoke()
                    if codecType == 'h264':
                        codecTypeControl.child_window(title="H264", control_type="ListItem").click_input()
                    elif codecType == 'h265':
                        codecTypeControl.child_window(title="H265", control_type="ListItem").click_input()
                    else:
                        logger.error('Parameter error! The optional parameter values of k1pro_codec_type are "h264","h265",')
                    time.sleep(1)
                else:
                    logger.error('while outputType = %s ,k1pro_codec_type contorl not exist!',currentOutputTypeValue)
            else:
                logger.error('k1pro_codec_type method is only applicable to k1pro!')

    def k1pro_quality(self,Quality='medium'):
        currentCameraModelValue = current_value.get_corrent_cameraModelValue()
        k1pro_ws_dlg = self.get_k1pro_ws_dlg()
        if k1pro_ws_dlg != None:
            if currentCameraModelValue == 'K1 Pro':
                Quality = Quality.lower()
                currentOutputTypeValue = Control(name=" Down", ControlType=ControlType.ComboBoxControl,
                                                 foundIndex=3).AccessibleCurrentValue()
                OutputValueList = ['VR180(Equi)', 'VR180(Mesh)']
                if currentOutputTypeValue in OutputValueList:
                    currentCodecTypeValue = Control(name=" Down", ControlType=ControlType.ComboBoxControl,
                                                 foundIndex=5).AccessibleCurrentValue()
                    currentOutputResolutionValue = Control(name=" Down", ControlType=ControlType.ComboBoxControl,
                                                 foundIndex=2).AccessibleCurrentValue()
                    BasicSettingsCustom2 = k1pro_ws_dlg['Basic SettingsCustom2']
                    qualityControl = BasicSettingsCustom2.DownComboBox6
                    qualityControl.invoke()
                    try:
                        if Quality == 'high':
                            qualityControl.child_window(title="High(VBR)", control_type="ListItem").click_input()
                        elif Quality == 'medium':
                            qualityControl.child_window(title="Medium(VBR)", control_type="ListItem").click_input()
                        elif Quality == 'low':
                            qualityControl.child_window(title="Low(VBR)", control_type="ListItem").click_input()
                        elif Quality == '10m':
                            qualityControl.child_window(title="10M(CBR)", control_type="ListItem").click_input()
                        elif Quality == '20m':
                            qualityControl.child_window(title="20M(CBR)", control_type="ListItem").click_input()
                        elif Quality == '30m':
                            qualityControl.child_window(title="30M(CBR)", control_type="ListItem").click_input()
                        elif Quality == '40m':
                            qualityControl.child_window(title="40M(CBR)", control_type="ListItem").click_input()
                        elif Quality == '50m':
                            qualityControl.child_window(title="50M(CBR)", control_type="ListItem").click_input()
                        elif Quality == '60m':
                            qualityControl.child_window(title="60M(CBR)", control_type="ListItem").click_input()
                        elif Quality == '80m':
                            qualityControl.child_window(title="80M(CBR)", control_type="ListItem").click_input()
                        elif Quality == '100m':
                            qualityControl.child_window(title="100M(CBR)", control_type="ListItem").click_input()
                        elif Quality == '120m':
                            qualityControl.child_window(title="120M(CBR)", control_type="ListItem").click_input()
                        elif Quality == '140m':
                            qualityControl.child_window(title="140M(CBR)", control_type="ListItem").click_input()
                        elif Quality == '160m':
                            qualityControl.child_window(title="160M(CBR)", control_type="ListItem").click_input()
                        elif Quality == '180m':
                            qualityControl.child_window(title="180M(CBR)", control_type="ListItem").click_input()
                        elif Quality == '200m':
                            qualityControl.child_window(title="200M(CBR)", control_type="ListItem").click_input()
                        elif Quality == '220m':
                            qualityControl.child_window(title="220M(CBR)", control_type="ListItem").click_input()
                        else:
                            logger.error(
                                'Parameter error! The optional parameter values of k1pro_quality are "high","medium","low","10m","20m","30m"'
                                ',"40m","50m","60m","80m","100m","120m","140m","160m","180m","200m","220m"')
                        time.sleep(1)
                    except Exception as e:
                        logger.error('while OutputResolution = %s ,CodecType = %s ,the ListItem = %s of k1pro_quality ListBox not exist! ',currentOutputResolutionValue,currentCodecTypeValue,Quality)
                else:
                    logger.error('while outputType = %s ,k1pro_quality contorl not exist!', currentOutputTypeValue)
            else:
                logger.error('k1pro_quality method is only applicable to k1pro!')

    def k1pro_stitch_engine(self,stitchEngine='gpu'):
        currentCameraModelValue = current_value.get_corrent_cameraModelValue()
        k1pro_ws_dlg = self.get_k1pro_ws_dlg()
        if k1pro_ws_dlg != None:
            if currentCameraModelValue == 'K1 Pro':
                stitchEngine = stitchEngine.lower()
                currentOutputTypeValue = Control(name=" Down", ControlType=ControlType.ComboBoxControl,
                                                 foundIndex=3).AccessibleCurrentValue()
                OutputValueList = ['VR180(Equi)', 'VR180(Mesh)']
                if currentOutputTypeValue in OutputValueList:
                    BasicSettingsCustom3 = k1pro_ws_dlg['Basic SettingsCustom3']
                    stitchEngineControl = BasicSettingsCustom3.DownComboBox7
                else:
                    BasicSettingsCustom0 = k1pro_ws_dlg['Basic SettingsCustom0']
                    stitchEngineControl = BasicSettingsCustom0.DownComboBox5
                stitchEngineControl.invoke()
                try:
                    if stitchEngine == 'cpu':
                        stitchEngineControl.child_window(title="CPU", control_type="ListItem").click_input()
                    elif stitchEngine == 'gpu':
                        stitchEngineControl.child_window(title="GPU", control_type="ListItem").click_input()
                    else:
                        logger.error('Parameter error! The optional parameter values of k1pro_stitch_engine are "cpu","gpu",')
                except Exception as e:
                    logger.error('sorroy, your computer does not contain stitch engine %s ',stitchEngine)
            else:
                logger.error('k1pro_stitch_engine method is only applicable to k1pro!')

    def k1pro_switch_left_right(self,status='on'):
        currentCameraModelValue = current_value.get_corrent_cameraModelValue()
        k1pro_ws_dlg = self.get_k1pro_ws_dlg()
        if k1pro_ws_dlg != None:
            if currentCameraModelValue == 'K1 Pro':
                status = status.lower()
                currentOutputTypeValue = Control(name=" Down", ControlType=ControlType.ComboBoxControl,
                                                 foundIndex=3).AccessibleCurrentValue()
                OutputValueList = ['VR180(Equi)', 'VR180(Mesh)']
                common_control.scroll_controll(direction='down')
                if currentOutputTypeValue in OutputValueList:
                    BasicSettingsCustom4 = k1pro_ws_dlg['Basic SettingsCustom4']
                    switchLeftRightControl = BasicSettingsCustom4.DownComboBox8
                else:
                    BasicSettingsCustom2 = k1pro_ws_dlg['Basic SettingsCustom2']
                    switchLeftRightControl = BasicSettingsCustom2.DownComboBox6
                switchLeftRightControl.invoke()
                if status == 'on':
                    switchLeftRightControl.child_window(title="On", control_type="ListItem").click_input()
                elif status == 'off':
                    switchLeftRightControl.child_window(title="Off", control_type="ListItem").click_input()
                else:
                    logger.error('Parameter error! The status value of k1pro_switch_left_right can be any of "on","off",')
                time.sleep(1)
                common_control.scroll_controll(direction='up')
            else:
                logger.error('k1pro_switch_left_right method is only applicable to k1pro!')

    def k1pro_smart_align(self,status='on'):
        currentCameraModelValue = current_value.get_corrent_cameraModelValue()
        k1pro_ws_dlg = self.get_k1pro_ws_dlg()
        if k1pro_ws_dlg != None:
            if currentCameraModelValue == 'K1 Pro':
                status = status.lower()
                currentOutputTypeValue = Control(name=" Down", ControlType=ControlType.ComboBoxControl,
                                                 foundIndex=3).AccessibleCurrentValue()
                OutputValueList = ['VR180(Equi)', 'VR180(Mesh)']
                common_control.scroll_controll(direction='down')
                if currentOutputTypeValue in OutputValueList:
                    BasicSettingsCustom5 = k1pro_ws_dlg['Basic SettingsCustom5']
                    smartAlignControl = BasicSettingsCustom5.DownComboBox9
                else:
                    BasicSettingsCustom3 = k1pro_ws_dlg['Basic SettingsCustom3']
                    smartAlignControl = BasicSettingsCustom3.DownComboBox6
                smartAlignControl.invoke()
                if status == 'on':
                    smartAlignControl.child_window(title="On", control_type="ListItem").click_input()
                elif status == 'off':
                    smartAlignControl.child_window(title="Off", control_type="ListItem").click_input()
                else:
                    logger.error('Parameter error! The status value of k1pro_smart_align can be any of "on","off",')
                time.sleep(1)
                common_control.scroll_controll(direction='up')
            else:
                logger.error('k1pro_smart_align method is only applicable to k1pro!')


class encode_pane_page(object):
    """使用该类的方法需要先转到encode界面,可使用stitch_window_page类下的choose_encode_tab()方法，转到encode界面"""
    def __init__(self):
        self.app = Application(backend='uia').connect(path=TEST_APP_PATH)
        self.ws_dlg = self.app.window(class_name='Qt5QWindowIcon', )

    def get_encode_dlg(self):
        encodeDlgControl = Control(searchDepth=0x00000004, ControlType=ControlType.PaneControl)
        if WaitForExist(encodeDlgControl,15):
           encode_dlg =  self.ws_dlg.child_window(control_type = 'Pane')
        else:
            logger.error('encode window NotFoundError')
            encode_dlg=None
        return encode_dlg

    def png_file_directory(self,encodeInputPath):
        if not os.path.exists(encodeInputPath):
            logger.error('The input path does not exist.')
        encode_dlg = self.get_encode_dlg()
        if encode_dlg != None:
            BasicSettingsCustom1 = encode_dlg.Custom5
            pngFileDirectoryControl = BasicSettingsCustom1.Edit1
            pngFileDirectoryControl.invoke()
            pngFileDirectoryControl.type_keys('^a^c')
            pngFileDirectoryControl.type_keys(encodeInputPath, with_spaces=True)
            pngFileDirectoryControl.type_keys('{VK_RETURN}')
            time.sleep(1)

    def video_file_directory(self,encodeOutputPath):
        if not os.path.exists(encodeOutputPath):
            os.makedirs(encodeOutputPath)
        encode_dlg = self.get_encode_dlg()
        if encode_dlg != None:
            BasicSettingsCustom2 =encode_dlg.Custom7
            videoFileDirectoryControl = BasicSettingsCustom2.Edit2
            videoFileDirectoryControl.invoke()
            videoFileDirectoryControl.type_keys('^a^c')
            videoFileDirectoryControl.type_keys(encodeOutputPath, with_spaces=True)
            videoFileDirectoryControl.type_keys('{VK_RETURN}')
            time.sleep(1)

    def encode_output_type(self,outputType):
        outputType = outputType.lower()
        encode_dlg = self.get_encode_dlg()
        if encode_dlg != None:
            BasicSettingsCustom2 = encode_dlg.Custom7
            encodeOutputTypeControl = BasicSettingsCustom2.DownComboBox1
            encodeOutputTypeControl.invoke()
            if outputType == 'mov':
                encodeOutputTypeControl.child_window(title="MOV", control_type="ListItem").click_input()
            elif outputType == 'mp4':
                encodeOutputTypeControl.child_window(title="MP4", control_type="ListItem").click_input()
            else:
                logger.error('Parameter error! The optional parameter values of encode_output_type are "mov","mp4",')

            time.sleep(1)

    def video_start_point(self,videoStartPoint=0):
        videoStartPoint = str(videoStartPoint)
        encode_dlg = self.get_encode_dlg()
        if encode_dlg != None:
            OptionalSettingsCustom1 = encode_dlg.Custom9
            videoStartPointControl = OptionalSettingsCustom1.Edit3
            if  videoStartPoint.isdigit():
                videoStartPointControl.invoke()
                videoStartPointControl.type_keys('^a^c')
                videoStartPointControl.type_keys(videoStartPoint)
                videoStartPointControl.type_keys('{VK_RETURN}')
                time.sleep(1)
            else:
                logger.error('Input parameter of video_start_point is integer.')

    def encode_duration(self,duration):
        duration = str(duration)
        encode_dlg = self.get_encode_dlg()
        if encode_dlg != None:
            OptionalSettingsCustom1 = encode_dlg.Custom9
            durationControl = OptionalSettingsCustom1.DurationEdit
            if duration.isdigit():
                durationControl.invoke()
                durationControl.type_keys('^a^c')
                durationControl.type_keys(duration)
                durationControl.type_keys('{VK_RETURN}')
                time.sleep(1)
            else:
                logger.error('Input parameter of duration is integer.')

    def encode_frame_rate(self,frameRate='29.97'):
        frameRate = str(frameRate)
        encode_dlg = self.get_encode_dlg()
        if encode_dlg != None:
            frameRateControl = encode_dlg.DownComboBox3
            if frameRateControl.is_enabled():
                frameRateControl.invoke()
                if frameRate == '29.97':
                    frameRateControl.child_window(title="29.97", control_type="ListItem").click_input()
                elif frameRate == '59.94':
                    frameRateControl.child_window(title="59.94", control_type="ListItem").click_input()
                elif frameRate == '25':
                    frameRateControl.child_window(title="25", control_type="ListItem").click_input()
                elif frameRate == '50':
                    frameRateControl.child_window(title="50", control_type="ListItem").click_input()
                else:
                    logger.error('Parameter error! The optional parameter values of frameRate are "29.97","59.94","25","50"')
                time.sleep(1)
            else:
                logger.error('Current frame_rate ComboBoxControl is in a gray state, and you can not operate it.')

    def encode_quality(self,encodeQuality='medium'):
        encodeQuality =encodeQuality.lower()
        encode_dlg = self.get_encode_dlg()
        if encode_dlg != None:
            encodeQualityControl = encode_dlg.DownComboBox4
            if encodeQualityControl.is_enabled():
                encodeQualityControl.invoke()
                if encodeQuality == 'high':
                    encodeQualityControl.child_window(title="High(VBR)", control_type="ListItem").click_input()
                elif encodeQuality == 'medium':
                    encodeQualityControl.child_window(title="Medium(VBR)", control_type="ListItem").click_input()
                elif encodeQuality == 'low':
                    encodeQualityControl.child_window(title="Low(VBR)", control_type="ListItem").click_input()
                elif encodeQuality == '120m':
                    encodeQualityControl.child_window(title="120M(CBR)", control_type="ListItem").click_input()
                elif encodeQuality == '80m':
                    encodeQualityControl.child_window(title="80M(CBR)", control_type="ListItem").click_input()
                elif encodeQuality == '50m':
                    encodeQualityControl.child_window(title="50M(CBR)", control_type="ListItem").click_input()
                else:
                    logger.error('Parameter error! The optional parameter values of encode_quality are "high","medium","low","120m","80m","50m"')
                time.sleep(1)

            else:
                logger.error('Current encode_quality ComboBoxControl is in a gray state, and you can not operate it.')

    def encode_codec_type(self,codecType):
        codecType=codecType.lower()
        encode_dlg = self.get_encode_dlg()
        if encode_dlg != None:
            encodeCodecTypeControl = encode_dlg.DownComboBox5
            if encodeCodecTypeControl.is_enabled():
                encodeCodecTypeControl.invoke()
                if codecType == 'h264':
                    encodeCodecTypeControl.child_window(title="H264", control_type="ListItem").click_input()
                elif codecType == 'h265':
                    encodeCodecTypeControl.child_window(title="H265", control_type="ListItem").click_input()
                else:
                    logger.error( 'Parameter error! The optional parameter values of encode_codec_type are "h264","h265",')
                time.sleep(1)

            else:
                 logger.error('Current encode_codec_type ComboBoxControl is in a gray state, and you can not operate it.')

    def encode_stereo_mode(self,stereoMode):
        stereoMode=stereoMode.lower()
        encode_dlg = self.get_encode_dlg()
        if encode_dlg != None:
            encodeStereoModeControl = encode_dlg.DownComboBox6
            if encodeStereoModeControl.is_enabled():
                encodeStereoModeControl.invoke()
                if stereoMode == 'mono':
                    encodeStereoModeControl.child_window(title="MONO", control_type="ListItem").click_input()
                elif stereoMode == 'left_right':
                    encodeStereoModeControl.child_window(title="LEFT_RIGHT", control_type="ListItem").click_input()
                elif stereoMode == 'top_bottom':
                    encodeStereoModeControl.child_window(title="TOP_BOTTOM", control_type="ListItem").click_input()
                else:
                    logger.error('Parameter error! The optional parameter values of encode_stereo_mode are "mono","left_right","top_bottom"')
                time.sleep(1)
            else:
                logger.error('Current encode_stereo_mode ComboBoxControl is in a gray state, and you can not operate it.')

    def projection_type(self,projectionType):
        projectionType = projectionType.lower()
        encode_dlg = self.get_encode_dlg()
        if encode_dlg != None:
            projectionTypeControl = encode_dlg.DownComboBox7
            if projectionType == 'equirectangular':
                projectionTypeControl.child_window(title="Equirectangular", control_type="ListItem").click_input()
            elif projectionType == 'vr180(equi)':
                projectionTypeControl.child_window(title="VR180(Equi)", control_type="ListItem").click_input()
            else:
                logger.error('Parameter error! The optional parameter values of projection_type are "Equirectangular","VR180(Equi)",')
            time.sleep(1)

    def sound_track_enable(self,status=0):
        """The toggle state is represented by an integer
                    status=0 - unchecked
                    status=1 - checked
        """
        status = str(status)
        encode_dlg = self.get_encode_dlg()
        if encode_dlg != None:
            soundTrackEnableControl = encode_dlg.EnableCheckBox
            soundTrackEnableControl.set_focus()
            correntStatus = soundTrackEnableControl.get_toggle_state()
            print(correntStatus)
            if status == '1':
                if correntStatus == 1:
                    pass
                else:
                    soundTrackEnableControl.toggle()
            elif status == '0':
                if correntStatus == 1:
                    soundTrackEnableControl.toggle()
                else:
                    pass
            else:
                logger.error(
                    'Parameter error! the status of checkbox is represented by an integer，status=0:unchecked,status=1:checked')
            time.sleep(1)

    def add_sound_track(self,soundTrackPath):
        encode_dlg = self.get_encode_dlg()
        if encode_dlg != None:
            addSoundTrackEdit = encode_dlg.Edit5
            if addSoundTrackEdit.is_enabled():
                addSoundTrackEdit.invoke()
                addSoundTrackEdit.type_keys('^a^c')
                addSoundTrackEdit.type_keys(soundTrackPath, with_spaces=True)
                addSoundTrackEdit.type_keys('{VK_RETURN}')
                time.sleep(2)
            else:
                logger.error('Current add_sound_track EditControl is in a gray state, and you can not operate it.')


class advance_options_pane_page(object):
    """使用该类的方法需要advance_options对话框处于可视状态，可使用stitch_window_page类下的advance_options()方法，弹出advance_options窗口"""
    def __init__(self):
        self.app = Application(backend='uia').connect(path=TEST_APP_PATH)
        self.ws_dlg = self.app.window(class_name='Qt5QWindowIcon', )

    def get_advance_option_dlg(self):
        advance_options_dlg = Control(ClassName='Qt5QWindow', ControlType=ControlType.PaneControl)
        if WaitForExist(advance_options_dlg,15):
           advance_dlg =  self.ws_dlg.child_window(class_name='Qt5QWindow')
        else:
            logger.error('advance options window NotFoundError')
            advance_dlg=None
        return advance_dlg

    def scan_before_stitch(self,status='on'):
        status=status.lower()
        advance_dlg = self.get_advance_option_dlg()
        if advance_dlg != None:
            ScanBeforeStitchControl = advance_dlg.Custom2.DownComboBox1
            ScanBeforeStitchControl.invoke()
            if status == 'on':
                ScanBeforeStitchControl.child_window(title="On", control_type="ListItem").click_input()
            elif status == 'off':
                ScanBeforeStitchControl.child_window(title="Off", control_type="ListItem").click_input()
            else:
                logger.error('Parameter error! status of scan_before_stitch can be any of "on","off",')

            time.sleep(1)

    def advance_option_flow(self,status='on'):
        status = status.lower()
        advance_dlg = self.get_advance_option_dlg()
        stitchTypevalue = current_value.get_corrent_stitchTypeValue()
        stitchTypeList1 = ['Optical Flow - Full','Optical Flow - Hybrid','Stereo']
        if advance_dlg != None:
            if stitchTypevalue in stitchTypeList1:
                AdvanceOptionFlowControl = advance_dlg.Custom3.DownComboBox2
                AdvanceOptionFlowControl.invoke()
                if status == 'on':
                    AdvanceOptionFlowControl.child_window(title="On", control_type="ListItem").click_input()
                elif status == 'off':
                    AdvanceOptionFlowControl.child_window(title="Off", control_type="ListItem").click_input()
                else:
                    logger.error(
                        'Parameter error! status of advance_option_flow can be any of "on","off",')
            else:
                logger.error('Current dialog does not contain advance option flow control')

            time.sleep(1)

    def optical_flow_mode(self,opticalFlowMode='smart'):
        opticalFlowMode=opticalFlowMode.lower()
        advance_dlg = self.get_advance_option_dlg()
        stitchTypevalue = current_value.get_corrent_stitchTypeValue()
        stitchTypeList1 = ['Optical Flow - Full', 'Optical Flow - Hybrid', 'Stereo']
        if advance_dlg != None:
            if stitchTypevalue in stitchTypeList1:
                OptionFlowModeControl = advance_dlg.Custom4.DownComboBox3
                OptionFlowModeControl.invoke()
                if opticalFlowMode == 'smart':
                    OptionFlowModeControl.child_window(title="Smart", control_type="ListItem").click_input()
                elif opticalFlowMode == 'normal':
                    OptionFlowModeControl.child_window(title="Normal", control_type="ListItem").click_input()
                else:
                    logger.error('Parameter error! The optional parameter values of optical_flow_mode are "Smart","Normal",')
            else:
                logger.error('Current dialog does not contain optical flow mode control')

            time.sleep(1)

    def sharpness_compensation(self,sharpnessCompensation='normal'):
        sharpnessCompensation = sharpnessCompensation.lower()
        advance_dlg = self.get_advance_option_dlg()
        stitchTypevalue = current_value.get_corrent_stitchTypeValue()
        stitchTypeList1 = ['Optical Flow - Full', 'Optical Flow - Hybrid', 'Stereo']
        if advance_dlg != None:
            if stitchTypevalue in stitchTypeList1:
                SharpnessCompensationControl = advance_dlg.Custom5.DownComboBox4
            else:
                SharpnessCompensationControl = advance_dlg.Custom3.DownComboBox2
            SharpnessCompensationControl.invoke()
            if sharpnessCompensation == 'high':
                SharpnessCompensationControl.child_window(title="High", control_type="ListItem").click_input()
            elif sharpnessCompensation == 'normal':
                SharpnessCompensationControl.child_window(title="Normal", control_type="ListItem").click_input()
            elif sharpnessCompensation == 'low':
                SharpnessCompensationControl.child_window(title="Low", control_type="ListItem").click_input()
            else:
                logger.error('Parameter error! The optional parameter values of sharpness_compensation are "High","Normal","Low",')
            time.sleep(1)

    def adjust_point_of_interest(self,AdjustPointOfInterestvalue=0):
        advance_dlg = self.get_advance_option_dlg()
        stitchTypevalue = current_value.get_corrent_stitchTypeValue()
        stitchTypeList1 = ['Optical Flow - Full', 'Optical Flow - Hybrid', 'Stereo']
        if advance_dlg != None:
            if stitchTypevalue in stitchTypeList1:
                AdjustPointOfInterest = advance_dlg.Custom6.UpDown
            else:
                AdjustPointOfInterest = advance_dlg.Custom4.UpDown
            # AdjustPointOfInterestControl = Control(searchDepth=0x00000005, ControlType=ControlType.SpinnerControl,foundIndex=1)
            # print('uiautomation:',AdjustPointOfInterestControl.IsEnabled)
            #Determine whether the control state is ash
            if AdjustPointOfInterest.is_enabled():
                AdjustPointOfInterest.invoke()
                list = range(0,360)
                if AdjustPointOfInterestvalue in list:
                    AdjustPointOfInterest.type_keys('^a^c')
                    AdjustPointOfInterest.type_keys(AdjustPointOfInterestvalue)
                else:
                    logger.error('Parameter error! The value of adjust_point_of_interest is an integer from 0 to 359.')
                time.sleep(1)
            else:
                logger.error('Current adjust_point_of_interest control is in a gray state, and you can not operate it.')

    def need_flip(self,status='off'):
        status=status.lower()
        advance_dlg = self.get_advance_option_dlg()
        stitchTypevalue = current_value.get_corrent_stitchTypeValue()
        stitchTypeList1 = ['Optical Flow - Full', 'Optical Flow - Hybrid', 'Stereo']
        if advance_dlg != None:
            if stitchTypevalue in stitchTypeList1:
                needFlipControl = advance_dlg.Custom7.DownComboBox5
            else:
                needFlipControl = advance_dlg.Custom5.DownComboBox3
            needFlipControl.invoke()
            if status == 'off':
                needFlipControl.child_window(title="Off", control_type="ListItem").click_input()
            elif status == 'on':
                needFlipControl.child_window(title="On", control_type="ListItem").click_input()
            else:
                logger.error( 'Parameter error! status of need_flip can be any of "on","off",')
            time.sleep(1)

    def smooth_factor(self,smoothFactor='No'):
        smoothFactor = smoothFactor.lower()
        advance_dlg = self.get_advance_option_dlg()
        stitchTypevalue = current_value.get_corrent_stitchTypeValue()
        stitchTypeList1 = ['Optical Flow - Full', 'Optical Flow - Hybrid', 'Stereo']
        if advance_dlg != None:
            if stitchTypevalue in stitchTypeList1:
                smoothFactorControl = advance_dlg.ComboBox6
            else:
                smoothFactorControl = advance_dlg.ComboBox4
            smoothFactorControl.invoke()
            if smoothFactor == 'ultra high':
                smoothFactorControl.child_window(title="Ultra high", control_type="ListItem").click_input()
            elif smoothFactor == 'high':
                smoothFactorControl.child_window(title="High", control_type="ListItem").click_input()
            elif smoothFactor == 'normal':
                smoothFactorControl.child_window(title="Normal", control_type="ListItem").click_input()
            elif smoothFactor == 'low':
                smoothFactorControl.child_window(title="Low", control_type="ListItem").click_input()
            elif smoothFactor == 'ultra low':
                smoothFactorControl.child_window(title="Ultra Low", control_type="ListItem").click_input()
            elif smoothFactor == 'no':
                smoothFactorControl.child_window(title="No", control_type="ListItem").click_input()
            else:
                logger.error('Parameter error!  smooth_factor value can be any of "ultra high","high","normal","low","ultra low","no"')
            time.sleep(1)

    def zenith_nadir_feather(self,status='off'):
        status=status.lower()
        advance_dlg = self.get_advance_option_dlg()
        stitchTypevalue = current_value.get_corrent_stitchTypeValue()
        stitchTypeList1 = ['Optical Flow - Full', 'Optical Flow - Hybrid', 'Stereo']
        if advance_dlg != None:
            if stitchTypevalue in stitchTypeList1:
                zenithNadirFeatherControl = advance_dlg.ComboBox7
            else:
                zenithNadirFeatherControl = advance_dlg.ComboBox5
            zenithNadirFeatherControl.invoke()
            if status == 'off':
                zenithNadirFeatherControl.child_window(title="Off", control_type="ListItem").click_input()
            elif status == 'on':
                zenithNadirFeatherControl.child_window(title="On", control_type="ListItem").click_input()
            else:
                logger.error( 'Parameter error! status value of zenith_nadir_feather can be any of "on","off",')
            time.sleep(1)

    def mono_top_enable(self,status='off'):
        status = status.lower()
        advance_dlg = self.get_advance_option_dlg()
        stitchTypevalue = current_value.get_corrent_stitchTypeValue()
        stitchTypeList1 = ['Optical Flow - Full', 'Optical Flow - Hybrid', 'Stereo']
        if advance_dlg != None:
            if stitchTypevalue in stitchTypeList1:
                monoTopEnableControl = advance_dlg.Custom8.ComboBox8
            else:
                monoTopEnableControl = advance_dlg.Custom6.ComboBox6

            if monoTopEnableControl.is_enabled():
                monoTopEnableControl.invoke()
                if status == 'off':
                    monoTopEnableControl.child_window(title="Off", control_type="ListItem").click_input()
                elif status == 'on':
                    monoTopEnableControl.child_window(title="On", control_type="ListItem").click_input()
                else:
                    logger.error('Parameter error! status value of mono_top_enable can be any of "on","off",')
                time.sleep(1)
            else:
                logger.error('Current mono_top_enable ComboBoxControl is in a gray state, and you can not operate it. ')

    def mono_top_degree_from_pole(self,monoTopDegreeFromPolevalue=45):
        advance_dlg = self.get_advance_option_dlg()
        stitchTypevalue = current_value.get_corrent_stitchTypeValue()
        stitchTypeList1 = ['Optical Flow - Full', 'Optical Flow - Hybrid', 'Stereo']
        if advance_dlg != None:
            if stitchTypevalue in stitchTypeList1:
                monoTopDegreeFromPoleControl = advance_dlg.Custom9.UpDown
            else:
                monoTopDegreeFromPoleControl = advance_dlg.Custom7.UpDown

            if monoTopDegreeFromPoleControl.is_enabled():
                monoTopDegreeFromPoleControl.invoke()
                list=range(0,60)
                if monoTopDegreeFromPolevalue in list:
                    monoTopDegreeFromPoleControl.type_keys('^a^c')
                    monoTopDegreeFromPoleControl.type_keys(monoTopDegreeFromPolevalue)
                else:
                    logger.error('Parameter error! The value of mono_top_degree_from_pole is an integer from 0 to 60.')
                time.sleep(1)

            else:
                logger.error("Current mono_top_degree_from_pole control is in a gray state, and you can not operate it.")

    def ok_bottom(self):
        advance_dlg = self.get_advance_option_dlg()
        okBottomControl=advance_dlg.child_window(title="Ok Enter", control_type="Button")
        okBottomControl.click()
        time.sleep(1)


class stitching_record_pane_page(object):
    """使用该类方法，需要先点击start按钮(stitch_window_page.start_stitch())，弹出stitching对话框"""
    def __init__(self):
        self.app = Application(backend='uia').connect(path=TEST_APP_PATH)

    def get_stitching_dlg(self):
        stitching_dlg_control = Control(ClassName='Qt5QWindow', ControlType=ControlType.PaneControl)
        if WaitForExist(stitching_dlg_control, 30):
            stitching_dlg = self.app.window(class_name='Qt5QWindow',control_type = 'Pane')
        else:
            logger.error('stitching window NotFoundError')
            stitching_dlg = None
        return stitching_dlg

    def stitching_log(self):
        """Returns the contents of the stitching log and process operation results """
        stitching_dlg = self.get_stitching_dlg()
        if stitching_dlg != None:
            stitching_result = {}
            processsInforControl = Control(Name="Processing ...",ControlType = ControlType.TextControl)
            #processinfor = stitching_dlg.child_window(title="Processing ...", control_type="Text")
            #processinfor.wait_not(wait_for_not = 'exists',timeout=4*60*60)
            if WaitForDisappear(processsInforControl,timeout=4*60*60):
                process_result = stitching_dlg.Static2.window_text()
                stitching_result['process_result'] = process_result
                stitching_log_control = stitching_dlg.Edit
                stitching_log_content = stitching_log_control.get_value()
                stitching_result['stitching_log'] = stitching_log_content
                time.sleep(5)
                videopathwindow = Control(ClassName="CabinetWClass",ControlType = ControlType.WindowControl, searchDepth=1)
                if WaitForExist(videopathwindow,timeout=120):
                    CloseControl = Control(Name="关闭",ControlType = ControlType.ButtonControl)
                    CloseControl.Click()
            else:
                logger.error('stitching process failed !')
            return stitching_result

    def restart_stitch(self):
        stitching_dlg = self.get_stitching_dlg()
        if stitching_dlg != None:
            restartBotton = stitching_dlg.child_window(title="Restart", control_type="Button")
            if restartBotton.is_enabled:
                restartBotton.click()
            else:
                logger.error('"Current restart bottom is in a gray state, and you can not operate it."')

    def close_stitch(self):
        stitching_dlg = self.get_stitching_dlg()
        if stitching_dlg != None:
            closeBotton = stitching_dlg.child_window(title="Close", control_type="Button")
            processsInforControl = Control(Name="Processing ...", ControlType=ControlType.TextControl)
            if WaitForDisappear(processsInforControl, timeout=4 * 60 * 60):
                closeBotton.click()


class StithWindowTest(object):
    def __init__(self,TestOutPutResolution,**kwargs):
        self.kwargs = kwargs
        self.TestOutPutResolution = TestOutPutResolution
        self.TestCassID = self.kwargs['TestCassID']
        self.InputFileDirectory = self.kwargs['input_file_directory']
        self.CameraModel = self.kwargs['camera_model']
        self.CameraID = self.kwargs['camera_id']
        self.StitchType = self.kwargs['stitch_type']
        self.OutputResolution = self.kwargs['output_resolution']
        self.StitchFrame = self.kwargs['stitch_frame']
        self.DestinationDirectory = self.kwargs['destination_directory']
        self.OutpuType = self.kwargs['output_type']
        self.CodecType = self.kwargs['codec_type']
        self.Quality = self.kwargs['quality']
        self.StitchEngine = self.kwargs['stitch_engine']
        self.stitch_window = stitch_window_page()
        self.stitching_pane = stitching_record_pane_page()
        self.TestVideoName = os.path.basename(self.InputFileDirectory)
        self.StitchVideooutputPath = os.path.join(config.stitchOutputPath, self.CameraModel, self.TestVideoName,
                                  self.StitchEngine , self.StitchType,
                                  self.CodecType, self.OutpuType,self.TestOutPutResolution)

    def test_stitch_window(self):
        self.stitch_window.choose_stitch_tab()
        #self.stitch_window.reset()
        self.stitch_window.input_file_directory(inputPath=self.InputFileDirectory)
        self.stitch_window.camera_model(cameraModel=self.CameraModel)
        self.stitch_window.camera_id(self.CameraID)
        stitchframe = self.StitchFrame.split('-')
        self.stitch_window.stitch_frame(stitchframe[0], stitchframe[1])
        self.stitch_window.destination_directory(outputPath=self.StitchVideooutputPath)
        self.stitch_window.output_resolution(self.TestOutPutResolution)
        self.stitch_window.output_type(self.OutpuType)
        self.stitch_window.codec_type(self.CodecType )
        self.stitch_window.quality(self.Quality)
        self.stitch_window.stitch_type(self.StitchType)
        self.stitch_window.stitch_engine(self.StitchEngine)
        self.stitch_window.stitch_preview(self.StitchVideooutputPath)

#============================conmmon functions==========================



# if __name__ == '__main__':
#     #example:
#     app = app(backend='uia')
#     app.run(appPath=TEST_APP_PATH)
#
#     # time.sleep(5)
#     # app.close()
# #     #
# #     # #----------------------class stitch_window_page functions------------------------
#     stitch_window=stitch_window_page()
#     stitch_window.choose_stitch_tab()#转到stitch界面
#     stitch_window.reset()
#     stitch_window.camera_model('v1')
#     stitch_window.camera_id('30390018009')
#     #stitch_window.clear_config()
#     stitch_window.input_type('video')
#     #stitch_window.input_file_directory(r'Z:\customer\V1\2#30390018009')
#     stitch_window.destination_directory(r'C:\Users\wu\Desktop\work8-16')
#     stitch_window.reset()
    #stitch_window.stitch_frame(100,105)
    #stitch_window.destination_directory(r'C:\Users\wu\Desktop\work8-16\s1\15030010001_chuxi\gpu\opticalflow-full\h264\3k(dci)')
    #stitch_window.output_resolution('3k(dci)')
    #stitch_window.output_type('png')
    #stitch_window.multi_process('off')
    #stitch_window.stitch_type('opticalflow-hybrid')
    # stitch_window.stitch_engine('cpu')
    # stitch_window.codec_type('h265')
    # stitch_window.quality('medium')
    #stitch_window.enable_brightness_adjustment(status=1)
    #stitch_window.enable_HDR(status=1)
    #stitch_window.brightness_reference('CameraA')
    # stitch_window.start_stitch()
    #stitch_window.reset()
    #stitch_window.advance_options()
    #stitch_window.stitch_preview()
    #------------------------class k1pro_stitch_window_page functions-------------------------
    # stitch_window=stitch_window_page()
    #stitch_window.camera_model('k1pro')
    #stitch_window.camera_id('24571010046')
    #k1pro_stitch = k1pro_stitch_window_page()
    #k1pro_stitch.get_k1pro_ws_dlg()
    #k1pro_stitch.k1pro_input_config_file(configPath=r'Z:\calibration_data\K1Pro\bigfrog-2018-7-26\30370028195\2880\outdoor\30370028195.2.8k.json')
    #stitch_window.clear_config()
    # k1pro_stitch.k1pro_input_file_directory(input_file_Path=r'Z:\calibration_data\K1Pro\bigfrog-2018-7-26\30370028195\2880\outdoor')
    # k1pro_stitch.k1pro_stitch_frame('10','15')
    # k1pro_stitch.k1pro_destination_directory(outputPath=r'C:\Users\wu\Desktop\work7-24')
    # k1pro_stitch.k1pro_output_resolution('1024')
    # k1pro_stitch.k1pro_output_type('png')
    # k1pro_stitch.k1pro_layout('top_bottom')
    # k1pro_stitch.k1pro_codec_type('h265')
    # k1pro_stitch.k1pro_quality('60M')
    # k1pro_stitch.k1pro_stitch_engine('cpu')
    # k1pro_stitch.k1pro_switch_left_right('off')
    # k1pro_stitch.k1pro_smart_align('off')
    #stitch_window.stitch_preview(stitchPreviewImagePath=r'C:\Users\wu\Desktop\work7-24')
    #stitch_window.start_stitch()
    #stitch_window.reset()

    #---------------------class advance_options_window_page functions-------------------
    # stitch_window=stitch_window_page()
    # stitch_window.advance_options()#弹出davance_options对话框
    # advance_options = advance_options_pane_page()
    # advance_options.scan_before_stitch(status='off')
    # advance_options.advance_option_flow(status='off')
    # advance_options.option_flow_mode('normal')
    # advance_options.sharpness_compensation(value='high')
    # advance_options.adjust_point_of_interest(60)
    # advance_options.need_flip('on')
    # advance_options.smooth_factor('normal')
    # advance_options.zenith_nadir_feather('on')
    # advance_options.mono_top_enable('on')
    # advance_options.mono_top_degree_from_pole(value=50)
    # advance_options.ok_bottom()

    #------------------------class encode_window_page functions---------------------
    # stitch_window=stitch_window_page()
    #stitch_window.choose_encode_tab()#转到encode界面
    #encode = encode_pane_page()
    #encode.png_file_directory(r'C:\Users\wu\Desktop\work7-24\15030010001_chuxi_pano')
    # encode.video_file_directory(r'C:\Users\wu\Desktop\work8-14')
    # encode.encode_output_type('mp4')
    # encode.video_start_point(40)
    # encode.encode_duration(45)
    #encode.encode_frame_rate('29.97')
    #encode.encode_quality('high')
    #encode.encode_codec_type('h265')
    # encode.encode_stereo_mode('left_right')
    # encode.projection_type('VR180(Equi)')
    # encode.sound_track_enable(status=0)
    # encode.add_sound_track(r'C:\Users\wu\Desktop\work7-24')
    # stitch_window.start_stitch()

    #-----------------------class Record_stitching_window_page functions--------------------------
    # stitch_window = stitch_window_page()
    # stitch_window.start_stitch()
    # stitching_pane = stitching_record_pane_page()
    # #stitching_pane.get_stitching_dlg()
    # stitch_result = stitching_pane.stitching_log()
    # print(stitch_result)
    # #stitching_pane.restart_stitch()
    # stitching_pane.close_stitch()


