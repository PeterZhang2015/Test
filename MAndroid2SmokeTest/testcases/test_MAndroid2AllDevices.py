import os
import subprocess
import sys

# from ..library.MAndroid2BaseYaml import getYam
# from ..library.MAndroid2BaseMCloud import MCloudControl
from datetime import datetime, timedelta
from os import listdir
from time import sleep

import pytest

from MAndroid2SmokeTest.library.MAndroid2BaseYaml import getYam
from MAndroid2SmokeTest.library.MAndroid2BaseMCloud import MCloudControl
from MAndroid2SmokeTest.library.MAndroid2BaseCommon import addJsonReportMetaData, executeTestLogic, \
    verifyTestCaseResult, connectTestUsers, checkTestEnvironmentConfig, checkTestParametersConfig, \
    checkTestCaseInfoConfig, createExcelTestReport, writeExcelTestReportSummary, initializeExcelSummary, \
    writeExcelTestReportDetail, executeTestCase, getAllAvailableDevicesUnderDifferentEnvironment
from MAndroid2SmokeTest.library.MAndroid2BaseCommon import disconnectTestUsers
from MAndroid2SmokeTest.library.MAndroid2BaseYaml import getAllConfigureInfo
from MAndroid2SmokeTest.library.MAndroid2BaseYaml import getConfigureInfo

from MAndroid2SmokeTest.library.MAndroid2BaseAPI import placeBasicVoiceCall, getMAndroid2Version
from MAndroid2SmokeTest.library.MAndroid2BaseAPI import receiveBasicVoiceCall
from MAndroid2SmokeTest.library.MAndroid2BaseAPI import endBasicVoiceCall

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

RELPATH = lambda p: os.path.relpath(
    os.path.join(os.path.dirname(__file__), p)
)

@pytest.mark.allAvailableDeviceSmokeTest

