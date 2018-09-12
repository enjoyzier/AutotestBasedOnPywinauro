from utils.common.HTMLTestRunner import HTMLTestRunner
import os.path
from config.globalconfig import REPORT_PATH,TEST_CASE_PATH,BASE_PATH
import time
import unittest
from utils.common.TestcaseManagement import testPlan
from utils.common import log,file_reader
filename= os.path.basename(os.path.realpath(__file__)).split('.')[0]
logger = log.Logger(filename).get_logger()
import traceback
import shutil
from utils.common.common_func import send_email
import multiprocessing

Config = file_reader.Config()
def makeTestCase():
    try:
        logger.info("Building test case starts")
        # 按照Excel配置运行
        allsuites = testPlan()
        logger.info("Build test case end!")
        return allsuites
    except:
        logger.error("Test case construction failed。ErrMsg:\n" + traceback.format_exc())


# 运行前的初始化工作
def init():
    tempimgpath = os.path.join(BASE_PATH, "report", "tempimg")  # 截图的临时目录
    if os.path.exists(tempimgpath):
        shutil.rmtree(tempimgpath)
        os.mkdir(tempimgpath)
    else:
        os.mkdir(tempimgpath)

def run_test(generateTestReport=False,p_suite=()):
    #生成测试报告运行
    if generateTestReport == True:
        report_title = 'WonderStitch用例执行报告'
        desc = '用例执行报告'
        now_time = time.strftime('%Y%m%d-%H%M%S')
        os.mkdir(REPORT_PATH + r"\ResultReport-%s" % now_time)  # 创建一个与报告文件名同名的目录
        report_file = REPORT_PATH + r"\ResultReport-%s" % now_time + r"\ResultReport-%s.html" % now_time
        with open(report_file, 'wb') as report:
            runner = HTMLTestRunner(stream=report, title=report_title, description=desc)
            runner.run(p_suite)
            # 邮件发送
        try:
            if Config.sendEmail:
                logger.info("Start sending mail！")
                send_email()  # 发送邮件
                logger.info("End of mail delivery")
        except:
            logger.error("send email fialed。ErrMsg:\n" + traceback.format_exc())

    #不生成测试报告运行
    else:
        runner = unittest.TextTestRunner()
        runner.run(p_suite)

def main():
    init()
    allsuites = makeTestCase()
    print('allsuites:',allsuites)
    generateTestReport = True
    # 多进程执行开始
    logger.info("Start executing test cases")
    for suites in allsuites:
        processes = []
        for suite in suites:
            processes.append(multiprocessing.Process(target=run_test, args=(generateTestReport,suite,)))
        for p in processes:
            p.start()
        for p in processes:
            p.join()
    logger.info("End of test execution")

if __name__ == '__main__':
   main()

