from reed_solomon import ReedSolomon


def file_to_int_array(file_path):
    with open(file_path, 'rb') as f:
        return list(f.read())

def int_array_to_file(int_array, output_path):
    with open(output_path, 'wb') as f:
        f.write(bytearray(int_array))


if __name__ == '__main__':
    # Параметры
    input_file = 'data/input.txt'
    encoded_file = 'data/encoded.bin'
    corrupted_file = 'data/corrupted.bin'
    decoded_file = 'data/decoded.txt'
    parity_symbols = 10  # Количество символов коррекции ошибок

    message_array = file_to_int_array(input_file)
    print("Исходные данные файла:", message_array)

    rs = ReedSolomon(n=len(message_array) + parity_symbols * 2, k=len(message_array))

    encoded = rs.encode(message_array)
    int_array_to_file(encoded, encoded_file)
    print("Закодированные данные файла:", encoded)

    # Симуляция ошибок в закодированном файле
    corrupted = encoded[:]
    corrupted[2] = 0
    corrupted[4] = 0
    int_array_to_file(corrupted, corrupted_file)
    print("Закодированные данные с ошибками:", corrupted)

    # Декодирование
    try:
        decoded = rs.decode(corrupted)
        int_array_to_file(decoded, decoded_file)
        print("Исправленные данные файла:", decoded)
    except Exception as e:
        print("Ошибка декодирования:", e)
