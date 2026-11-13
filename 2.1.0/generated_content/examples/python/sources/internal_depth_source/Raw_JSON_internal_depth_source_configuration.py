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
                "@type": "type.googleapis.com/sonardyne.api.sources.internal_depth_source.InternalDepthSourceConfiguration",
                "manualDepthOffsetMetres": 1.0,
                "pressureToDepthConversion": "PRESSURE_TO_DEPTH_CONVERSION_FIXED_SCALING"
            }
        }
    ]
}, indent=4).encode())

