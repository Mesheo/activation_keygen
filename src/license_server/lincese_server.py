# TODO @mesheo: implementar salt na criptografia sha256
import hashlib


def generate_activation_key(system_info, encode_algorithm="sha256"):
    encoded_info = system_info.encode()  # Convertendo a string para bytes
    hash_object = hashlib.new(encode_algorithm, encoded_info)  # Criando um objeto de hash
    activation_key = hash_object.hexdigest()  # Convertendo o hash como uma string hexadecimal

    return activation_key

if __name__ == "__main__":
    print("KEY GENERATOR started...")
    system_info = input("Write your computer identification code: ")
    print("Here is your activation key: ", generate_activation_key(system_info))
