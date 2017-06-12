import urllib2
import os
import datetime
from datetime import datetime
import csv

errors = []

def downloadUrl(url, count, row_count):
    try:
        file_name = url.split('/')[-1]
        u = urllib2.urlopen(url)
        f = open(file_name, 'wb')
        meta = u.info()
        file_size = int(meta.getheaders("Content-Length")[0])
        print "[%d / %d] Downloading: %s Bytes: %s" %(count, row_count, file_name, file_size)

        file_size_dl = 0
        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break
            file_size_dl += len(buffer)
            f.write(buffer)
            status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
            status = status + chr(8)*(len(status)+1)
            print status,

        f.close()
    except:
        errors.append(url)
        print '*** ERROR WITH:', url


file = open("urls.csv")
row_count = len(file.readlines())
print("")

with open('urls.csv', 'rb') as f:
    count = 1
    reader = csv.reader(f, delimiter=' ')
    exportDIR = datetime.now().strftime('%Y-%m-%d_%H.%M.%S')
    os.system('mkdir ' + exportDIR)
    os.chdir(exportDIR)
    for row in reader:
        url = row[0]
        downloadUrl(url, count, row_count)
        count = count + 1
    print '\n\n[ FINISHED DOWNLOADING FILES ]\n'

    if len(errors) > 0:
        print '(%d) ERRORS:' %(len(errors))
        for element in errors:
            print element
