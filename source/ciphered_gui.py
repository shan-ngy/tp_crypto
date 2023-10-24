#TP

from basic_gui import *
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import os
import logging
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding, hashes
import base64
import dearpygui.dearpygui as dpg

from chat_client import ChatClient
from generic_callback import GenericCallback

# default values used to populate connection window

SALT = b"weshyaleskeufs"
LENGTH = 16
ITERATIONS = 480000
NB_BLOCK = 128

class CipheredGUI(BasicGUI):
    def __init__(self)->None:
        # constructor
        super().__init__()
        self._key = None


    def _create_connection_window(self)->None:
        # windows about connexion
        with dpg.window(label="Connection", pos=(200, 150), width=400, height=300, show=False, tag="connection_windows"):
            
            for field in ["host", "port", "name"]:
                with dpg.group(horizontal=True):
                    dpg.add_text(field)
                    dpg.add_input_text(default_value=DEFAULT_VALUES[field], tag=f"connection_{field}")
            
            #adding a password field
            dpg.add_text("password")      
            dpg.add_input_text(password=True,tag="connection_password")
            dpg.add_button(label="Connect", callback=self.run_chat)



    def run_chat(self, sender, app_data)->None:
        # callback used by the connection windows to start a chat session
        host = dpg.get_value("connection_host")
        port = int(dpg.get_value("connection_port"))
        name = dpg.get_value("connection_name")
        #adding password callback
        password = dpg.get_value("connection_password")
        self._log.info(f"Connecting {name}@{host}:{port}")

        self._callback = GenericCallback()

        self._client = ChatClient(host, port)
        self._client.start(self._callback)
        self._client.register(name)

        #Key Derivation function
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=LENGTH, salt=SALT, iterations=ITERATIONS)
        #Key derivation
        b_password = bytes(password, 'utf-8')
        self._key = kdf.derive(b_password)
        self._log.info(f"self.key {self._key}")
        
        dpg.hide_item("connection_windows")
        dpg.show_item("chat_windows")
        dpg.set_value("screen", "Connecting")

    def encrypt(self, message):

        #Creating a random vector
        iv = os.urandom(16)
        #Initializing the AES algorithm
        cipher = Cipher(algorithms.AES(self._key), modes.CTR(iv))
        self._encryptor = cipher.encryptor()

        #adding a padding
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_message = padder.update(bytes(message, "utf8")) + padder.finalize()

        #encrypting the message
        encrypted_message = self._encryptor.update(padded_message) + self._encryptor.finalize()
        return (iv, encrypted_message)

    def decrypt(self, message) -> str:
        iv = base64.b64decode(message[0]['data'])
        encrypted_message = base64.b64decode(message[1]['data'])
        cipher = Cipher(algorithms.AES(self._key), modes.CTR(iv),backend=default_backend())
        decryptor = cipher.decryptor()
        
        #Decrypting the message
        unpadder = padding.PKCS7(NB_BLOCK).unpadder()
        decrypted_message = decryptor.update(encrypted_message) + decryptor.finalize()
        return (unpadder.update(decrypted_message)+unpadder.finalize());decode()

    def recv(self)->None:
        #function called to get incoming messages and display them
        if self._callback is not None:
            for user, encrypted_message in self._callback.get():
                decrypted_message = self.decrypt(encrypted_message)
                self.update_text_screen(f"{user} : {decrypted_message}")
            self._callback.clear()

    def send(self, message)->None:
        # function called to send a message to all (broadcasting)
        encrypted_message = self.encrypt(message)
        self._client.send_message(encrypted_message)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    # instanciate the class, create context and related stuff, run the main loop
    client = CipheredGUI()
    client.create()
    client.loop()
