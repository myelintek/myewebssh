README - myewebssh
====

### introduction

myewebssh mainly leveraged an open source project, webssh, and add 5 files to fit myelintek webssh usage.

myewebssh launches a webssh window for users of myelintek web portal without additional actions. For this purpose, myewebssh will deal with the key authentication part itself, including generating key pair if necessary.

#### sequence of launching myewebssh

myewebssh handles a webssh request as following:

1. send a "launch webssh" request from myelintek web portal and redirect to myewebssh web server in netloc:4200 with username
2. the myewebssh web server response to client by rendering the myeIndex.html
3. client send a post request to myewebssh server with the username and session id.
4. check user name and session id recorded in lockfile which was writen by myelindl web portal.
5. Try to look for the RSA key under home directory. If the key does not exist, automatically generate a pair of RSA key, named `id_mye`, in the .ssh directory under home of the user. Users are trusted at this moment because they have been authenticated while login to web portal.
6. authenticate user with key by paramiko.
7. connec to local sshd.
8. prepare websocket connection and return a websocket id.
9. reply websocket id to client to build the web socket connection up.


#### [webssh](https://github.com/huashengdun/webssh) features:

- SSH password authentication supported, including empty password.
- SSH public-key authentication supported, including DSA RSA ECDSA Ed25519 keys.
- Encrypted keys supported.
- Fullscreen terminal supported.
- Terminal window resizable.
- Auto detect the ssh server's default encoding.
- Modern browsers including Chrome, Firefox, Safari, Edge, Opera supported.


### integration

#### system architecture

- myelintek web portal: flask web server
- myewebssh: tornado web server
	- listen on "localhost:4200" in default, port number could be changed by command option.

#### implement

hack 5 files of webssh:  `myelintek_setup.py`  `webssh/myeHandler.py`  `webssh/myelintek.py` `templates/myeIndex.html` `static/js/myeMain.js`
   - `myeHandler.py` inherit from `handler.py` and hack the argument process function, `get_args()`, to fetch the private key from user home.
   - `myelintek.py` is used to register the myeHandler to handle the post request of '/'
   - `myelintek_setup.py` is used to build the wheel package.
   - `templates/myeIndex.html` load related js files.
   - `static/js/myeMain.js` automatically post request to myewebssh server while window loaded.

add 2 scripts:  `preprocess` `user_go`
   - `preprocess` is used to invoke su command to execute `user_go` as user
   - `user_go` is responsible for checking the key existence, create new one if not exist. And also, checking the key is recorded in file `authorized_keys`, add to if not.


#### useful commands

- build and install myewebssh package
    - `bash build.sh install`
- launh myewebssh
	- `wssh --port=4200 --fbidhttp=False --logging=debug`

### config
config file use to set configs and share to myelindl web portal for setting up environment.
please note that you should copy this config from myewebssh to myelindl webportal if you change any.
- lock file path and name: lock file records session id and identifies by username.
    - `lockfile_path`=/tmp
    - `lockfile`=wslock\_
- ssh service on the server: connect to a specified sshd server, we connect to localhost right now.
    - `ssh_host`=localhost
    - `ssh_port`=22
- key file name: file name of RSA key pair
    - `key_fn`=id\_mye
- myewebssh web server url: ws\_host should be the hostname of web server, but ignore in this version.
ws\_host and ws\_port constructs the redirect address.
    - `ws_host`=localhost
    - `ws_port`=1220


#### Q & A
- authentication fail
	- check the key existence
    - check the key record in file `authorized_keys`
    - check the execution result of scripts: `/myewebssh/scripts/preprocess`


