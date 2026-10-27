import sonardyne_api as son
import time
import random

with son.WrapperGrpc('0.0.0.0', 8103) as wrapper:  
    print(wrapper.set_configuration(son.SoundVelocitySourceConfiguration(
        input_sound_velocity_data_source_reference=son.SoundVelocityDataSourceReference(set_salinity_parts_per_thousand=100)))
    )
    print(wrapper.set_configuration(son.SoundVelocitySourceConfiguration(
        input_sound_velocity_data_source_reference=son.SoundVelocityDataSourceReference(set_manual_sound_velocity_metres_per_second=150)))
    )
    print(wrapper.set_configuration(son.SoundVelocitySourceConfiguration(
        input_sound_velocity_data_source_reference=son.SoundVelocityDataSourceReference(set_any_ethernet_port=True)))
    )
    print(wrapper.set_configuration(son.SoundVelocitySourceConfiguration(
        input_sound_velocity_data_source_reference=son.SoundVelocityDataSourceReference(set_any_external_control_port=True)))
    )