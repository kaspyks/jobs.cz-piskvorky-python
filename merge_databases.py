#!/usr/bin/env python3

import sqlite3
from paramiko import SSHClient
from scp import SCPClient
import os
import sys


def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))


tmp_file_name = "/tmp/db_tmp.db"
script_folder = get_script_path()
ssh = SSHClient()
ssh.load_system_host_keys()
ssh.connect('rasta.cloud')
# SCPCLient takes a paramiko transport as an argument
scp = SCPClient(ssh.get_transport())
scp.get('~/scripts/piskvorky_python/centralDB.db', tmp_file_name)
scp.close()

con3 = sqlite3.connect(str(get_script_path()) + "/centralDB.db")
con3.execute("ATTACH '" + tmp_file_name + "' as dba")

con3.execute("BEGIN")
for row in con3.execute("SELECT * FROM dba.sqlite_master WHERE type='table'"):
    if row[1] != "games" and row[1] != "sqlite_sequence":
        sql_prepare = "CREATE TABLE IF NOT EXISTS `{}` \
(id INTEGER PRIMARY KEY AUTOINCREMENT, data VARCHAR (5000));".format(row[1])
        con3.execute(sql_prepare)
    combine = "INSERT OR IGNORE INTO `" + row[1] + "` SELECT * FROM `dba`.`" + row[1] + "`"
    print(combine)
    con3.execute(combine)
con3.commit()
con3.execute("detach database dba")

os.remove(tmp_file_name)
