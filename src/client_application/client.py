# TODO @mesheo: implementar salt na criptografia sha256
import hashlib
import platform
from pathlib import Path
from time import sleep


# TODO @mesheo: implementar o dataclass para guardar as informacoes do machine_info
# para seguranca e impedir manipulacao do dado depois de retornar
def collect_system_info() -> dict[str, str]:
    system_info = platform.uname()

    return {
        "system": system_info.system,
        "node": system_info.node,
        "release": system_info.release,
        "version": system_info.version,
        "machine": system_info.machine,
        "processor": system_info.processor,
    }

def persist_activation_key(activation_key: str) -> None:
    file_path = "activation_key.txt"
    with Path(file_path).open("w") as file:
        file.write(activation_key)

def generate_activation_key(hash_system_info, encode_algorithm="sha256"):
    encoded_info = hash_system_info.encode()
    hash_object = hashlib.new(encode_algorithm, encoded_info)
    activation_key = hash_object.hexdigest()

    return activation_key

def verify_activation_key(activation_key, hash_system_info):
    if generate_activation_key(hash_system_info) == activation_key:
        return True
    return False

def encode_machine_info():
    machine_info = collect_system_info()

    machine_info_str = "\n".join([f"{key}: {value}" for key, value in machine_info.items()])
    hash_object = hashlib.sha256(machine_info_str.encode())
    hash_hex = hash_object.hexdigest()

    return hash_hex


if __name__ == "__main__":
    activated = False

    # TODO @mesheo: checar se ja esta ativado antes de perguntar ao usuario
    while not activated:
        option = int(input("\nChoose an option: \n1 - Activate Program\n2- Generate Machine Fingerprint\n"))
        activate_program = 1
        generate_machine_fingerprint = 2

        if option == activate_program:
            activation_key = input("Digite o código de ativação do NWATCH: ")
            if verify_activation_key(activation_key, encode_machine_info()):
                print("\nPROGRAMA ATIVADO\n----------------------")
                persist_activation_key(activation_key)
                activated = True

        if option == generate_machine_fingerprint:
            print("\naqui as infos da maquina: ", encode_machine_info())

    while activated:
        # TODO @mesheo: ficar checando se a chave esta valida (forcar erro no texto pra chave ser invalida)
        print("\nPROGRAMA RODANDO")
        sleep(4)
