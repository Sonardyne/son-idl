import json, socket
    
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect(('0.0.0.0', 8103))
socket.sendall(json.dumps(
{
    "@type": "type.googleapis.com/sonardyne.api.common.envelope.RequestEnvelope",
    "uid": 1,
    "requests": [
        {
            "@type": "type.googleapis.com/sonardyne.api.services.configuration_service.GetConfigurationRequest",
            "matchingCriteria": {
                "matchTypeNameSuffix": "Configuration"
            }
        }
    ]
}, indent=4).encode())

socket.sendall(json.dumps(
{
    "@type": "type.googleapis.com/sonardyne.api.common.envelope.RequestEnvelope",
    "uid": 2,
    "requests": [
        {
            "@type": "type.googleapis.com/sonardyne.api.services.configuration_service.GetConfigurationRequest",
            "matchingCriteria": {
                "matchTypeNameSuffix": "SourceConfiguration"
            }
        }
    ]
}, indent=4).encode())

socket.sendall(json.dumps(
{
    "@type": "type.googleapis.com/sonardyne.api.common.envelope.RequestEnvelope",
    "requests": [
        {
            "@type": "type.googleapis.com/sonardyne.api.services.configuration_service.ConfigurationEnvelope",
            "configurationMessages": [
                {
                    "@type": "type.googleapis.com/sonardyne.api.services.configuration_service.ConfigurationSubscriptionRequest",
                    "configurationSubscriptions": [
                        {
                            "matchingCriteria": {
                                "matchTypeNameSuffix": "Configuration"
                            }
                        }
                    ]
                }
            ]
        }
    ]
}, indent=4).encode())

while True:
    if data := socket.recv(10240):
        print(data.decode())