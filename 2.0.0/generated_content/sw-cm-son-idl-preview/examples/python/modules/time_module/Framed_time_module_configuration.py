import sonardyne_api as son

with son.WrapperFramedTcp('0.0.0.0', 8103) as wrapper:  
    print(wrapper.set_configuration(son.TimeModuleConfiguration(
        input_time_sources=son.TimeSourceInputReferences(
            input_ntp_time_source=son.NtpTimeSourceReference(set_uid=son.UniqueID(name="NTP Time Source")),
            input_zda_time_source=son.ZdaTimeSourceReference(set_none=True),
            input_pps_time_source=son.PpsTimeSourceReference(set_none=True)
        )
    )))