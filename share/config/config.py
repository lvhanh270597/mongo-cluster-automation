from os import path
import os, json


BASPATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CNFPATH = path.join(BASPATH, "config")
RESPATH = path.join(BASPATH, "resource")
SHEPATH = path.join(RESPATH, "shell")
CNFNAME = "config.json"
KEYNAME = "keyfile.key"

config = dict()
with open(path.join(CNFPATH, CNFNAME)) as filedata:
    config = json.load(filedata)

config["add"] = {
    "admin" : path.join(RESPATH, "users", "admin.js"),
    "user" : path.join(RESPATH, "users", "user.js"),
    "init" : path.join(RESPATH, "cluster", "init_cluster.js"),
    "hosts" : path.join(RESPATH, "cluster", "add_hosts.js"),
    
    "tmp_admin" : path.join(RESPATH, "users", "admin.tmp.js"),
    "tmp_user" : path.join(RESPATH, "users", "user.tmp.js"),
    "tmp_init" : path.join(RESPATH, "cluster", "init_cluster.tmp.js"),
    "tmp_hosts" : path.join(RESPATH, "cluster", "add_hosts.tmp.js")
}

config["config"] = {
    "create_users" : "mongod --fork --port %s --bind_ip 0.0.0.0 --logappend --logpath %s --dbpath %s --pidfilepath %s",
    "create_cluster" : "mongod --fork --keyFile %s --replSet %s --bind_ip 0.0.0.0 --port %s  --logappend --logpath %s --dbpath %s --pidfilepath %s",
    "start_service" : "mongod --fork --keyFile %s --replSet %s  --bind_ip 0.0.0.0 --port %s --logappend --logpath %s --dbpath %s --pidfilepath %s"
}