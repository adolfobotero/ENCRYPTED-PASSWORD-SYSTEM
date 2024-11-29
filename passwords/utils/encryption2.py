from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64
import bcrypt
import hashlib
from cryptography.fernet import Fernet
from django.conf import settings

class PasswordEncryptor:
    @staticmethod
    def hash_password(password: str, method: str) -> str:
        if method == 'bcrypt':
            salt = bcrypt.gensalt()
            return bcrypt.hashpw(password.encode(), salt).decode()
        elif method == 'sha256':
            # Hash simple con SHA-256 (sin salt por simplicidad; podrías añadirlo si es necesario)
            return hashlib.sha256(password.encode()).hexdigest()
        elif method == 'fernet':
            cipher = Fernet(settings.SECRET_KEY.encode())
            return cipher.encrypt(password.encode()).decode()
        elif method == 'aes':
            key = base64.urlsafe_b64decode(settings.SECRET_KEY)
            # key = settings.SECRET_KEY.encode()  # Se usa la clave secreta de Django como clave para AES
            cipher = AES.new(key, AES.MODE_CBC)
            iv = cipher.iv
            ciphertext = cipher.encrypt(pad(password.encode(), AES.block_size))
            # Retorna el IV y el texto cifrado concatenados y codificados en base64
            return base64.b64encode(iv + ciphertext).decode()
        else:
            raise ValueError("Método de encriptación no soportado.")

    @staticmethod
    def check_password(password: str, hashed_password: str, method: str) -> bool:
        if method == 'bcrypt':
            return bcrypt.checkpw(password.encode(), hashed_password.encode())
        elif method == 'sha256':
            return hashlib.sha256(password.encode()).hexdigest() == hashed_password
        elif method == 'fernet':
            try:
                decrypted_password = PasswordEncryptor.decrypt_passwordferner(hashed_password)
                return decrypted_password == password
            except Exception:
                return False
        elif method == 'aes':
            
            # Para AES no hay "check_password" directo, por lo que se desencripta y compara
            decrypted_password = PasswordEncryptor.decrypt_password(hashed_password)
            return decrypted_password == password
        else:
            raise ValueError("Método de verificación no soportado.")

    @staticmethod
    def decrypt_password(encrypted_password: str) -> str:
        data = base64.b64decode(encrypted_password)
        iv = data[:AES.block_size]
        ciphertext = data[AES.block_size:]
        key = base64.urlsafe_b64decode(settings.SECRET_KEY)
        # key = settings.SECRET_KEY.encode()  # Usamos la misma clave para desencriptar
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size).decode()
        return plaintext
    
    @staticmethod
    def decrypt_passwordferner(hashed_password: str) -> str:
        cipher = Fernet(settings.SECRET_KEY.encode())
        return cipher.decrypt(hashed_password.encode()).decode()
