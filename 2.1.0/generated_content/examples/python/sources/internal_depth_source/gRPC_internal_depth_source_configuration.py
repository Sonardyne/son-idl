import sonardyne_api as son

with son.WrapperGrpc('0.0.0.0', 8103) as wrapper:  
    print(wrapper.set_configuration(son.InternalDepthSourceConfiguration(
        manual_depth_offset_metres=1,
        pressure_to_depth_conversion=son.PRESSURE_TO_DEPTH_CONVERSION_FIXED_SCALING
    )))