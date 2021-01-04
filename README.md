# kelchat

**A simple terminal TCP chatroom with messages encrypted with TLS**

## **Requires**
* Python 3

## **Usage/Installation**
* I have included sample *cert.pem* and *key.pem* files. Please generate your own using the following openssl command:
```
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365
```
**NB: Please check the following link for more information on generating self-signed certificates: https://stackoverflow.com/questions/10175812/how-to-create-a-self-signed-certificate-with-openssl**

* Once you have generated your own *cert.pem* and *key.pem*, go to __line 23__ of *client.py*:
```
client_s = ssl_context.wrap_socket(client, server_hostname='ALLANON')
```
and change the *server_hostname='ALLANON'* to **your own** hostname.

* Also go to __line 15__ of *client.py*:
```
SSL_CERT = os.path.abspath('cert.pem')
```
and make sure you set the correct path to your cert.pem file (or leave it as it is if the cert.pem file is in the same directory as your client.pem)

* Go to __lines 15,16__ of your *server.py* file:
```
 15  SSL_KEY = os.path.abspath('key.pem')
 16  SSL_CERT = os.path.abspath('cert.pem')
```
and make sure you set the correct path to your cert.pem and key.pem files (or leave them as they are if they are in the same directory as your server.py)

###### **Tested on**
* Linux Mint 19/20
* Manjaro 20.2
* Kali Linux
