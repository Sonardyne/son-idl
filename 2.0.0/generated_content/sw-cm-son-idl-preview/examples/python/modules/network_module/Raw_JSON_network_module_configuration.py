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
                "@type": "type.googleapis.com/sonardyne.api.modules.network_module.NetworkModuleConfiguration",
                "ipAddressList": {
                    "ipAddresses": [
                        "192.168.179.56"
                    ]
                },
                "subnetMask": "255.255.255.0",
                "gatewayIp": "192.168.179.1",
                "dhcpEnabled": false
            }
        }
    ]
}, indent=4).encode())

