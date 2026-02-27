import sonardyne_api as son

with son.WrapperFramedTcp('0.0.0.0', 8103) as wrapper:  
    print(wrapper.set_configuration(son.DvlAlgorithmConfiguration(
        dvl_rate=son.DvlRate(value=son.DvlRate.DvlRateEnum.DVL_RATE_ENUM_FIXED_5HZ),
        dvl_mode=son.DvlMode(value=son.DvlMode.DVL_MODE_ENUM_DVL),
        adcp_parameters=son.DvlAdcpParameters(
            number_of_cells=son.BoundedUInt32(value=100),
            preferred_cell_width_metres=son.BoundedDouble(value=0.1),
            pings_to_average=son.BoundedUInt32(value=10),
            dvl_adcp_ping_ratio=son.BoundedUInt32(value=10),
            velocity_limit=son.AdcpVelocityLimit(value=son.AdcpVelocityLimit.ADCP_VELOCITY_LIMIT_ENUM_STANDARD)
        ),
        input_trigger_parameters=son.DvlInputTriggerParameters(
            input_trigger_port=son.TriggerPortReference(set_uid=son.UniqueID(name="Trigger A1")),
            input_trigger_edge=son.TRIGGER_EDGE_RISING,
            input_trigger_delay_seconds=son.BoundedDouble(value=0.1)
        )
    )))