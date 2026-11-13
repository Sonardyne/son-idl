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
                "@type": "type.googleapis.com/sonardyne.api.modules.device_module.DeviceModuleCommandShutdown"
            }
        }
    ]
}, indent=4).encode())

