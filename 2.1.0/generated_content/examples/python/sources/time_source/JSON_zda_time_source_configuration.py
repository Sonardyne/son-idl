import sonardyne_api as son

with son.WrapperJsonTcp('0.0.0.0', 8103) as wrapper:  
    print(wrapper.set_configuration(son.ZdaTimeSourceConfiguration(input_data_port=son.DataPortReference(set_any_ethernet_port=True))))