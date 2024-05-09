import base64
import re

from cryptography.fernet import Fernet

AES_KEY = b"YjPv5whLFa_59KGjG6ZpOblWvHmgqTxQmjnb4oCvkq0="

#TODO @arthurazs: usar eval ao inves de regex para construir o objeto
def extract_fingerprint(str_sytem_info: str):
    fingerprint = re.search(r"fingerprint='([a-fA-F0-9]+)'", str_sytem_info)
    if fingerprint:
        return fingerprint.group(1)
    else:
        return None

def decrypt(information: str, aes_key: bytes) -> str:
    decrypted_information = ""
    try:
        encrypted_info_bytes = base64.urlsafe_b64decode(information)
        cipher = Fernet(aes_key)

        decrypted_key_bytes = cipher.decrypt(encrypted_info_bytes)
        decrypted_information = decrypted_key_bytes.decode()
    except Exception as e:
        print("Error decrypting information", e)
        decrypted_information = None

    print("\n[license_server] - Decript info: ", decrypted_information)

    return decrypted_information

def generate_activation_key(system_info: str, activation_days: int, aes_key: str) -> str:
    # Concatenando a data de expiração com o fingerprint da maquina cliente
    key_with_expiry = system_info + " "+str(activation_days)
    encoded_info = key_with_expiry.encode()  # Convertendo de string para bytes

    # Criptografando a chave combinada usando AES
    cipher = Fernet(aes_key)
    encrypted_key = cipher.encrypt(encoded_info)

    # Convertendo a chave criptografada em uma representação hexadecimal
    activation_key = base64.urlsafe_b64encode(encrypted_key).decode()
    return activation_key

def main():
    print("KEY GENERATOR started...")
    client_system_info = input("\nWrite the client system_information code: ")
    decrypted_information = decrypt(client_system_info, AES_KEY)

    client_fingerprint = extract_fingerprint(decrypted_information)
    expiry_days = int(input("\nEnter the number of days until expiration: "))

    activation_key = generate_activation_key(client_fingerprint, expiry_days, AES_KEY)
    print("\nHere is your activation key: ", activation_key)

if __name__ == "__main__":
    main()
