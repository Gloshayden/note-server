from cryptography.fernet import Fernet
with open("key.key","rb") as f:
    keyinfo = f.read()
cipher_suite = Fernet(keyinfo)
def encryptString(string, key):
    encoded_text = cipher_suite.encrypt(string)
    return encoded_text

def decryptString(string, key):
    decoded_text = cipher_suite.decrypt(string)
    return decoded_text