import os
import sys
myewebssh_conf = os.environ['MYEWEBSSH_CONFIG']
mye_root = os.environ['MYE_ROOT']
myeconf_parser = os.environ['MYECONF_PARSER']
sys.path.insert(0, os.path.dirname(myeconf_parser))
myeconf_parser_name = os.path.splitext(os.path.basename(myeconf_parser))[0]
parser = __import__(myeconf_parser_name)

import subprocess
import codecs

from webssh.handler import *

SPFILE=os.environ['MYE_SCRIPTS_DIR']

# read config from file
myeconfig = parser.get_config(myewebssh_conf)

WS_CONF_SESS_NAME="webssh"
# get_value_decorator take arg1 to define the session
@parser.get_value_decorator(myeconfig, WS_CONF_SESS_NAME)
def wsconfig_value(keyword):
    try:
        return myeconfig[WS_CONF_SESS_NAME][keyword]
    except KeyError as e:
        logger.warning('Key Error: %s', keyword)

def check_lockfile(username, sid):
    lockfile_path = wsconfig_value("lockfile_path")
    lockfile_prefix = wsconfig_value("lockfile")
    lockfile = "{}/{}{}.lock".format(lockfile_path, lockfile_prefix, username)
    with open(lockfile, 'r') as lockfile:
        sid_infile = lockfile.read();

    if sid == sid_infile:
	logging.info("vis dev: sid match, sid = {}".format(sid))
	return True
    else:
        # logging in file, don't response sid_infile to client.
	logging.error("sid not match! user = {}, sid = {}, sid_infile = {}".format(username, sid, sid_infiile))
        raise InvalidValueError("sid not match! sid = {}".format(sid))


class MyeHandler(IndexHandler):

    # scripts file path
    SPFILE="/myewebssh/scripts/preprocess"

    def get_args(self):
        hostname = wsconfig_value('ssh_host')
        port = wsconfig_value('ssh_port')
        if isinstance(self.policy, paramiko.RejectPolicy): self.lookup_hostname(hostname, port)

        username = self.get_value('username')
        sid = self.get_value('sid')
        check_lockfile(username, sid)
        password = self.get_argument('password', u'')
        privatekey = self.get_user_key(username)
        if privatekey:
            pkey = self.get_pkey_obj(
                privatekey, password, self.privatekey_filename
            )
            password = None
        else:
            pkey = None

        args = (hostname, port, username, password, pkey)
        # record user login for audit
        logging.info(args)
        return args

    def get_user_key(self, username):
        # exec preprocess script first
        subprocess.call([self.SPFILE, username])
        key_fn = wsconfig_value('key_fn')
        kpath = "/home/{}/.ssh/{}".format(username, key_fn)
        self.privatekey_filename = kpath

        # read private key in utf-8 encoding
        with codecs.open(kpath, 'rb', encoding="utf-8") as keyfile:
            data = keyfile.read()

        # convert to utf-8
        #value = self.decode_argument(data, name=name).strip()
        #logging.debug("read public key from file: {}".format(data))
        return data


