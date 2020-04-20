import time
from datetime import datetime


class EraAst:
    """Handles the AST recoring file - reads and writes.

    Each ASTERIX datablock preceeds 8bytes of header.

    | ast file structure:   |
    |-----------------------|
    | 8 bytes block header  |
    | asterix data block    |
    | 8 bytes block header  |
    | asterix data block    |
    | ...                   |


    | ast header (8 bytes): |                                          |
    |-----------------------|------------------------------------------|
    | 0                     | type (1 byte)                            |
    | 1                     | subtype (1 byte)                         |
    | 2 - 3                 | length (2 bytes, little endian)          |
    | 4 - 7                 | unix epoch time (4 bytes, little endian) |

    Header:
      1B    1B    2B   4B
    |type|subtype|len|time|asx-msg|
                     |---len------|


    """

    def __init__(self, file, mode):
        """Initiates the ast file for reading or writing.

        If mode is 'r' read, the file is open.
        Pointer is set to first byte after file header.
        If mode is 'w' write, the file is created.

        Parameters:
            file (str): file name
            mode (str): {'r', 'w'} mode of file - either read: 'r' or write 'w'
        """

        self.file = file
        if mode == 'r':
            self.position = 0
        if mode == 'w':
            pass

    def get_records(self):
        """Provides ASTERIX records in chunks as denote by the record header
        
        Returns:
            record (bytes): asterix data record
            timestamp (int): unix epoch time
        """

        with open(self.file, "rb") as f:
            f.seek(self.position, 0)
            while True:
                astheader = f.read(8)
                if not astheader:
                    break
                self.position += 8
                length = int.from_bytes(astheader[2:4], byteorder='little')

                # unix epoch time
                t_stamp = int.from_bytes(astheader[4:8], byteorder='little')

                record = f.read(length-4)  # 4 bytes of time are included
                self.position += length

                yield record, t_stamp

    def write_record(self, record, *argv):
        """Write header and datablock to a file. If timestamp (unix epoch time) provided as argv those are used.
            If not provided, current time is used.

        Parameters:
            record (bytes): asterix record
            *argv (int): optional, timestamp in unix epoch time
        """
        stamp = 0
        if argv:
            stamp = argv[0]
        else:
            stamp = int(time.time())
        with open(self.file, "ab") as f:

            # header
            header = bytearray(int('0x00', 16).to_bytes(2, "little"))
            TYPE = 0x38
            SUBTYPE = 0x00
            header[0] = TYPE
            header[1] = SUBTYPE

            f.write(TYPE.to_bytes(1, byteorder='little'))
            f.write(SUBTYPE.to_bytes(1, byteorder='little'))
            f.write((len(record)+4).to_bytes(2, byteorder='little'))
            f.write(stamp.to_bytes(4, byteorder='little'))
            
            # asterix data
            f.write(record)


def main():
    rfile = EraAst('./data/sample.ast', 'r')
    wfile = EraAst('./data/out.rec', 'w')

    g = rfile.get_records()
    while g:
        try:
            rrr, t_stamp = next(g)

            wfile.write_record(rrr, t_stamp)
            # wfile.write_record(rrr)
        except StopIteration:
            print('End of file.')
            break


if __name__ == "__main__":
    main()
