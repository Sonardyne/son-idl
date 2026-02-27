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
                    "@type": "type.googleapis.com/sonardyne.api.sources.sound_velocity_source.SoundVelocitySourceObservation",
                    "soundVelocityData": {
                        "timeOfValidity": {
                            "commonTimeSeconds": 1772209964.7356508
                        },
                        "soundVelocityMetersPerSecond": 1495.7
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
                                "matchTypeNameSuffix": "SoundVelocitySourceObservation"
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