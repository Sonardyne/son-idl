import sonardyne_api as son

with son.WrapperFramedTcp('0.0.0.0', 8103) as wrapper:  
    print(wrapper.set_configuration(son.PowerPassPortListConfiguration(power_pass_ports=[
        son.PowerPassPort(power_pass_state=son.PowerPassPort.POWER_PASS_STATE_TRIPPED),
        son.PowerPassPort(power_pass_state=son.PowerPassPort.POWER_PASS_STATE_ENABLED)
    ])))