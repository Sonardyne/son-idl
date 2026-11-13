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
                "@type": "type.googleapis.com/sonardyne.api.port_lists.ethernet_port_list.EthernetPortListConfiguration",
                "ethernetPorts": [
                    {
                        "sourcePort": 8110,
                        "tcpServer": {}
                    },
                    {
                        "sourcePort": 8111,
                        "tcpClient": {
                            "serverIpAddress": "192.168.179.60"
                        }
                    },
                    {
                        "sourcePort": 8112,
                        "udpSocket": {
                            "destinationIpAddress": "192.168.179.70"
                        }
                    }
                ]
            }
        }
    ]
}, indent=4).encode())

