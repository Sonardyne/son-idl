import json, socket
    
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect(('0.0.0.0', 8103))
socket.sendall(json.dumps(
{
    "@type": "type.googleapis.com/sonardyne.api.common.envelope.RequestEnvelope",
    "requests": [
        {
            "@type": "type.googleapis.com/sonardyne.api.services.observation_service.ObservationEnvelope",
            "observationMessages": [
                {
                    "@type": "type.googleapis.com/sonardyne.api.sources.xpos_source.XposSourceObservation",
                    "xposData": {
                        "timeOfValidity": {
                            "commonTimeSeconds": 1772209964.022302
                        },
                        "horizontalPositionUncertaintyMetres": 0.5,
                        "depthUncertaintyMetres": 1.0,
                        "source": "XPOS_SOURCE_GNSS"
                    }
                }
            ]
        }
    ]
}, indent=4).encode())

socket.sendall(json.dumps(
{
    "@type": "type.googleapis.com/sonardyne.api.common.envelope.RequestEnvelope",
    "requests": [
        {
            "@type": "type.googleapis.com/sonardyne.api.services.observation_service.ObservationEnvelope",
            "observationMessages": [
                {
                    "@type": "type.googleapis.com/sonardyne.api.services.observation_service.ObservationSubscriptionRequest",
                    "observationSubscriptions": [
                        {
                            "matchingCriteria": {
                                "matchTypeNameSuffix": "XposSourceObservation"
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