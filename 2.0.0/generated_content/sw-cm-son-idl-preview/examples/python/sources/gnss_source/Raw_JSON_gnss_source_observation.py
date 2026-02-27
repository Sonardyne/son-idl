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
                    "@type": "type.googleapis.com/sonardyne.api.sources.gnss_source.GnssSourceObservation",
                    "ggaTelegram": {
                        "timeOfValidity": {
                            "commonTimeSeconds": 1772207939.695202
                        },
                        "hdop": 0.5,
                        "numberOfSatellites": 10,
                        "fixQuality": "FIX_QUALITY_GNSS_FIX"
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
                                "matchTypeNameSuffix": "GnssSourceObservation"
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