import socket
import struct

TCPport = 44818
UDPport = 2222
UDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDP.bind(("0.0.0.0", UDPport))
# UDP.setblocking(0)


module1_IP = "193.0.1.1"

Module1_Request_start = "00"
Module1_Request_stop = "00"
Module1_Request_reset = "00"
Module2_Request_start = "00"
Module2_Request_stop = "00"
Module2_Request_reset = "00"


def get_module1_data(module1_IP):
    global Module1_currentset, Module1_Enable, Module1_Request_start, Module1_Request_stop, Module1_Request_reset, module1
    Module1_Register = bytes.fromhex(
        "65000400000000000000000000000000000000000000000001000000"
    )
    Module1_TCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Module1_TCP.connect((module1_IP, TCPport))
    Module1_TCP.sendall(Module1_Register)
    Module1_TCPmessage = Module1_TCP.recv(1024)
    Module1_Session = Module1_TCPmessage[4:8].hex()
    Module1_Identity = bytes.fromhex(
        "%s%s%s"
        % (
            "6f001600",
            Module1_Session,
            "00000000000000000000000000000000000000000000020000000000b2000600010220012401",
        )
    )
    Module1_TCP.sendall(Module1_Identity)
    Module1_TCPmessage = Module1_TCP.recv(1024)
    module1ID_1 = Module1_TCPmessage[54:55].hex()
    module1ID_2 = Module1_TCPmessage[55:56].hex()
    module1 = int((module1ID_2 + module1ID_1), base=16)
    Module1_ForwardOpen = bytes.fromhex(
        "%s%s%s"
        % (
            "6f004000",
            Module1_Session,
            "00000000000000000000000000000000000000000000020000000000b20030005402200624010a0a0200550e0300550e550edafa0df0ad8b00000000c0c300002e46c0c300007a40010320042c702c64",
        )
    )
    Module1_ForwardClose = bytes.fromhex(
        "%s%s%s"
        % (
            "6f002800",
            Module1_Session,
            "00000000000000000000000000000000000000000000020000000000b20018004e02200624010a0a550edafa0df0ad8b030020042c702c64",
        )
    )
    Module1_Enable = "00"
    Module1_Seq = "00000000"
    Module1_CIPSeq = "0000"
    #Module1_currentset = struct.pack("f", (module1_CurSet) * 0.1)
    #Module1_CurSet = "".join(["%02x" % b for b in Module1_currentset])
    Module1_CMD = "%s%s%s%s%s" % (
        Module1_Enable,
        Module1_Request_start,
        Module1_Request_stop,
        Module1_Request_reset,
        "0000000000000000000000000000000000000000000000000000000000000000",
    )
    # print(Module1_CMD)
    Module1_TCP.sendall(Module1_ForwardOpen)
    Module1_TCPmessage = Module1_TCP.recv(1024)
    print(Module1_TCPmessage.hex())
    Module1_O2TID = Module1_TCPmessage[44:48].hex()
    Module1_T2OID = Module1_TCPmessage[48:52].hex()
    # time.sleep(0.1)
    k = 0
    while k <= 1:
        try:
            Module1_O2T = bytes.fromhex(
                "%s%s%s%s%s%s%s"
                % (
                    "020002800800",
                    Module1_O2TID,
                    Module1_Seq,
                    "b1002e00",
                    Module1_CIPSeq,
                    "01000000",
                    Module1_CMD,
                )
            )
            UDP.sendto(Module1_O2T, (module1_IP, UDPport))
            try:
                Module1_T2O, M1addr = UDP.recvfrom(150)
                Module1_Seq = Module1_T2O[10:14].hex()
                Module1_CIPSeq = Module1_T2O[18:20].hex()
                k = k + 1
            except socket.timeout as e:
                print("Module1 UDP Timeout")
                k = 5
        except:
            print("Module1_O2T error")
    Module1_TCP.sendall(Module1_ForwardClose)
    Module1_TCPmessage = Module1_TCP.recv(1024)
    Module1_Request_reset = "00"
    Module1_TCP.close()
    if M1addr[0] == module1_IP:
        return Module1_T2O


while True:
    module1_data = get_module1_data(module1_IP)
    print(module1_data)