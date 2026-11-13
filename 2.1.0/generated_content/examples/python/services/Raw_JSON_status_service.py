import json, socket
    
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect(('0.0.0.0', 8103))
socket.sendall(json.dumps(
{
    "@type": "type.googleapis.com/sonardyne.api.common.envelope.RequestEnvelope",
    "uid": 1,
    "requests": [
        {
            "@type": "type.googleapis.com/sonardyne.api.services.status_service.StatusEnvelope",
            "statusMessages": [
                {
                    "@type": "type.googleapis.com/sonardyne.api.services.status_service.StatusSubscriptionRequest",
                    "statusSubscriptions": [
                        {
                            "matchingCriteria": {
                                "matchTypeNameSuffix": "InsAlgorithmStatus"
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