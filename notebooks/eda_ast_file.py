
from atm import asterix


def read_block_header(f):
    era_header = f.read(8)
    print('time', int.from_bytes(era_header[4:8], byteorder='little'))
    if len(era_header) < 8:
        return False
    return era_header


def read_data_block(f):
    astheader = f.read(3)
    length = int.from_bytes(astheader[1:3], byteorder='big')
    f.seek(-3, 1)
    data = f.read(length)
    print('---------------------')
    return length, data


decoder = asterix.AsterixDecoderPD.AsterixDecoder(20, version='1_7')

with open("data/sample.ast", "rb") as f:


    hdr = read_block_header(f)
    length, data = read_data_block(f)
    decoder.load_data(data)
    # res = decoder.get_result()
    # print(res[20][0]['140'])
    print(length)

    hdr = read_block_header(f)
    length, data = read_data_block(f)
    decoder.load_data(data)
    # res = decoder.get_result()
    # print(res[20][0]['140'])
    print(length)


    # while hdr:
    for i in range(0, 10):
        hdr=read_block_header(f)
        if not hdr:
            break
        length, data = read_data_block(f)
        decoder.load_data(data)
        res = decoder.get_result()
        print(res[20][0]['140'])
        if length == 0:
            break
        # read_data_block(f)


