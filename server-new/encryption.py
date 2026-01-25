from cryptography.fernet import Fernet
with open("key.key","rb") as f:
    keyinfo = f.read()
cipher_suite = Fernet(keyinfo)
def encryptFile(FileName):
    with open(FileName,"rb") as f:
        Original = f.read()
    encoded_file = cipher_suite.encrypt(Original)
    with open(FileName,"wb") as f:
        f.write(encoded_file)
    return encoded_file

def decryptFile(FileName):
    with open(FileName,"rb") as f:
        Encrypted = f.read()
    decoded_file = cipher_suite.decrypt(Encrypted)
    with open(FileName,"wb") as f:
        f.write(decoded_file)
    return decoded_file

def encryptString(string):
    encoded_string = cipher_suite.encrypt(bytes(string,"utf-8"))
    return encoded_string

def decryptString(string):
    decoded_Bytes = cipher_suite.decrypt(string)
    decoded_string = str(decoded_Bytes,"utf-8")
    return decoded_string