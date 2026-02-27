import sonardyne_api as son

with son.WrapperFramedTcp('0.0.0.0', 8103) as wrapper:  
    print(wrapper.set_configuration(son.DepthSourceConfiguration(
        input_depth_data_source_reference=son.DepthDataSourceReference(
            set_uid=son.UniqueID(name="TCP-8110")
        ),
        lever_arms=son.LeverArms(forward_metres=1.5, starboard_metres=2, down_metres=3.2)
    )))