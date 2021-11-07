
import urllib.request, urllib.error, urllib.parse

IP_Address = '192.168.1.32'
port = '8085'

# Function to log data to Domoticz server...
def LogToDomoticz(idx, SensorVal):
    url = 'http://' + IP_Address + ':' + port + '/json.htm?type=command&param=udevice&nvalue=0&idx='+idx+'&svalue='+str(SensorVal)

    try:
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
    except urllib.error.HTTPError as e:
        response = "HTTPError: " + e
    except urllib.error.URLError as e:
        response = "URLError: " + e
    except:
        response = "Error"

    return response
