import tempfile
import subprocess

from db_handler import get_file

def writeTofile(data):
    fle = tempfile.NamedTemporaryFile(delete=False);
    fle.write(data)
    return fle

def readBlobData(id):
    record = get_file(id)
    fileName = "";
    fileContent = record[0]

    fileName = writeTofile(fileContent)
    subprocess.call(('xdg-open', fileName.name))
