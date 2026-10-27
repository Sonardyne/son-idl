import sonardyne_api as son

with son.WrapperJsonTcp('0.0.0.0', 8103) as wrapper:  
    print(wrapper.set_configuration(son.DvlSensorConfiguration(
        is_raw_logging_enabled=False
    )))