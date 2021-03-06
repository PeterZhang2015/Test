import json
import subprocess
import sys
from os import listdir
import shlex

import xlsxwriter
import os
from datetime import datetime
from MAndroid2SmokeTest.library.MAndroid2BaseYaml import getYam
from MAndroid2SmokeTest.library.MAndroid2BaseMCloud import MCloudControl

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

UNLOCK_HANDSET_SCREEN_CODE = '1031'
BACK_TO_HOME_SCREEN_CODE = '1033'

PLACE_VOICE_CALL_CODE = '3010'
RECEIVE_VOICE_CALL_CODE = '3011'
END_VOICE_CALL_CODE = '3012'
SEND_SMS_CODE = '3001'
RECEIVE_SMS_CODE = '3002'
SEND_MMS_CODE = '3003'
RECEIVE_MMS_CODE = '3004'
WEB_BROWSING_CODE = '3030'
HTTP_DOWNLOAD_CODE = '3060'
GET_MANDROID2_VERSION_CODE = '9001'
GET_MANDROID2_AGENT_VERSION_CODE = '9002'
GET_MANDROID2_PLUGIN_VERSION_CODE = '9003'

def getMAndroid2Version(MAndroid2AgentPath, handsetId):
    # Initialization
    version = {}

    # Construct command
    command = "java -jar {} {} {}".format(MAndroid2AgentPath,
                                          handsetId,
                                          GET_MANDROID2_VERSION_CODE)
    print (command)
    # Execute command
    response = json.loads(subprocess.check_output(command.split()))
    print (response)
    if ('version' not in response):
        return None

    # Record version info
    version['MAndroid2'] = response['version']

    # Construct command
    command = "java -jar {} {} {}".format(MAndroid2AgentPath,
                                          handsetId,
                                          GET_MANDROID2_AGENT_VERSION_CODE)
    print (command)
    # Execute command
    response = json.loads(subprocess.check_output(command.split()))
    print (response)
    if ('version' not in response):
        return None

    # Record version info
    version['MAndroid2Agent'] = response['version']

    # Construct command
    command = "java -jar {} {} {}".format(MAndroid2AgentPath,
                                          handsetId,
                                          GET_MANDROID2_PLUGIN_VERSION_CODE)
    print (command)
    # Execute command
    print (response)
    response = json.loads(subprocess.check_output(command.split()))
    if ('version' not in response):
        return None

    # Record version info
    version['MAndroid2Plugin'] = response['version']

    return version

def placeBasicVoiceCall(MAndroid2AgentPath, handsetId, calledUserNumber):

    # Initialization
    dicResponse = {}

    # Construct command
    command = "java -jar {} {} {} call_phonenum {}".format(MAndroid2AgentPath,
                                                                         handsetId,
                                                                         PLACE_VOICE_CALL_CODE,
                                                                         calledUserNumber)
    print("Command of placing basic voice call is: ", command)
    # response = os.system(placeVoiceCallCommand)

    # process = subprocess.Popen(['java', '-jar', MAndroid2AgentPath, handsetId, PLACE_VOICE_CALL_CODE, 'call_phonenum', calledUserNumber],
    #                            stdout=subprocess.PIPE,
    #                            universal_newlines=True)
    # response = process.communicate()[0]

    # response = subprocess.check_output(['java', '-jar', MAndroid2AgentPath, handsetId, PLACE_VOICE_CALL_CODE, 'call_phonenum', calledUserNumber])

    # Execute command
    response = subprocess.check_output(command.split())
    print("Response of placing basic voice call is: ", json.loads(response))

    # Record command and response
    dicResponse['command'] = command
    dicResponse['response'] = json.loads(response)

    return dicResponse

def receiveBasicVoiceCall(MAndroid2AgentPath, handsetId):

    # Initialization
    dicResponse = {}

    # Construct command
    command = "java -jar {} {} {} ".format(MAndroid2AgentPath,
                                                           handsetId,
                                                           RECEIVE_VOICE_CALL_CODE)
    print("Command of receiving basic voice call is: ", command)

    # Execute command
    response = subprocess.check_output(command.split())
    print("Response of receiving basic voice call is: ", json.loads(response))

    # Record command and response
    dicResponse['command'] = command
    dicResponse['response'] = json.loads(response)

    return dicResponse

def endBasicVoiceCall(MAndroid2AgentPath, handsetId):

    # Initialization
    dicResponse = {}

    # Construct command
    command = "java -jar {} {} {}".format(MAndroid2AgentPath,
                                                          handsetId,
                                                          END_VOICE_CALL_CODE)
    print("Command of receiving basic voice call is: ", command)

    # Execute command
    response = subprocess.check_output(command.split())
    print("Response of ending basic voice call is: ", json.loads(response))

    # Record command and response
    dicResponse['command'] = command
    dicResponse['response'] = json.loads(response)

    return dicResponse

