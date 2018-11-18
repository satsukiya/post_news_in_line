import urllib.request
from urllib.error import URLError, HTTPError
import time

def loopRequest(url, maxRetry=100, isPrint=False):
    count = 0
    mark = None
    while (0 <= maxRetry):
        try:
            html = urllib.request.urlopen(url)
            mark = html.read().decode("utf-8")
            maxRetry = -1 
        except HTTPError as e:
            time.sleep(5)
            maxRetry = maxRetry - 1
            count = count + 1

    if isPrint:
        print("[url]" + url)
        print("[request url count]" + str(count))

    return mark

def imageDownload(url, path, name="", exe=".png", isPrint=False):

    isSuccess = False
    filepath = ""
    try:
        i = urllib.request.urlopen(url)
        filename = url.split('/')[-1]
        basename = filename.split(".")[0]

        if name != "":
            basename = name

        filepath = path + basename + exe
        saveData = open(filepath, 'wb');

        saveData.write(i.read());
        saveData.close()
        i.close()
        isSuccess = True        

    except:
        isSuccess = False
        print ('[error:imageDownload]: ' + url)
    finally :
        if isPrint:
            print ('>>> getImage:' + filepath)

    return isSuccess, filepath