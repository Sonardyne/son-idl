import sonardyne_api as son

with son.WrapperGrpc('0.0.0.0', 8103) as wrapper:  
    print(wrapper.set_configuration(son.NetworkModuleConfiguration(
        subnet_mask="255.255.255.0",
        ip_address_list=son.IPAddressList(ip_addresses=["192.168.179.56"]),
        gateway_ip="192.168.179.1",
        dhcp_enabled=False
    )))