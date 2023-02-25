import hashlib
import base58


def base58_to_eth_address(base58_address):
    # декодирование base58-адреса
    decoded = base58.b58decode(base58_address)

    # удаление контрольной суммы
    raw_address = decoded[:-4]

    # удаление префикса из байтового адреса
    prefix_bytes = raw_address[:2]

    # преобразование байтов в hex-строку
    prefix_hex_digest = prefix_bytes.hex()

    # удаление префикса из хеша
    hex_digest = prefix_hex_digest[2:] + raw_address[2:].hex()

    # добавление префикса 0x к hex-строке
    eth_address = "0x" + hex_digest

    return eth_address


def eth_address_to_base58(eth_address):
    # удаление префикса 0x из hex-строки адреса
    hex_string = eth_address[2:]

    # преобразование hex-строки в байты
    byte_array = bytes.fromhex(hex_string)

    # добавление префикса к байтовому адресу
    prefix_bytes = b"\x01" + byte_array

    # добавление контрольной суммы к байтовому адресу
    checksum = hashlib.sha256(hashlib.sha256(
        prefix_bytes).digest()).digest()[:4]
    raw_address = prefix_bytes + checksum

    # преобразование байтового адреса в base58-строку
    base58_address = base58.b58encode(raw_address)

    return base58_address.decode()


def face_encoding_to_address(face_encoding):
    # преобразование кодировки лица в строку
    face_encoding_str = ",".join(str(val) for val in face_encoding)

    # создание хеша SHA256 из строки кодировки лица
    hash_object = hashlib.sha256(face_encoding_str.encode())
    hex_digest = hash_object.hexdigest()

    # добавление префикса к хешу
    prefix_hex_digest = "01" + hex_digest

    # преобразование hex-строки в байты
    prefix_bytes = bytes.fromhex(prefix_hex_digest)

    # создание контрольной суммы
    checksum = hashlib.sha256(hashlib.sha256(
        prefix_bytes).digest()).digest()[:4]

    # добавление контрольной суммы к префиксу
    raw_address = prefix_bytes + checksum

    # преобразование байтового адреса в строку в формате base58
    address = base58.b58encode(raw_address)

    print('addr_decode', address.decode())

    eth_address = base58_to_eth_address(address.decode())
    print("to eth", eth_address)

    base58_address = eth_address_to_base58(eth_address)
    print("from eth", base58_address)

    print("original", face_encoding)

    print("recover encodings from direct address",
          address_to_face_encoding(address.decode()))

    print("recover encodings from recover address",
          address_to_face_encoding(base58_address))

    return address.decode()


def address_to_face_encoding(address):
    # преобразование base58-строки адреса в байты
    raw_address = base58.b58decode(address)

    # проверка контрольной суммы
    prefix_bytes = raw_address[:-4]
    checksum = raw_address[-4:]
    expected_checksum = hashlib.sha256(
        hashlib.sha256(prefix_bytes).digest()).digest()[:4]
    if checksum != expected_checksum:
        raise ValueError("Invalid address: incorrect checksum")

    # удаление префикса из байтового адреса
    prefix_bytes = prefix_bytes[1:]

    # преобразование байтов в hex-строку
    prefix_hex_digest = prefix_bytes.hex()

    # удаление префикса из хеша
    hex_digest = prefix_hex_digest[2:]

    # разбиение хеша на список значений
    hash_list = [int(hex_digest[i:i+2], 16)
                 for i in range(0, len(hex_digest), 2)]

    # преобразование списка значений в список чисел с плавающей точкой
    face_encoding = [val / 1000 for val in hash_list]

    return face_encoding
