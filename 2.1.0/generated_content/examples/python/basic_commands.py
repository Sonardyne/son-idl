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

import sonardyne_api as son

with son.WrapperGrpc('0.0.0.0', 8103) as wrapper:  # Device IP address & gRPC port:
    # Adds ethernet ports.
    wrapper.send_command(son.EthernetPortListCommandAddPort(ethernet_port=son.EthernetPort(source_port=8130, tcp_server=son.TcpServerParameters())))
    wrapper.send_command(son.EthernetPortListCommandAddPort(ethernet_port=son.EthernetPort(source_port=8136, tcp_client=son.TcpClientParameters(server_ip_address="192.168.179.135"))))
    wrapper.send_command(son.EthernetPortListCommandAddPort(ethernet_port=son.EthernetPort(source_port=8132, udp_socket=son.UdpSocketParameters(destination_ip_address="192.168.179.135"))))
    # Deletes ethernet ports.
    wrapper.send_command(son.EthernetPortListCommandRemovePort(uid_to_delete=son.UniqueID(name="TCP-8130")))
    wrapper.send_command(son.EthernetPortListCommandRemovePort(source_port_to_delete=8136))
    # Updates a serial port's Baud rate.
    wrapper.send_command(son.SerialPortListCommandUpdatePort(serial_port=son.SerialPort(uid=son.UniqueID(name="Serial A1"), baud_rate=son.SerialPort.BAUD_RATE_9600)))
    # Performs a hard reset.
    wrapper.send_command(son.AhrsAlgorithmCommandReset())
