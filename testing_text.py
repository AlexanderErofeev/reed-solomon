from reed_solomon import ReedSolomon


def string_to_int_array(string):
    return [ord(char) for char in string]


def int_array_to_string(int_array):
    return ''.join(chr(i) for i in int_array)


if __name__ == '__main__':
    message = "Hello World!"

    rs = ReedSolomon(n=len(message) + 4, k=len(message))

    message_array = string_to_int_array(message)
    print("Коды символов сообщения:", message_array)

    encoded = rs.encode(message_array)
    print("Коды символов закодированного сообщения:", encoded)

    # Симуляция ошибок
    encoded[2] = 0
    encoded[14] = 0
    print("Коды символов закодированного сообщения с ошибками:", encoded)

    decoded = rs.decode(encoded)
    print("Исправленные коды символов сообщения:", decoded)

    decoded_message = int_array_to_string(decoded)
    print("Декодированное сообщение:", decoded_message)
