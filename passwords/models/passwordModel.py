from django.db import models
from ..utils.encryption import PasswordEncryptor

ENCRYPTION_CHOICES = [
    ('bcrypt', 'Bcrypt'),
    ('sha256', 'SHA-256'),
    ('fernet', 'Fernet'),
    ('aes', 'AES'),
]

class Password(models.Model):
    service = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    hashed_password = models.CharField(max_length=255)
    encryption_method = models.CharField(max_length=10, choices=ENCRYPTION_CHOICES)

    def set_password(self, password):
        self.hashed_password = PasswordEncryptor.hash_password(password, self.encryption_method)

    def check_password(self, password):
        return PasswordEncryptor.check_password(password, self.hashed_password, self.encryption_method)

    def get_decrypted_password(self):
        if self.encryption_method == 'fernet':
            return PasswordEncryptor.decrypt_password(self.hashed_password)
        elif self.encryption_method == 'aes':
            return PasswordEncryptor.decrypt_password_aes(self.hashed_password)
        else:
            raise ValueError("Este método de encriptación no admite desencriptación.")

    def __str__(self):
        return f"{self.service} - {self.encryption_method}"
