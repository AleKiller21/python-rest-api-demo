import re
import heapq

CHUNKSIZE = 100
OUTPUTBUFFER = 50
INPUTBUFFER = 20
NEXTEMAIL = 1
REGEX = "[a-z0-9.]+@[a-z0-9-]+([.][a-z]+)+"

class Item:
    def __init__(self, value, segment, consumed, file):
        self.value = value
        self.segment = segment
        self.consumed = consumed
        self.file = file

    def __lt__(self, other):
        return self.value < other.value

class Sort:
    'This class allows you to sort alphabetically a file of email addresses'
    def __init__(self, filename):
        self.__filename = filename
        self.output_file = "output.txt"
        self.__file = None

    def sort(self):
        'This method does the actual sorting'
        files_written = 0

        with open(self.__filename) as self.__file:
            files_written = self.__construct_sub_files()
            self.__merge(files_written)

    def __construct_sub_files(self):
        counter = 0
        files_written = 0
        chunk = []

        for line in self.__file:
            chunk.append(line.lower())
            counter += 1

            if counter != CHUNKSIZE:
                continue
            self.__add_new_line(chunk)
            self.__write_to_chunk(chunk, files_written)
            counter = 0
            chunk.clear()
            files_written += 1

        if counter > 0:
            self.__add_new_line(chunk)
            self.__write_to_chunk(chunk, files_written)
            files_written += 1

        return files_written

    def __add_new_line(self, chunk):
        email = chunk[len(chunk) - 1]
        if email[len(email) - 1] != "\n":
            chunk[len(chunk) - 1] = email + "\n"

    def __merge(self, files_written):
        heap = []

        self.__build_min_heap(files_written, heap)
        self.__write_sorted_mail_output(heap)

    def __write_to_chunk(self, chunk, files_written):
        filename = "temp" + str(files_written) + ".txt"
        self.__filter(chunk)
        chunk.sort()
        if not len(chunk):
            return
        sub_file = open(filename, "w")
        sub_file.writelines(chunk)
        sub_file.close()

    def __filter(self, chunk):
        i = 0
        while i < len(chunk):
            if re.match(REGEX, chunk[i]):
                i += 1
            else:
                chunk.remove(chunk[i])

    def __build_min_heap(self, files_written, heap):
        for i in range(files_written):
            filename = "temp" + str(i) + ".txt"
            file = open(filename)
            emails = self.__read_temp_file(file)
            consumed = INPUTBUFFER
            value = emails[0]
            item = Item(value, emails, consumed, file)
            heapq.heappush(heap, item)

    def __read_temp_file(self, file):
        buffer = []

        for i in range(INPUTBUFFER):
            line = file.readline()
            if line == "":
                break
            else:
                buffer.append(line)

        return buffer

    def __write_sorted_mail_output(self, heap):
        output = []
        output_file = open(self.output_file, "w")

        while len(heap) > 0:
            email = self.__get_email(heap)
            if len(output) >= OUTPUTBUFFER:
                output_file.writelines(output)
                output.clear()
            output.append(email)

        if len(output) > 0:
            output_file.writelines(output)

        output_file.close()

    def __get_email(self, heap):
        item = heap[0]
        email = item.value
        item.segment.remove(email)

        if not len(item.segment):
            item.segment = self.__read_temp_file(item.file)
            if not len(item.segment):
                item.file.close()
                heapq.heappop(heap)
                return email

        item.value = item.segment[0]
        heapq.heapreplace(heap, item)
        return email
