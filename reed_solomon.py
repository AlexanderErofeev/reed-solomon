import reedsolo


PRIMITIVE_POLY = 285  # неприводимый многочлен для GF(2^8)


class ReedSolomon:
    def __init__(self, n, k):
        self.n = n  # длина закодированного сообщения
        self.k = k  # длина исходного сообщения
        self.gf_exp, self.gf_log = self._init_galois_field()

    def _init_galois_field(self):
        # Инициализируем поле Галуа GF(2^8)
        gf_exp = [0] * 256
        gf_log = [0] * 256

        x = 1
        for i in range(256):
            gf_exp[i] = x
            gf_log[x] = i
            x *= 2
            if x > 255:
                x ^= PRIMITIVE_POLY

        print(gf_exp)
        print(gf_log)

        return gf_exp, gf_log

    def _gf_mul(self, x, y):
        # Умножение в поле Галуа
        return self.gf_exp[(self.gf_log[x] + self.gf_log[y]) % 255]

    # def gf_div(self, x, y):
    #     # Деление в поле Галуа
    #     if y == 0:
    #         raise ZeroDivisionError("Деление на 0 в поле Галуа")
    #     if x == 0:
    #         return 0
    #     return self.gf_exp[(self.gf_log[x] - self.gf_log[y]) % 255]
    #
    # def gf_poly_scale(self, poly, x):
    #     # Умножение полинома на скаляр
    #     return [self.gf_mul(c, x) for c in poly]
    #
    # def gf_poly_add(self, poly1, poly2):
    #     # Сложение двух полиномов
    #     diff = len(poly2) - len(poly1)
    #     if diff > 0:
    #         poly1 = [0] * diff + poly1
    #     elif diff < 0:
    #         poly2 = [0] * (-diff) + poly2
    #     return [(a ^ b) for a, b in zip(poly1, poly2)]

    def _gf_poly_mul(self, poly1: list[int], poly2: list[int]):
        # Умножение двух полиномов
        result = [0] * (len(poly1) + len(poly2) - 1)
        for i, a in enumerate(poly1):
            for j, b in enumerate(poly2):
                result[i + j] ^= self._gf_mul(a, b)
        return result

    def encode(self, message):
        """Кодирование сообщения"""
        if len(message) > self.k:
            raise ValueError("Длина сообщения превышает k")
        message = list(message) + [0] * (self.n - self.k)
        generator = self._rs_generator_poly(self.n - self.k)
        remainder = self._gf_poly_mod(message, generator)
        return [int(el) for el in message[:self.k] + remainder]

    def _rs_generator_poly(self, nsym):
        """Создание генератора полинома"""
        g = [1]
        for i in range(nsym):
            g = self._gf_poly_mul(g, [1, self.gf_exp[i]])
        return g

    def _gf_poly_mod(self, poly, divisor):
        """Остаток от деления полинома"""
        poly = poly[:]
        for i in range(len(poly) - len(divisor) + 1):
            coef = poly[i]
            if coef != 0:
                for j in range(len(divisor)):
                    poly[i + j] ^= self._gf_mul(coef, divisor[j])
        return poly[-len(divisor) + 1:]

    def decode(self, encoded_message):
        """
        Декодирует сообщение, исправляет ошибки и возвращает исходное сообщение.
        """
        if len(encoded_message) != self.n:
            raise ValueError(f"Длина кодового слова должна быть {self.n}")

        decoded = reedsolo.RSCodec(self.n - self.k).decode(encoded_message)
        return list(decoded[0])
