import json, socket
    
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect(('0.0.0.0', 8103))
socket.sendall(json.dumps(
{
    "@type": "type.googleapis.com/sonardyne.api.common.envelope.RequestEnvelope",
    "requests": [
        {
            "@type": "type.googleapis.com/sonardyne.api.services.comms_service.CommsEnvelope",
            "commsMessages": [
                {
                    "@type": "type.googleapis.com/sonardyne.api.services.comms_service.CommsSubscriptionRequest",
                    "commsSubscriptions": [
                        {
                            "matchingCriteria": {
                                "matchUids": [
                                    {
                                        "name": "TCP-8110"
                                    }
                                ]
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