import base64
import platform
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from time import sleep

import machineid
from cryptography.fernet import Fernet

AES_KEY = b"YjPv5whLFa_59KGjG6ZpOblWvHmgqTxQmjnb4oCvkq0="

@dataclass(frozen=True, kw_only=True)
class SystemInfo:
    system: str
    node: str
    release: str
    version: str
    machine: str
    processor: str
    fingerprint: str

@dataclass(frozen=True, kw_only=True)
class DecryptedKey:
    machineid: str
    activation_days: int
    key_expiration_date: datetime

class StartOptions(Enum):
    ACTIVATE_PROGRAM = 1
    GENERATE_FINGERPRINT = 2
class ActivationStatus(Enum):
    INVALID = "Activation key is not valid"
    EXPIRED = "Activation key has expired"
    ACTIVE = "Activation key is active"
    NOT_FOUND = "Activation key not found"
    KEY_EXPIRED = "Activation key has expired based on key expiration date"

def collect_system_info() -> SystemInfo:
    system_info = platform.uname()

    return SystemInfo(
        system=system_info.system,
        node=system_info.node,
        release=system_info.release,
        version=system_info.version,
        machine=system_info.machine,
        processor=system_info.processor,
        fingerprint=machineid.hashed_id(),
    )

def encrypt(system_info: SystemInfo, aes_key: bytes) -> str:
    byte_info = str(system_info).encode()

    cipher = Fernet(aes_key)
    encrypted_info = cipher.encrypt(byte_info)

    base64_encrypted_info = base64.urlsafe_b64encode(encrypted_info).decode()

    return base64_encrypted_info

def decrypt_activation_key(encrypted_key: str, aes_key: bytes) -> DecryptedKey:
    try:
        encrypted_key_bytes = base64.urlsafe_b64decode(encrypted_key)

        cipher = Fernet(aes_key)
        decrypted_key_bytes = cipher.decrypt(encrypted_key_bytes)

        descrypt_key_data = decrypted_key_bytes.decode().split()
    except Exception as e:
        print("[Client] ERROR decrypting activation code: ", e)
        descrypt_key_data = ["None", "0", "1970-01-01"]

    return DecryptedKey(
        machineid=descrypt_key_data[0],
        activation_days=int(descrypt_key_data[1]),
        key_expiration_date=datetime.strptime(descrypt_key_data[2], "%Y-%m-%d")
    )

def persist_data(data: str, file_path: str) -> None:
    with Path(file_path).open("w") as file:
        file.write(str(data))

def verify_activation() -> ActivationStatus:
    activation_key = ""
    expiration_date = ""

    try:
        with open("activation_key.txt") as file:
            activation_key = file.read()
    except FileNotFoundError:
        return ActivationStatus.NOT_FOUND

    decrypted_key = decrypt_activation_key(activation_key, AES_KEY)

    if datetime.now() > decrypted_key.key_expiration_date:
        return ActivationStatus.KEY_EXPIRED

    try:
        with open("expiration_date.txt") as file:
            expiration_date = datetime.strptime(file.read(), "%Y-%m-%d %H:%M:%S.%f")
    except FileNotFoundError:
        expiration_date = datetime.now() + timedelta(days = decrypted_key.activation_days)
        persist_data(expiration_date, "expiration_date.txt")

    print("Expiration_date: ", expiration_date)

    if machineid.hashed_id() != decrypted_key.machineid:
        return ActivationStatus.INVALID
    elif datetime.now() >= expiration_date:
        return ActivationStatus.EXPIRED
    elif datetime.now() < expiration_date:
        return ActivationStatus.ACTIVE

    return ActivationStatus.NOT_FOUND

if __name__ == "__main__":
    activated = False
    activation_status = verify_activation()

    if activation_status == ActivationStatus.ACTIVE:
        print("PROGRAMA JÁ INICIOU ATIVADO!")
        activated = True
    elif activation_status == ActivationStatus.INVALID:
        print("Ativação corrompida. O programa será desativado.")
    elif activation_status == ActivationStatus.EXPIRED:
        print("Ativação expirou. O programa será desativado.")
    elif activation_status == ActivationStatus.NOT_FOUND:
        print("Ativação ainda não realizada.")

    while not activated:
        option = int(input(
            "\nChoose an option: \n1 - Activate Program\n2 - Generate Machine Fingerprint\n"))

        if option == StartOptions.ACTIVATE_PROGRAM:
            activation_key = input("Digite o código de ativação do NWATCH: ")
            persist_data(activation_key, "activation_key.txt")

            activation_status = verify_activation()
            if activation_status == ActivationStatus.ACTIVE:
                print("\nPROGRAMA ATIVADO\n----------------------")
                activated = True

        if option == StartOptions.GENERATE_FINGERPRINT:
            system_info = collect_system_info()
            encrypted_system_info = encrypt(system_info, AES_KEY)

            print("\n[Client] encrypted_system_info", encrypted_system_info)

    while activated:
        activation_status = verify_activation()

        if activation_status == ActivationStatus.ACTIVE:
            print("\nPROGRAMA RODANDO")
            sleep(4)
        else:
            print("\n ACTIVATION_STATUS: ", activation_status)
            print("Ativação expirou ou arquivo de ativação não encontrado. O programa será desativado.")

            activated = False
            break
