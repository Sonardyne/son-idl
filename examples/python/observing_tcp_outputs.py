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

    # Sets 6 ethernet ports for use on the device. 4 TCP servers, 1 TCP client & 1 UDP socket.
    print("creating tcp servers...")
    wrapper.set_configuration(son.EthernetPortListConfiguration(ethernet_ports=[
        son.EthernetPort(source_port=8110, tcp_server=son.TcpServerParameters()),
        son.EthernetPort(source_port=8111, tcp_server=son.TcpServerParameters()),
        son.EthernetPort(source_port=8112, tcp_server=son.TcpServerParameters()),
        son.EthernetPort(source_port=8113, tcp_server=son.TcpServerParameters()),
        son.EthernetPort(source_port=8114, tcp_client=son.TcpClientParameters(server_ip_address="192.168.179.50")),
        son.EthernetPort(source_port=8115, udp_socket=son.UdpSocketParameters(destination_ip_address="192.168.179.60"))
    ]))

    # Outputs GGA messages at 100Hz on TCP-8110.
    print("setting GGA output...")
    wrapper.set_configuration(son.OutputMessageModuleConfiguration(
        output_message_list=son.OutputMessageList(
            output_messages=[
                son.OutputMessage(
                    output_message_type=son.OutputMessageType.OUTPUT_MESSAGE_TYPE_GGA,
                    rate_hz=100.0,
                    remote_point=son.RemotePointReference(set_uid=son.UniqueID(name="Common Reference Point")),
                    data_port_output=son.DataPortReference(set_uid=son.UniqueID(name="TCP-8110"))
                )
            ]
        )
    ))

    # Listens to data on the TCP-8110 port.
    comms_stream = wrapper.open_comms_stream(son.CommsSubscriptionRequest(
        comms_subscriptions=[
            son.CommsSubscription(matching_criteria=son.MatchingCriteria(match_uids=[son.UniqueID(name="TCP-8110")]))
        ]
    ))
    try:
        while True:
            for message in comms_stream.recv():
                if isinstance(message, son.DataPortComms):
                    print("->" if message.data_direction == son.DATA_DIRECTION_OUTPUT else "<-", message.data)
    except KeyboardInterrupt:
        pass

    # Removes any output messages.
    wrapper.set_configuration(son.OutputMessageModuleConfiguration(
        output_message_list=son.OutputMessageList(
            output_messages=[]
        )
    ))
