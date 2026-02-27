#
# MIT License
#
# Copyright (c) 2025 Sonardyne International Limited
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

class simple_binary_protocol:
    class MessageType:
        HNav = 0,
        XLHNav = 1,
        GoogleProtobufAny = 2

    class DecodedMessage:
        def __init__(self, payload, type, count):
            self.payload = payload
            self.type = type
            self.count = count

    proto_version = 0
    sync_byte_1 = 0xAA
    sync_byte_2 = 0xBF

    @staticmethod
    def encode(message, message_type, count):
        payload_size = len(message)
        header = bytes([simple_binary_protocol.sync_byte_1, simple_binary_protocol.sync_byte_2, simple_binary_protocol.proto_version, 0xff & message_type, message_type >> 8, 0xff & payload_size,
                        payload_size >> 8, count, 0xDE, 0xAD])
        result = header + message
        crc = simple_binary_protocol.__calculate_crc_16_X_25(result)
        return result + bytes([0xff & crc, (crc >> 8) & 0xff])

    @staticmethod
    def decode(bytes):
        bytes_size = len(bytes)
        if bytes_size < 12:
            return None
        if bytes[0] != simple_binary_protocol.sync_byte_1:
            raise Exception("InvalidSyncBytes")
        if bytes[1] != simple_binary_protocol.sync_byte_2:
            raise Exception("InvalidSyncBytes")
        if bytes[2] != simple_binary_protocol.proto_version:
            raise Exception("UnexpectedVersionNumber")
        message_size = bytes[5] | (bytes[6] << 8)
        if bytes_size < 12 + message_size:
            return None
        crc = bytes[10 + message_size] | (bytes[11 + message_size] << 8)
        expected_crc = simple_binary_protocol.__calculate_crc_16_X_25(bytes[:10 + message_size])
        if crc != expected_crc:
            raise Exception("BadChecksum")
        payload = bytes[10:10 + message_size]
        type = bytes[3] | (bytes[4] << 8)
        count = bytes[7]
        return simple_binary_protocol.DecodedMessage(payload, type, count)

    @staticmethod
    def __reflect(crc, bitnum):
        j = 1
        crc_out = 0
        i = 1 << (bitnum - 1)
        while i:
            if crc & i:
                crc_out |= j
            j <<= 1
            i >>= 1
        return crc_out

    @staticmethod
    def __calculate_crc_16_X_25(bytes):
        crc = 0xffff
        for c in bytes:
            c = simple_binary_protocol.__reflect(c, 8)
            j = 0x80
            while j != 0:
                bit = crc & 0x8000
                crc <<= 1
                if c & j:
                    bit ^= 0x8000
                if bit:
                    crc ^= 0x1021
                j >>= 1
        crc = simple_binary_protocol.__reflect(crc, 16)
        crc ^= 0xffff
        return crc & 0xffff
