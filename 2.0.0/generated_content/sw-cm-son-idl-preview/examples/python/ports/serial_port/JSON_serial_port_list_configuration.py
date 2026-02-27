import sonardyne_api as son

with son.WrapperJsonTcp('0.0.0.0', 8103) as wrapper:  
    print(wrapper.set_configuration(son.SerialPortListConfiguration(serial_ports=[
        son.SerialPort(baud_rate=son.SerialPort.BAUD_RATE_9600),
        son.SerialPort(baud_rate=son.SerialPort.BAUD_RATE_38400),
    ])))