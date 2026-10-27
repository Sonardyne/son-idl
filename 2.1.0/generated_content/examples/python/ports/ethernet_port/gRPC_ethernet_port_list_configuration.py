import sonardyne_api as son

with son.WrapperGrpc('0.0.0.0', 8103) as device: # SPRINT-Nav ip address & port
    print(device.set_configuration(son.EthernetPortListConfiguration(ethernet_ports=[
        son.EthernetPort(source_port=8110, tcp_server=son.TcpServerParameters()),
        son.EthernetPort(source_port=8111, tcp_client=son.TcpClientParameters(server_ip_address="192.168.179.60")),
        son.EthernetPort(source_port=8112, udp_socket=son.UdpSocketParameters(destination_ip_address="192.168.179.70")),
    ])))