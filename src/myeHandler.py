import subprocess
import codecs

from webssh.handler import *

class MyeHandler(IndexHandler):

    # scripts file path
    SPFILE="/myewebssh/scripts/preprocess"

    def get_args(self):
        hostname = self.get_hostname()
        port = self.get_port()
        if isinstance(self.policy, paramiko.RejectPolicy):
            self.lookup_hostname(hostname, port)
        username = self.get_value('username')
        password = self.get_argument('password', u'')
        #privatekey = self.get_privatekey()
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
        kpath = "/home/{}/.ssh/id_mye".format(username)
        self.privatekey_filename = kpath

        # read private key in utf-8 encoding
        with codecs.open(kpath, 'rb', encoding="utf-8") as keyfile:
            data = keyfile.read()

        # convert to utf-8
        #value = self.decode_argument(data, name=name).strip()
        #logging.debug("read public key from file: {}".format(data))
        return data


