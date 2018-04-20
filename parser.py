from struct import unpack

def parseByte(byteio):
    byte_buffer = byteio.read(1)
    return unpack('B', byte_buffer)[0]

def parseShort(byteio):
    byte_buffer = byteio.read(2)
    return unpack('H', byte_buffer)[0]

def parseInt(byteio):
    byte_buffer = byteio.read(4)
    return unpack('I', byte_buffer)[0]

def parseLong(byteio):
    byte_buffer = byteio.read(8)
    return unpack('L', byte_buffer)[0]

def parseULEB128(byteio):
    result = 0
    shift = 0
    while(True):
        byte = byteio.read(1)
        val = unpack('B', byte)[0]
        result |= (val & 0x7F) << shift
        if (val & 0x80) == 0:
            break
        shift += 7

    return result

# a single byte which will be either 0x00, indicating that the next two parts are not present,
# or 0x0b (decimal 11), indicating that the next two parts are present. 
# If it is 0x0b, there will then be a ULEB128, representing the byte length of the following string,
# and then the string itself, encoded in UTF-8.
def parseString(byteio):
    unicode_string = u''

    exists = unpack('B', byteio.read(1))[0]
    if exists == 0x00:
        return unicode_string
    elif exists == 0x0b:
        length = parseULEB128(byteio)
        string = unpack(str(length)+'s', byteio.read(length))[0]
        try:
            unicode_string = str(string, 'utf-8')
        except UnicodeDecodeError:
            print("Could not parse UTF-8 string, returning empty string.")

        return unicode_string