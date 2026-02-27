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
                "@type": "type.googleapis.com/sonardyne.api.sources.depth_source.DepthSourceConfiguration",
                "inputDepthDataSourceReference": {
                    "setUid": {
                        "name": "TCP-8110"
                    }
                },
                "leverArms": {
                    "forwardMetres": 1.5,
                    "starboardMetres": 2.0,
                    "downMetres": 3.2
                }
            }
        }
    ]
}, indent=4).encode())

