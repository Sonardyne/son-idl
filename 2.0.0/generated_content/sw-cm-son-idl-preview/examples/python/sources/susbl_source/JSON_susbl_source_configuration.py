import sonardyne_api as son
import time

with son.WrapperJsonTcp('0.0.0.0', 8103) as wrapper:  
    print(wrapper.set_configuration(son.SusblSourceConfiguration(input_data_port=son.DataPortReference(set_uid=son.UniqueID(name="External Control")))))