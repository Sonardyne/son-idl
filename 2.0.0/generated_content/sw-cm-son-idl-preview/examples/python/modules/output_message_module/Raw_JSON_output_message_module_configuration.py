import json, socket
    
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect(('0.0.0.0', 8103))
socket.sendall(json.dumps(
{
    "@type": "type.googleapis.com/sonardyne.api.common.envelope.RequestEnvelope",
    "uid": 1,
    "requests": [
        {
            "@type": "type.googleapis.com/sonardyne.api.services.configuration_service.SetConfigurationRequest",
            "configuration": {
                "@type": "type.googleapis.com/sonardyne.api.modules.output_message_module.OutputMessageModuleConfiguration",
                "outputMessageList": {
                    "outputMessages": [
                        {
                            "outputMessageType": "OUTPUT_MESSAGE_TYPE_GGA",
                            "dataPortOutput": {
                                "setAnyEthernetPort": true
                            },
                            "rateHz": 10.0,
                            "remotePoint": {
                                "setUid": {
                                    "name": "Remote Point 2"
                                }
                            }
                        },
                        {
                            "outputMessageType": "OUTPUT_MESSAGE_TYPE_LNAV",
                            "dataPortOutput": {
                                "setAnyEthernetPort": true
                            },
                            "rateHz": 5.0,
                            "remotePoint": {
                                "setUid": {
                                    "name": "Common Reference Point"
                                }
                            }
                        }
                    ]
                }
            }
        }
    ]
}, indent=4).encode())

