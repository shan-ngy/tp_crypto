import logging
import base64
import hashlib
import dearpygui.dearpygui as dpg
from chat_client import ChatClient
from generic_callback import GenericCallback
from ciphered_gui import *
from cryptography.fernet import Fernet


class FernetGUI(CipheredGUI):

    def run_chat(self, sender, app_data) -> None:
        host = dpg.get_value("connection_host")
        port = int(dpg.get_value("connection_port"))
        name = dpg.get_value("connection_name")
        password = dpg.get_value("connection_password")
        self._log.info(f"Connexion {name}@{host}:{port}")
        
        self._callback = GenericCallback()

        self._client = ChatClient(host, port)
        self._client.start(self._callback)
        self._client.register(name)


        #Key derivation
        key_bytes = hashlib.sha256(password.encode()).digest()
        self._key = base64.b64encode(key_bytes)

        dpg.hide_item("connection_windows")
        dpg.show_item("chat_windows")
        dpg.set_value("screen", "Connecting")
        
    def encrypt(self, message) -> bytes:
        #encrypting the message
        fernet = Fernet(self._key)
        encrypted_message = fernet.encrypt(bytes(message, 'utf-8'))
        return encrypted_message
    
    def decrypt(self, message) -> str :
        encrypted_message = base64.b64decode(message['data']) 
        #Decrypting the message
        fernet= Fernet(self._key)
        decrypted_message = fernet.decrypt(encrypted_message).decode('utf8')
        return decrypted_message

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    # instanciate the class, create context and related stuff, run the main loop
    client = FernetGUI()
    client.create()
    client.loop()