class TestMAndroid2TestCases():
    # Initialize variables.
    testEnvironmentPath = "../configuration/testEnvironment/"
    testEnvironmentName = "testEnvironment"
    testParametersName = "testParameters"
    excelReportPath = "../reports/excel/"
    voiceCallTestParametersPath = "../configuration/testParameters/voiceCall/testParameters1.yaml"
    smsTestParametersPath = "../configuration/testParameters/SMS/testParameters1.yaml"
    mmsTestParametersPath = "../configuration/testParameters/MMS/testParameters1.yaml"
    webBrowsingTestParametersPath = "../configuration/testParameters/webBrowsing/testParameters1.yaml"
    httpDownloadTestParametersPath = "../configuration/testParameters/httpDownload/testParameters1.yaml"
    testCaseSummary = {}
    testCaseDetailList = []
    voiceCallTestParameters = []
    smsTestParameters = []
    mmsTestParameters = []
    webBrowsingTestParameters = []
    httpDownloadTestParameters = []

    testEnvironments = getAllConfigureInfo(testEnvironmentPath, testEnvironmentName)
    assert (testEnvironments != None)

    parameters = getConfigureInfo(voiceCallTestParametersPath, testParametersName)
    assert (parameters != None)
    voiceCallTestParameters.append(parameters)

    parameters = getConfigureInfo(smsTestParametersPath, testParametersName)
    assert (parameters != None)
    smsTestParameters.append(parameters)

    parameters = getConfigureInfo(mmsTestParametersPath, testParametersName)
    assert (parameters != None)
    mmsTestParameters.append(parameters)

    parameters = getConfigureInfo(webBrowsingTestParametersPath, testParametersName)
    assert (parameters != None)
    webBrowsingTestParameters.append(parameters)

    parameters = getConfigureInfo(httpDownloadTestParametersPath, testParametersName)
    assert (parameters != None)
    httpDownloadTestParameters.append(parameters)

    testEnvironmentCombinations = getAllAvailableDevicesUnderDifferentEnvironment(testEnvironments)

    print("testEnvironmentCombinations is: {}".format(testEnvironmentCombinations))

    @classmethod
    def setup_class(cls):
        print("------ Setup before class TestMAndroid2TestCases ------")
        # Check excel report directory exist.
        if (os.path.exists(os.path.abspath(cls.excelReportPath)) == False):
            os.makedirs(cls.excelReportPath)

        # Create excel report and initialize test case summary.
        cls.excelReport, cls.summarySheet, cls.detailSheet = createExcelTestReport(cls.excelReportPath)
        cls.testCaseSummary = initializeExcelSummary(cls.testCaseSummary)

        # Get test case starting date.
        cls.testSuiteStartingTime = datetime.now()
        cls.testCaseSummary['testingDate'] = cls.testSuiteStartingTime.strftime("%d/%b/%Y_%H:%M:%S.%f")

    @classmethod
    def teardown_class(cls):
        print("------ Teardown after class TestMAndroid2TestCases ------")

        # Get test case ending date.
        cls.testSuiteEndTime = datetime.now()
        diff = cls.testSuiteEndTime - cls.testSuiteStartingTime  # the result is a datetime.timedelta object
        formatedDiff = str(timedelta(seconds=diff.seconds))
        cls.testCaseSummary['testDuration'] = "{}".format(formatedDiff)

        # Write excel test report.
        cls.excelReport.summary(cls.summarySheet, cls.testCaseSummary)
        print ("testCaseDetailList is {}".format(cls.testCaseDetailList))
        cls.excelReport.detail(cls.detailSheet, cls.testCaseDetailList)
        cls.excelReport.close()

    @pytest.mark.parametrize("testEnvironment", testEnvironmentCombinations)
    @pytest.mark.parametrize("testParameters", voiceCallTestParameters)
    def test_MAndroid2_VoiceCall(self, json_metadata, testEnvironment, testParameters):
        # Define test case variables.
        testCaseKey = 'VoiceCall'
        userFlag = 'MOMT'

        # Get and check test case info.
        testCaseInfo = checkTestCaseInfoConfig(testCaseKey)
        print ("testParameters is: {}".format(testParameters))
        # Execute test case.
        testResults = executeTestCase(testCaseKey, userFlag, json_metadata, testEnvironment, testParameters,
                                      testCaseInfo, self.testCaseSummary, self.testCaseDetailList)

        # Write test case summary and test case detail.
        writeExcelTestReportSummary(self.testCaseSummary, testResults, testEnvironment)
        writeExcelTestReportDetail(self.testCaseDetailList, testEnvironment, testParameters,
                                                             testCaseInfo, testResults)

        # Assert test result.
        for result in testResults:
            assert (result['checkPointResult'] == "passed")

    @pytest.mark.parametrize("testEnvironment", testEnvironmentCombinations)
    @pytest.mark.parametrize("testParameters", smsTestParameters)
    def test_MAndroid2_SMS(self, json_metadata, testEnvironment, testParameters):
        # Define test case variables.
        testCaseKey = 'SMS'
        userFlag = 'MOMT'

        # Get and check test case info.
        testCaseInfo = checkTestCaseInfoConfig(testCaseKey)

        # Execute test case.
        testResults = executeTestCase(testCaseKey, userFlag, json_metadata, testEnvironment, testParameters,
                                      testCaseInfo, self.testCaseSummary, self.testCaseDetailList)

        # Write test case summary and test case detail.
        writeExcelTestReportSummary(self.testCaseSummary, testResults, testEnvironment)
        writeExcelTestReportDetail(self.testCaseDetailList, testEnvironment, testParameters,
                                                             testCaseInfo, testResults)

        # Assert test result.
        for result in testResults:
            assert (result['checkPointResult'] == "passed")

    @pytest.mark.parametrize("testEnvironment", testEnvironmentCombinations)
    @pytest.mark.parametrize("testParameters", mmsTestParameters)
    def test_MAndroid2_MMS(self, json_metadata, testEnvironment, testParameters):
        # Define test case variables.
        testCaseKey = 'MMS'
        userFlag = 'MOMT'

        # Get and check test case info.
        testCaseInfo = checkTestCaseInfoConfig(testCaseKey)

        # Execute test case.
        testResults = executeTestCase(testCaseKey, userFlag, json_metadata, testEnvironment, testParameters,
                                      testCaseInfo, self.testCaseSummary, self.testCaseDetailList)

        # Write test case summary and test case detail.
        writeExcelTestReportSummary(self.testCaseSummary, testResults, testEnvironment)
        writeExcelTestReportDetail(self.testCaseDetailList, testEnvironment, testParameters,
                                                             testCaseInfo, testResults)

        # Assert test result.
        for result in testResults:
            assert (result['checkPointResult'] == "passed")

    @pytest.mark.parametrize("testEnvironment", testEnvironmentCombinations)
    @pytest.mark.parametrize("testParameters", webBrowsingTestParameters)
    def test_MAndroid2_WebBrowsing(self, json_metadata, testEnvironment, testParameters):

        print("testParameters is: {}".format(testParameters))

        # Define test case variables.
        testCaseKey = 'WebBrowsing'
        userFlag = 'MO'

        # Get and check test case info.
        testCaseInfo = checkTestCaseInfoConfig(testCaseKey)

        # Execute test case.
        testResults = executeTestCase(testCaseKey, userFlag, json_metadata, testEnvironment, testParameters,
                                      testCaseInfo, self.testCaseSummary, self.testCaseDetailList)

        # Write test case summary and test case detail.
        writeExcelTestReportSummary(self.testCaseSummary, testResults, testEnvironment)
        writeExcelTestReportDetail(self.testCaseDetailList, testEnvironment, testParameters,
                                                             testCaseInfo, testResults)

        # Assert test result.
        for result in testResults:
            assert (result['checkPointResult'] == "passed")

    @pytest.mark.parametrize("testEnvironment", testEnvironmentCombinations)
    @pytest.mark.parametrize("testParameters", httpDownloadTestParameters)
    def test_MAndroid2_HTTPDownload(self, json_metadata, testEnvironment, testParameters):
        # Define test case variables.
        testCaseKey = 'HTTPDownload'
        userFlag = 'MO'

        # Get and check test case info.
        testCaseInfo = checkTestCaseInfoConfig(testCaseKey)

        # Execute test case.
        testResults = executeTestCase(testCaseKey, userFlag, json_metadata, testEnvironment, testParameters,
                                      testCaseInfo, self.testCaseSummary, self.testCaseDetailList)

        # Write test case summary and test case detail.
        # self.testCaseSummary = writeExcelTestReportSummary(self.testCaseSummary, testResults, testEnvironment)
        # self.testCaseDetailList = writeExcelTestReportDetail(self.testCaseDetailList, testEnvironment, testParameters,
        #                                                      testCaseInfo, testResults)
        writeExcelTestReportSummary(self.testCaseSummary, testResults, testEnvironment)
        writeExcelTestReportDetail(self.testCaseDetailList, testEnvironment, testParameters,
                                                             testCaseInfo, testResults)
        # Assert test result.
        for result in testResults:
            assert (result['checkPointResult'] == "passed")


