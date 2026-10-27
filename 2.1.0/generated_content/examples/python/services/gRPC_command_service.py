import sonardyne_api as son

with son.WrapperGrpc('0.0.0.0', 8103) as wrapper:  
    wrapper.send_command(son.InsAlgorithmCommandReset())