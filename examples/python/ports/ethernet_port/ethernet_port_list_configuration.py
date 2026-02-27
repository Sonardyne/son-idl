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

with son.WrapperGrpc('0.0.0.0', 8103) as device: # SPRINT-Nav ip address & port
    print(device.set_configuration(son.EthernetPortListConfiguration(ethernet_ports=[
        son.EthernetPort(source_port=8110, tcp_server=son.TcpServerParameters()),
        son.EthernetPort(source_port=8111, tcp_client=son.TcpClientParameters(server_ip_address="192.168.179.60")),
        son.EthernetPort(source_port=8112, udp_socket=son.UdpSocketParameters(destination_ip_address="192.168.179.70")),
    ])))