if __name__ == '__main__':
    # Generate timestamp.
    dateTimeObj = datetime.now()
    timestampStr = dateTimeObj.strftime("%d_%b_%Y_%H_%M_%S.%f")

    # Construct report parameters.
    reportPath = RELPATH("../reports")
    htmlReport = "--html={}/html/htmlReport_{}.html".format(reportPath, timestampStr)
    jsonReport = "--json-report --json-report-file {}/json/jsonReport_{}.json".format(reportPath, timestampStr)
    print(jsonReport)

    # Execute test case.
    generateReportCommand = "pytest -m 'allAvailableDeviceSmokeTest' -q -r test_MAndroid2AllDevices.py {} {}".format(jsonReport, htmlReport)
    print(generateReportCommand)
    output3 = os.system(generateReportCommand)

    # Execute test cases and generate reports. Not sure why it is not working for json report.
    # pytest.main(["-q", "-r", "test_MAndroid2TestCases.py", jsonReport, htmlReport])
    # pytest.main(["-q", "-r", "test_MAndroid2TestCases.py", jsonReport])

    # pytest.main(["-v","test_MAndroid2TestCases.py",'--alluredir','result'])

    # pytest.main(["-s", "-q", '--alluredir', 'report/result', 'test_MAndroid2TestCases.py'])

    # #Generate json report
    # executeCommand = "pytest -s -q --alluredir report/result test_MAndroid2TestCases.py"
    # output1 = os.system(executeCommand)
    # print ("Generate json report command response", output1)
    #
    # # Change to report path.
    # reportPath = "C:\\Work\\Projects\\Python-Practice\\report"
    # output2 = os.chdir(reportPath)
    # print("Change to report path command response", output2)
    # print(os.getcwd())
    #
    # # Change json format to html format.
    # changeToHtmlCommand = "allure generate ./result/ -o ./report/html --clean"
    # output3 = os.system(changeToHtmlCommand)
    # print("Change json format to html format command response", output3)