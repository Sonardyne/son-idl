import json, socket
    
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect(('0.0.0.0', 8103))
socket.sendall(json.dumps(
{
    "@type": "type.googleapis.com/sonardyne.api.common.envelope.RequestEnvelope",
    "uid": 1,
    "requests": [
        {
            "@type": "type.googleapis.com/sonardyne.api.services.command_service.SendCommandRequest",
            "command": {
                "@type": "type.googleapis.com/sonardyne.api.modules.output_message_module.OutputMessageModuleCommandRemoveOutput",
                "outputMessage": {
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
                }
            }
        }
    ]
}, indent=4).encode())

