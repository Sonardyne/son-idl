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
                "@type": "type.googleapis.com/sonardyne.api.port_lists.serial_port_list.SerialPortListConfiguration",
                "serialPorts": [
                    {
                        "baudRate": "BAUD_RATE_9600"
                    },
                    {
                        "baudRate": "BAUD_RATE_38400"
                    }
                ]
            }
        }
    ]
}, indent=4).encode())

