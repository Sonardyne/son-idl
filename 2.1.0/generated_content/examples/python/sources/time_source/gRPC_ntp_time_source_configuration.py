import sonardyne_api as son

with son.WrapperGrpc('0.0.0.0', 8103) as wrapper:  
    print(wrapper.set_configuration(son.NtpTimeSourceConfiguration(ntp_server_ip_address="230.229.228.227")))