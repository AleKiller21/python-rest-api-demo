
class Steganography:
    'Class used for steganography. Its primary focus are bmp images'
    def __init__(self):
        self._message_length_bits = 16
        self._bitmap_data_start = 54
        self._byte_length = 8
        self._max_byte = 128

    def hide_message(self, image, message):
        'Hides the given message inside the image'
        message_bytes = bytearray(message, "utf8")
        offset = self.__set_message_length(len(message), image)
        count = 0

        for letter in message_bytes:
            while count < self._byte_length:
                bit = letter & (self._max_byte >> count)
                if bit == 0:
                    offset = self.__set_lsb(image, bit, offset)
                else:
                    offset = self.__set_lsb(image, 1, offset)
                if offset >= len(image):
                    break
                count += 1

            count = 0
            if offset >= len(image):
                break

    def extract_message(self, image):
        'Returns the message hidden on the image'
        size = self.__get_message_length(image)
        offset = self._bitmap_data_start + self._message_length_bits
        message_data = bytearray(size)

        for i in range(size):
            buffer = bytearray(self._byte_length)

            for counter in range(self._byte_length):
                buffer[counter] = self.__get_lsb(image[offset])
                offset += 1
                if offset >= len(image):
                    break
            message_data[i] = self.__make_byte(buffer)

            if offset >= len(image):
                break

        return message_data

    def __get_message_length(self, image):
        offset = self._bitmap_data_start
        message_length_buffer = bytearray(self._message_length_bits)

        for i in range(self._message_length_bits):
            message_length_buffer[i] = self.__get_lsb(image[offset])
            offset += 1

        return self.__get_decimal_representation(message_length_buffer)

    def __get_decimal_representation(self, byte_buffer):
        size = pos = 0

        for byte in byte_buffer:
            if byte == 1:
                size += (1 << pos)
            pos += 1

        return size

    def __set_message_length(self, size, image):
        byte_buffer = self.__get_binary_representation(size)
        offset = self._bitmap_data_start

        for byte in byte_buffer:
            offset = self.__set_lsb(image, byte, offset)

        return offset

    def __get_binary_representation(self, size):
        buffer = bytearray(self._message_length_bits)
        remainder = size
        counter = 0

        while size >= 1:
            remainder = size % 2
            size = size // 2

            if remainder != 0:
                buffer[counter] = 1
            counter += 1

        return buffer

    def __set_lsb(self, image, target, offset):
        if self.__get_lsb(image[offset]) == target:
            return offset + 1

        if target == 1:
            image[offset] += 1
        else:
            image[offset] -= 1

        return offset + 1

    def __get_lsb(self, num):
        if num % 2 == 1:
            return 1
        return 0

    def __make_byte(self, byte_buffer):
        value = pos = 0
        i = len(byte_buffer) - 1

        while i >= 0:
            if byte_buffer[i] == 1:
                value += (1 << pos)
            pos += 1
            i -= 1

        return value
