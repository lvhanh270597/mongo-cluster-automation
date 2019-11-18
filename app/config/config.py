import os, json
import io

BASEDIR = os.path.dirname(os.path.abspath(__name__))
APPPATH = os.path.join(BASEDIR, "app")
CNFPATH = os.path.join(APPPATH, "config")
SRCPATH = os.path.join(APPPATH, "source")
RESPATH = os.path.join(APPPATH, "resource")
SHEPATH = os.path.join(RESPATH, "shell")
SHAPATH = os.path.join(BASEDIR, "share")
CNFNAME = "config.json"
SIPMASTER = "172.16.176.1"
config = dict()
with open(os.path.join(CNFPATH, CNFNAME)) as filedata:
    config = json.load(filedata)