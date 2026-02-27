import sonardyne_api as son

with son.WrapperFramedTcp('0.0.0.0', 8103) as wrapper:  
    print(wrapper.send_command(son.OutputMessageModuleCommandRemoveOutput(
        output_message=
        son.OutputMessage(
            output_message_type=son.OutputMessageType.OUTPUT_MESSAGE_TYPE_GGA,
            rate_hz=10.0,
            remote_point=son.RemotePointReference(set_uid=son.UniqueID(name="Remote Point 2")),
            data_port_output=son.DataPortReference(set_any_ethernet_port=True)
        )
    )))