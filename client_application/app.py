import hashlib
import platform
from time import sleep

def collect_system_info():
    system_info = platform.uname()
    machine_info = {
        "system": system_info.system,
        "node": system_info.node,
        "release": system_info.release,
        "version": system_info.version,
        "machine": system_info.machine,
        "processor": system_info.processor
    }
    
    return machine_info

def persist_activation_key(activation_key):
    file_path = "activation_key.txt"
    with open(file_path, "w") as file:
        file.write(activation_key)

def generate_activation_key(hash_system_info, encode_algorithm='sha256'):
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

    machine_info_str = '\n'.join([f"{key}: {value}" for key, value in machine_info.items()])
    hash_object = hashlib.sha256(machine_info_str.encode())
    hash_hex = hash_object.hexdigest()
    
    return hash_hex


if __name__ == "__main__":
    activated = False
    while not activated:
        option = int(input("\nChoose an option: \n1 - Activate Program\n2- Generate Machine Fingerprint\n"))

        if option == 1:
            activation_key = input("Digite o código de ativação do NWATCH: ")
            if verify_activation_key(activation_key, encode_machine_info()):
                print("\nPROGRAMA ATIVADO\n----------------------")
                persist_activation_key(activation_key)
                activated = True
    
        if option == 2:
            print("\naqui as infos da maquina: ", encode_machine_info())
    
    while activated:
        
        print("\nPROGRAMA RODANDO")
        sleep(4)