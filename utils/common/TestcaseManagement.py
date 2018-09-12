#-*- coing=utf-8 -*-
import unittest
from config.globalconfig import BASE_PATH
import pandas as pd

def getConfigWay(value: str) -> int:
    if value == "1-按方法运行":
        return 1
    elif value == "2-按类名运行":
        return 2
    elif value == "3-按路径运行":
        return 3


def getPath(value: str) -> str:
    value = value.replace("\\", ".")
    if value[0] == ".":
        value = value[1:]
    if value[-1] == ".":
        value = value[:-1]
    return value


def getFileName(value: str) -> str:
    if "." not in value:
        return value
    return ".".join(value.split(".")[0:-1])


def getClassName(value: str) -> str:
    return value


def getFunctionName(value: str) -> str:
    return value


def whetherRun(value: str) -> bool:
    """
    func：Determine whether to run the user case.
    :param value: type = <class str> 
    :return: type = <class boolean>
    """
    if ("N" in value) or ("n" in value) or ("否" in value) or ("不" in value):
        return False
    else:
        return True


def getFileFullName(value: str) -> str:
    """
    func：Gets the name of the file containing the suffix.
    :param value:
    :return:
    """
    if "." not in value:
        raise TypeError("Filename field content must contain file name suffix in 'TestPlanConfig.xlsx'")
    elif value.split(".")[-1] not in ["xlsx", "xls"]:
        raise TypeError(
            "'TestPlanConfig.xlsx' does not support configuring the %s format name,please convert it to .xlsx or.xls." % (value.split(".")[-1])
        )
    else:
        return value


# 读取TestPlanConfig.xlsx，返回一个或多个suite(取决于配置了多少个sheet页，sheet页之间是多进程并行执行)
def addTestCaseByExcel(filename: str) -> tuple:
    """
    func：input:test case configuration file name，return: The test suite
    :param filename:
    :return: (suite1, suite2) <class tuple>
    """
    # 构造测试集 方法1 添加测试用例类中的方法(函数)
    # suite.addTest(S1BasicTest('test_s1_case000001'))
    # suite.addTest(S1BasicTest('test_s1_case000002'))
    # 构造测试集 方法2 添加测试用例类中的所有方法(函数)
    # suite = unittest.TestSuite(unittest.makeSuite(S1BasicTest))
    # 构造测试集 方法3 添加目录中所有的测试用例类的方法(函数)
    # suite = unittest.TestLoader().discover("test")
    # 构造测试集 方法4 按照Excel案例配置运行
    # addTestCaseByExcel(suite)

    suites = []
    od = pd.read_excel(
        io= BASE_PATH + "\\config\\" + filename, sheet_name=None
    )  # 读取所有sheet 返回OrderedDict
    sheets = list(od.keys())  # 获取Execl所有sheet名
    for sheet in sheets:  # 分别处理每个sheet中的案例配置
        suite = unittest.TestSuite()  # 每个sheet构造一个suite
        df = od[sheet]
        max_row = df.shape[0]  # 案例个数
        for i in range(max_row):
            if whetherRun(df.at[i, "是否执行"]):
                path = getPath(df.at[i, "路径"])
                filename = getFileName(df.at[i, "文件名"])
                classname = getClassName(df.at[i, "类名"])
                funname = getFunctionName(df.at[i, "方法名"])
                if getConfigWay(df.at[i, "配置方式"]) == 1:  # 按方法运行
                    import_str = (
                        "from " + path + "." + filename + " import " + classname
                    )
                    addtest_str = "suite.addTest(" + classname + "('" + funname + "'))"
                    exec(import_str)
                    eval(addtest_str)
                elif getConfigWay(df.at[i, "配置方式"]) == 2:  # 按类名运行
                    import_str = (
                        "from " + path + "." + filename + " import " + classname
                    )
                    addtest_str = "suite.addTest(unittest.makeSuite(" + classname + "))"
                    exec(import_str)
                    eval(addtest_str)
                elif getConfigWay(df.at[i, "配置方式"]) == 3:  # 按路径运行
                    addtest_str = (
                        'suite.addTest(unittest.TestLoader().discover("'
                        + path
                        + '"'
                        + "))"
                    )  # suite.addTest(unittest.TestLoader().discover("test"))
                    eval(addtest_str)
        suites.append(suite)
    return tuple(suites)


# 读取TestPlanConfig.xlsx
def readTestPlanExcel() -> tuple:
    """
    说明：读取TestPlanConfig.xlsx，获取配置串行运行案例的文件名。
    :return:文件名 <class tuple>
    """
    df = pd.read_excel(
        io= BASE_PATH + r"\config\TestPlanConfig.xlsx", sheet_name=0
    )  # 只读取第一个sheet页
    max_row = df.shape[0]  # 配置个数
    filenames = []
    for i in range(max_row):
        if whetherRun(df.at[i, "是否执行"]):
            filename = getFileFullName(df.at[i, "文件名"])
            filenames.append(filename)
    return tuple(filenames)


# 构造多进程执行计划
def testPlan() -> tuple:
    """
    说明：构造多进程的执行计划
    :return:
        返回不同Excel中sheet页案例所构造的suite
        ((suite1,), (suite2, suite3), (suite4,)))  <类型 tuple of tuple>
            ^               ^
        Excel有1个sheet Excel有2个sheet
        (suite1,) 与  (suite2, suite3) 与 (suite4,) 串行执行
        suite2, suite3 并行执行
    """
    filenames = readTestPlanExcel()
    allsuites = []
    for filename in filenames:
        suites = addTestCaseByExcel(filename)
        allsuites.append(suites)
    return tuple(allsuites)


# if __name__ == "__main__":
#     print(testPlan())
