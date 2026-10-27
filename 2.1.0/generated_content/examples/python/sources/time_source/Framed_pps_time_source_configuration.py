import sonardyne_api as son

with son.WrapperFramedTcp('0.0.0.0', 8103) as wrapper:  
    print(wrapper.set_configuration(son.PpsTimeSourceConfiguration(input_trigger_port=son.TriggerPortReference(set_any=True))))