import sonardyne_api as son

with son.WrapperJsonTcp('0.0.0.0', 8103) as wrapper:  
    print(wrapper.set_configuration(son.ExternalDepthSourceConfiguration(
        input_data_port=son.DataPortReference(set_uid=son.UniqueID(name="TCP-8110")),
        lever_arms=son.LeverArms(forward_metres=1.5, starboard_metres=2, down_metres=3.2),
        manual_depth_offset_metres=0,
        pressure_to_depth_conversion=son.PRESSURE_TO_DEPTH_CONVERSION_FIXED_SCALING
    )))