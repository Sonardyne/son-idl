import sonardyne_api as son

with son.WrapperGrpc('0.0.0.0', 8103) as wrapper:  
    print(wrapper.set_configuration(son.AhrsAlgorithmConfiguration(
        coarse_position_latitude_radians=0.1,
        coarse_position_longitude_radians=0.2
    )))