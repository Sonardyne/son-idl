import sonardyne_api as son

with son.WrapperFramedTcp('0.0.0.0', 8103) as wrapper:  
    print(wrapper.set_configuration(son.InsAlgorithmConfiguration(
        is_gnss_enabled=True,
        is_xpos_enabled=False,
        is_external_depth_enabled=False,
        is_internal_depth_enabled=False,
        is_gnss_height_enabled=True
    )))