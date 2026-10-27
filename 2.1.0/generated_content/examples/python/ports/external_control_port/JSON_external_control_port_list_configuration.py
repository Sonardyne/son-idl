import sonardyne_api as son

with son.WrapperJsonTcp('0.0.0.0', 8103) as wrapper:  
    print(wrapper.get_configuration(son.ExternalControlPortListConfiguration))