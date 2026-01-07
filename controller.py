from encryptor import Encryptor


class Controller:
    def __init__(self):
        self.encryptor = Encryptor()

    def run(self):
        if not self.encryptor.text_set:
            self.set_text()
        else:
            self.encryptor.encrypt()

    def set_text(self):
        if not self.encryptor.text_set:
            print("Input text to encrypt:")
            self.encryptor.set_plaintext(input())
