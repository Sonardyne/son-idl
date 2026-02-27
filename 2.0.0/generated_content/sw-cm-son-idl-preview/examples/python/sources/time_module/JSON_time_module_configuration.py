import sonardyne_api as son
import time

with son.WrapperJsonTcp('0.0.0.0', 8103) as wrapper:  
    print(wrapper.set_configuration(son.TimeModuleConfiguration(
        input_time_sources=son.TimeSourceInputReferences(
            input_ntp_time_source=son.NtpTimeSourceReference(set_none=True),
            input_zda_time_source=son.ZdaTimeSourceReference(set_any=True),
            input_pps_time_source=son.PpsTimeSourceReference(set_none=True)
        )
    )))