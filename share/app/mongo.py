from config.config import *
from system import fman
import subprocess
import os
import ntpath

class Mongo:

    def __init__(self, role, pos=0):
        self.role = role
        self.pos = pos
        self.init_folders()
    
    def init_folders(self):
        if self.role == 'slave':
            self.host = config["slaves"][self.pos]
        else:
            self.host = config["master"]
        self.config = config["hosts"][self.host]
        fman.create_path(self.config["data"]["sharedir"])
        fman.create_path(self.config["data"]["datadir"])
        fman.create_path(self.config["data"]["data_path"])
        fman.create_path(os.path.dirname(self.config["data"]["log_path"]))
        fman.create_file(self.config["data"]["log_path"])

    def init_users(self):
        """mongod --fork --port %s --bind_ip 0.0.0.0 --logappend --logpath %s --dbpath %s --pidfilepath %s"""
        command = config["config"]["create_users"] % (
            self.config["service"]["port"], 
            self.config["data"]["log_path"],
            self.config["data"]["data_path"],
            self.config["data"]["pidfile"]
        )
        print(command)
        subprocess.call(command.split())
        # run script add user admin
        replace = {
            "__port__" : self.config["service"]["port"],
            "__user__" : config["accounts"]["admin"]["username"],
            "__pass__" : config["accounts"]["admin"]["password"]
        }
        fman.search_replace(config["add"]["admin"], replace, config["add"]["tmp_admin"])
        subprocess.call(["mongo", "--port", self.config["service"]["port"], config["add"]["tmp_admin"]])

        replace = {
            "__port__" : self.config["service"]["port"],
            "__user__" : config["accounts"]["other"]["username"],
            "__pass__" : config["accounts"]["other"]["password"],
            "__db__"   : config["accounts"]["other"]["db"]
        }
        fman.search_replace(config["add"]["user"], replace, config["add"]["tmp_user"])
        subprocess.call(["mongo", "--port", self.config["service"]["port"], config["add"]["tmp_user"]])
        
        subprocess.call(["pkill", "mongod"])

    # For master
    def create_keyfile(self):
        subprocess.call([os.path.join(SHEPATH, "create_keyfile.sh"), KEYPATH])
    # For master
    def send_keyfile(self):
        """Send to shared folder"""
        filepath = os.path.join(self.config["data"]["sharedir"], ntpath.basename(KEYPATH))
        subprocess.call(["cp", KEYPATH, filepath])
    # For slave
    def get_keyfile(self):
        """Copy from sharefolder"""
        filepath = os.path.join(self.config["data"]["sharedir"], ntpath.basename(KEYPATH))
        subprocess.call(["cp", filepath, KEYPATH])

    def create_cluster(self):
        self.create_keyfile()
        self.send_keyfile()
        """mongod --fork --keyFile %s --replSet %s --bind_ip 0.0.0.0 --port %s  --logappend --logpath %s --dbpath %s --pidfilepath %s"""
        command = config["config"]["create_cluster"] % (
            KEYPATH,
            config["repl_name"],
            self.config["service"]["port"],
            self.config["data"]["log_path"],
            self.config["data"]["data_path"],
            self.config["data"]["pidfile"]
        )
        print(command)
        subprocess.call(command.split())

        replace = {
            "__port__" : self.config["service"]["port"],
            "__user__" : config["accounts"]["admin"]["username"],
            "__pass__" : config["accounts"]["admin"]["password"],
            "__replName__"   : config["repl_name"],
            "__host__" : self.host
        }
        fman.search_replace(config["add"]["init"], replace, config["add"]["tmp_init"])
        subprocess.call(["mongo", "--port", self.config["service"]["port"], config["add"]["tmp_init"]])
        # run script add user admin

    # For master
    def init(self):
        self.init_users()

    # For master
    def create(self):
        self.create_cluster()

    def add(self):
        string = []
        for slave in config["slaves"]:
            string.append("%s:%s" % (slave, config["hosts"][slave]["service"]["port"]))
        replace = {
            "__port__" : self.config["service"]["port"],
            "__user__" : config["accounts"]["admin"]["username"],
            "__pass__" : config["accounts"]["admin"]["password"],
            "__port__" : self.config["service"]["port"],
            "__list_hosts__" : str(string)
        }
        fman.search_replace(config["add"]["hosts"], replace, config["add"]["tmp_hosts"])
        subprocess.call(["mongo", "--port", self.config["service"]["port"], config["add"]["tmp_hosts"]])

    # For slaves
    # Start service
    def start(self):
        self.get_keyfile()
        """mongod --fork --keyFile %s --replSet %s  --bind_ip 0.0.0.0 --port %s --logappend --logpath %s --dbpath %s --pidfilepath %s"""
        command = config["config"]["start_service"] % (
            KEYPATH,
            config["repl_name"],
            self.config["service"]["port"],
            self.config["data"]["log_path"],
            self.config["data"]["data_path"],
            self.config["data"]["pidfile"]
        )
        print(command)
        subprocess.call(command.split())

# Mongo()