import logging
import base64
from fernet_gui import *
import time
from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken

TTL = 30

class TimeFernetGUI(FernetGUI):
    def __init__(self) -> None:
        super().__init__()

    def encrypt(self, message) -> bytes:
        #Encrypting by an object Fernet with a TTL
        fernet = Fernet(self._key)  
        n_time = int(time.time())  
        new_message = bytes(message, 'utf-8') 
        encrypted_message = fernet.encrypt_at_time(new_message, n_time+TTL)  
        return encrypted_message
    
    def decrypt(self, message) -> str:
        #Decrypting the message (Fernet object verifies the TTL)
        try:
            encrypted_message = base64.b64decode(message['data'])
            fernet = Fernet(self._key)
            n_time = int(time.time())
            decrypted_message = fernet.decrypt_at_time(encrypted_message, TTL, n_time).decode('utf8')
            return decrypted_message
        except InvalidToken:
            self._log.warning(InvalidToken.__name__)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    # instanciate the class, create context and related stuff, run the main loop
    client = TimeFernetGUI()
    client.create()
    client.loop()
