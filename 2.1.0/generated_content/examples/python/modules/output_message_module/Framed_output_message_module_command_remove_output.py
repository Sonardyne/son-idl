import sonardyne_api as son

with son.WrapperFramedTcp('0.0.0.0', 8103) as wrapper:  
    wrapper.set_configuration(son.OutputMessageModuleConfiguration(
        output_message_list=son.OutputMessageList(
            output_messages=[
                son.OutputMessage(
                    output_message_type=son.OutputMessageType.OUTPUT_MESSAGE_TYPE_GGA,
                    rate_hz=10.0,
                    remote_point=son.RemotePointReference(set_uid=son.UniqueID(name="Remote Point 2")),
                    data_port_output=son.DataPortReference(set_any_ethernet_port=True)
                ),
                son.OutputMessage(
                    output_message_type=son.OutputMessageType.OUTPUT_MESSAGE_TYPE_LNAV,
                    rate_hz=5.0,
                    remote_point=son.RemotePointReference(set_uid=son.UniqueID(name="Common Reference Point")),
                    data_port_output=son.DataPortReference(set_any_ethernet_port=True)
                )
            ]
        )
    ))
    wrapper.send_command(son.OutputMessageModuleCommandRemoveOutput(
        output_message=son.OutputMessage(uid=son.UniqueID(name="LNAV Output Message"))
    ))