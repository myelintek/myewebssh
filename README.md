README - myewebssh
====

### introduction

myewebssh mainly leveraged an open source project, webssh, and modified 3 files to fit myelintek webssh usage.

myewebssh launches a webssh window for users of myelintek web portal without additional actions. For this purpose, myewebssh will deal with the key authentication part itself, including generating key pair if necessary.

#### sequence of launching myewebssh

myewebssh handles a webssh request as following:

1. send a "launch webssh" request from myelintek web portal and redirect to localhost:4200 with username
2. the index.html receive and pass the username to a connection function.
3. Try to look for the RSA key under home directory. If the key does not exist, automatically generate a pair of RSA key, named `id_mye`, in the .ssh directory under home of the user. Users are trusted at this moment because they have been authenticated while login to web portal.
4. authenticate user with key by paramiko.
5. connec to local sshd.
6. prepare websocket connection.
7. reply to client to build the web socket connection up.


#### [webssh](https://github.com/huashengdun/webssh)

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

hack 3 files of webssh:  `myelintek_setup.py`  `webssh/myeHandler.py`  `webssh/myelintek.py`
   - inherit from `handler.py` as `myeHandler.py` and hack the argument process function, `get_args()`, to fetch the private key from user home.
   - `myelintek.py` is used to register the myeHandler to handle the post request of '/'
   - `myelintek_setup.py` is used to build the wheel package

add 2 scripts:  preprocess `user_go`
   - preprocess is used to invoke su command and execute `user_go` as user
   - `user_go` is used to check the key existence, create new one if not exist. And also, checking the key is recorded in file `authorized_keys`, add to if not.


#### useful commands

- launh myewebssh
	- `wssh --port=4200 --fbidhttp=False --logging=debug`

#### Q & A
- authentication fail
	- check the key existence
    - check the key record in file `authorized_keys`
    - check the execution result of scripts: `/myewebssh/scripts/preprocess`