def sendSMS(MAndroid2AgentPath, handsetId, calledUserNumber, smsBody):

    # Initialization
    dicResponse = {}

    # Construct command
    smsBody = smsBody.translate(str.maketrans({" ": r"\ "}))
    command = "java -jar {} {} {} sms_address {} sms_body \"{}\"".format(MAndroid2AgentPath,
                                                                         handsetId,
                                                                         SEND_SMS_CODE,
                                                                         calledUserNumber,
                                                                         smsBody)

    print("Command of sending SMS is: ", command)

    # Execute command
    response = subprocess.check_output(shlex.split(command))
    print("Response of sending SMS is: ", json.loads(response))

    # Record command and response
    dicResponse['command'] = command
    dicResponse['response'] = json.loads(response)

    return dicResponse

def receiveSMS(MAndroid2AgentPath, handsetId):

    # Initialization
    dicResponse = {}

    # Construct command
    command = "java -jar {} {} {}".format(MAndroid2AgentPath,
                                         handsetId,
                                         RECEIVE_SMS_CODE)

    print("Command of receiving SMS is: ", command)

    # Execute command
    response = subprocess.check_output(command.split())
    print("Response of receiving SMS is: ", json.loads(response))

    # Record command and response
    dicResponse['command'] = command
    dicResponse['response'] = json.loads(response)

    return dicResponse

def getMMSUrl(MAndroid2AgentPath, handsetId):

    # Construct command
    command = "java -jar {} {} {}".format(MAndroid2AgentPath,
                                         handsetId,
                                         BACK_TO_HOME_SCREEN_CODE)

    # Execute command
    response = subprocess.check_output(shlex.split(command))

    # Get screenshotURL as mmsURL from response
    dicResponse = json.loads(response)
    if ('screenshotURL' not in dicResponse):
        return None
    else:
        return dicResponse['screenshotURL']

def unlockHandsetScreen(MAndroid2AgentPath, handsetId):
    # Initialization
    dicResponse = {}

    # Construct command
    command = "java -jar {} {} {}".format(MAndroid2AgentPath,
                                         handsetId,
                                         UNLOCK_HANDSET_SCREEN_CODE)

    # Execute command
    response = subprocess.check_output(shlex.split(command))

    # Record command and response
    dicResponse['command'] = command
    dicResponse['response'] = json.loads(response)

    return dicResponse

def sendMMS(MAndroid2AgentPath, handsetId, calledUserNumber, mmsBody, mmsUrl):

    # Initialization
    dicResponse = {}

    # Construct command
    mmsBody = mmsBody.translate(str.maketrans({" ": r"\ "}))
    command = "java -jar {} {} {} mms_address {} mms_body \"{}\" mms_url \"{}\"".format(MAndroid2AgentPath,
                                                                         handsetId,
                                                                         SEND_MMS_CODE,
                                                                         calledUserNumber,
                                                                         mmsBody,
                                                                         mmsUrl)

    print("Command of sending MMS is: ", command)

    # Execute command
    response = subprocess.check_output(shlex.split(command))
    print("Response of sending MMS is: ", json.loads(response))

    # Record command and response
    dicResponse['command'] = command
    dicResponse['response'] = json.loads(response)

    return dicResponse

def receiveMMS(MAndroid2AgentPath, handsetId):

    # Initialization
    dicResponse = {}

    # Construct command
    command = "java -jar {} {} {}".format(MAndroid2AgentPath,
                                         handsetId,
                                         RECEIVE_MMS_CODE)

    print("Command of receiving MMS is: ", command)

    # Execute command
    response = subprocess.check_output(command.split())
    print("Response of receiving MMS is: ", json.loads(response))

    # Record command and response
    dicResponse['command'] = command
    dicResponse['response'] = json.loads(response)

    return dicResponse

def webBrowsing(MAndroid2AgentPath, handsetId, webUrl):

    # Initialization
    dicResponse = {}

    # Construct command
    command = "java -jar {} {} {} web_url \"{}\"".format(MAndroid2AgentPath,
                                                     handsetId,
                                                     WEB_BROWSING_CODE,
                                                     webUrl)

    print("Command of web browsing is: ", command)

    # Execute command
    response = subprocess.check_output(command.split())
    print("Response of web browsing is: ", json.loads(response))

    # Record command and response
    dicResponse['command'] = command
    dicResponse['response'] = json.loads(response)

    return dicResponse

def startHTTPDownload(MAndroid2AgentPath, handsetId, downloadUrl):

    # Initialization
    dicResponse = {}

    # Construct command
    downloadFileName = str(downloadUrl).split("/")[-1]
    command = "java -jar {} {} {} download_url \"{}\" fileName \"{}\"".format(MAndroid2AgentPath,
                                                                         handsetId,
                                                                         HTTP_DOWNLOAD_CODE,
                                                                         downloadUrl,
                                                                         downloadFileName)

    print("Command of HTTP downloading is: ", command)

    # Execute command
    response = subprocess.check_output(command.split())
    print("Response of HTTP downloading is: ", json.loads(response))

    # Record command and response
    dicResponse['command'] = command
    dicResponse['response'] = json.loads(response)

    return dicResponse

def getFileInfo(MAndroid2AgentPath, handsetId, fileUrl):

    # Initialization
    dicResponse = {}

    # Construct command
    command = "adb -s {} shell ls -la {}".format(handsetId, fileUrl)

    # Execute command
    response = subprocess.check_output(command.split()).decode('utf-8').split()

    # Record command and response
    dicResponse['command'] = command
    dicResponse['response'] = response

    return dicResponse

