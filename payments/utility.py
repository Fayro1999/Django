from Crypto.Cipher import AES
import base64

def pad(text):
    pad_len = 16 - (len(text) % 16)
    return text + chr(pad_len) * pad_len

def encrypt_aes_ecb_base64(plain_text, key):
    key_bytes = key.encode('utf-8')
    padded_text = pad(plain_text)
    cipher = AES.new(key_bytes, AES.MODE_ECB)
    encrypted = cipher.encrypt(padded_text.encode('utf-8'))
    encoded = base64.b64encode(encrypted).decode('utf-8')
    return encoded
