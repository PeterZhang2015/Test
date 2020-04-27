import sys
import os
import requests
import json
import time
import subprocess

from MAndroid2SmokeTest.library.MAndroid2BaseYaml import getConfigureInfo

class MCloudControl(object):
    # Define basic information on MCloud.
    mcloudBaseUrl = "http://mcloud.matrium.com.au:7100/api/v1"
    mcloudLoginUser = "Peter.Zhang@matrium.com.au"
    mcloudLoginToken = "Bearer 6fc22b08ce00468fa56cc53a22384012e16d1ac9ab12403abeaaa5e14496239e"
    deviceSerialList = []

    # testEnvironmentPath = "../configuration/testEnvironment/"
    # testEnvironmentName = "testEnvironment"
    # testEnvironment = getConfigureInfo(testEnvironmentPath, testEnvironmentName)
    # mcloudBaseUrl = testEnvironment['MCloud']['baseUrl']
    # mcloudLoginToken = testEnvironment['MCloud']['accessToken']
    # mcloudLoginUser = testEnvironment['tester']
    # deviceSerialList = []

    def _url(self, path):
        return self.mcloudBaseUrl + path

    def requestDevice(self, deviceSerial):

        # Set authorization Token to acces mCloud through REST API.
        headers = {"Authorization": self.mcloudLoginToken, "Content-Type": "application/json"}
        # Set device serial as the REST API POST body.
        data = {"serial": deviceSerial}

        # Call REST API to use the device on mcloud.
        print("##########Calling REST API to use device {} on MCloud.".format(deviceSerial))
        resp = requests.post(self._url('/user/devices'),
                             headers=headers,
                             data=json.dumps(data),)

        print (self._url('/user/devices'))

        if resp.status_code == 200:
            # Check REST API response.
            dictResponse = json.loads(resp.content)
            print(dictResponse)

            self.deviceSerialList.append(deviceSerial)
            print("Adding {} to deviceSerialList".format(deviceSerial))

            return True
        else:
            print('[!] HTTP {0} calling [{1}]'.format(resp.status_code, self._url('/user/devices')))
            return False



    def remoteConnect(self, deviceSerial):
        # Set authorization Token to acces mCloud through REST API.
        headers = {"Authorization": self.mcloudLoginToken, "Content-Type": "application/json"}
        # Set device serial as the REST API POST body.
        data = {"serial": deviceSerial}

        # Call REST API to get the remote debug URL of the testing device for further adb control.
        print("##########Calling REST API to get the remote debug URL of the testing device {} on MCloud.".format(deviceSerial))
        resp = requests.post(self._url('/user/devices/{}/remoteConnect'.format(deviceSerial)),
                             data=json.dumps(data),
                             headers=headers)

        print(self._url('/user/devices/{}/remoteConnect'.format(deviceSerial)))

        if resp.status_code == 200:
            # Check REST API response.
            dictResponse = json.loads(resp.content)
            print(dictResponse)
            return resp
        else:
            print('[!] HTTP {0} calling [{1}]'.format(self._url('/user/devices/{}/remoteConnect'.format(deviceSerial))))
            return None



    def releaseDevice(self, deviceSerial):
        # Set authorization Token to acces mCloud through REST API.
        headers = {"Authorization": self.mcloudLoginToken}

        # Call REST API to release the use of the testing device.
        print("##########Calling REST API to release device {} on MCloud.".format(deviceSerial))
        resp = requests.delete(self._url('/user/devices/' + deviceSerial),
                             headers=headers)
        print(self._url('/user/devices/' + deviceSerial))
        print("resp.status_code is {}".format(resp.status_code))

        if resp.status_code == 200:
            # Check REST API response.
            dictResponse = json.loads(resp.content)
            print(dictResponse)
            if (deviceSerial in self.deviceSerialList):
                self.deviceSerialList.remove(deviceSerial)
            return True
        else:
            print('[!] HTTP {0} calling [{1}]'.format(self._url('/user/devices/' + deviceSerial)))
            return False


    def getDeviceSerialByImsi(self, userIMSI):
        # Initialize return value.
        deviceSerial = None

        # Set authorization Token to acces mCloud through REST API.
        headers = {"Authorization": self.mcloudLoginToken}

        # Call REST API to get the devices list on mcloud.
        print("##########Calling REST API to get devices list on MCloud.")
        resp = requests.get(self._url('/devices'),
                             headers=headers)

        print (self._url('/devices'))
        dictResponse = json.loads(resp.content)
        # print(dictResponse)

        if resp.status_code == 200:
            # Check REST API response.
            # Get device list from response body.
            devicesList = dictResponse['devices']

            # Check whether any handset is connected on mcloud.
            if (len(devicesList) == 0):
                raise SystemExit("There is not handset connected to the mcloud.")

            # Loop to check the device that can be matched with the testing user IMSI.
            for device in devicesList:
                # Only check the present handsets.
                if ((device['present'] != True) or (device['phone']['imsi'] == None)):
                    continue

                # Get the device serial of the matched IMSI.
                if (device['phone']['imsi'] == userIMSI):
                    deviceSerial = device['serial']
                    break

            if (deviceSerial) == None:
                print("There is no device that can be matched with the testing user IMSI.")
                return None

            # Check that whether the device has been occupied by someone else
            if (device['owner'] != None):
                currentDeviceOwner = device['owner']['email']

            if (device['owner'] == None):
                print("Handset with IMSI {} has not been occupied.".format(userIMSI))
                print("Corresponding device serial is {}.".format(deviceSerial))

            elif (currentDeviceOwner == self.mcloudLoginUser):
                self.releaseDevice(deviceSerial)
                print("Handset with IMSI {} has been occupied by myself {}.".format(userIMSI,
                                                                                    self.mcloudLoginUser))

            else:
                print("Handset with IMSI {} has been occupied by mcloud user {}.".format(userIMSI,
                                                                           device['owner']['email']))
                return None

            return deviceSerial
        else:
            print('[!] HTTP {0} calling [{1}]'.format(self._url('/devices')))
            return None



    def connectToMcloudUser(self, userIMSI):
        # Try to find the device serial of the matched IMSI.
        deviceSerial = self.getDeviceSerialByImsi(userIMSI)

        if (deviceSerial == None):
            print ("Cannot find the matched IMSI {} on mcloud".format(userIMSI))
            return None
        else:
            print("Find the matched IMSI {} on mcloud".format(userIMSI))

        # Use the device on mcloud.
        result = self.requestDevice(deviceSerial)
        if (result == False):
            print("Failed to use the device {} on mcloud.".format(deviceSerial))
            return None

        # Get the device remote control url.
        resp = self.remoteConnect(deviceSerial)
        # Abort the execution if failed to call the API.
        if (resp == None):
            print ("Fail to remoteConnect {} on mcloud".format(userIMSI))
            return None

        dictResponse = json.loads(resp.content)

        # Abort the execution if it cannot get the remote control url of the testing device.
        if (dictResponse['success'] != True):
            print ("Fail to remoteConnect {} on mcloud".format(userIMSI))
            return None
        else:
            print ("connect {} on mcloud successfully".format(userIMSI))

        # ADB connect to the device on mCloud.
        process = subprocess.Popen(['adb', 'connect', dictResponse['remoteConnectUrl']],
                                   stdout=subprocess.PIPE,
                                   universal_newlines=True)

        print ("remoteConnectUrl is ", dictResponse['remoteConnectUrl'])

        return dictResponse['remoteConnectUrl']

    def tearDownUsingDevices(self, deviceSerialList):
        # ADB disconnect to all devices.
        subprocess.call("adb disconnect")

        # release all used devices.
        tempList = deviceSerialList.copy()
        for deviceSerial in tempList:
            result = self.releaseDevice(deviceSerial)
            if (result == False):
                sys.exit("Failed to release device ", deviceSerial)
            print("Remaining released deviceSerialList is {}".format(deviceSerialList))

        # ADB disconnect to all devices.
        subprocess.call("adb disconnect")


if __name__ == '__main__':
    testIMSI = '505025504563848'
    mcloud = MCloudControl()
    handset_id = mcloud.connectToMcloudUser(testIMSI)

    time.sleep (5)
    mcloud.tearDownUsingDevices(mcloud.deviceSerialList)


