from cryptography.fernet import Fernet

# Genera una clave para Fernet
fernet_key = Fernet.generate_key()

# Convierte la clave a formato de cadena (UTF-8) para usarla en la configuración de Django
print(fernet_key.decode())