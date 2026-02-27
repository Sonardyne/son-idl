import sonardyne_api as son

with son.WrapperFramedTcp('0.0.0.0', 8103) as wrapper:  
    print(wrapper.send_command(son.InsAlgorithmCommandReset()))