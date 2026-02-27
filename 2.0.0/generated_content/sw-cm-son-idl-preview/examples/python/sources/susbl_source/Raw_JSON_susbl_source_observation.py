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
                    "@type": "type.googleapis.com/sonardyne.api.sources.susbl_source.SusblSourceObservation",
                    "psimssbTelegram": {
                        "timeOfValidity": {
                            "commonTimeSeconds": 1772207940.4380164
                        },
                        "coordinateType": "PSIMSSB_COORDINATE_SYSTEM_RADIANS",
                        "isValid": true,
                        "orientationType": "PSIMSSB_ORIENTATION_NORTH",
                        "softwareFilter": "PSIMSSB_SOFTWARE_FILTER_UNKNOWN",
                        "positionUncertaintyMetres": 1.0
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
                                "matchTypeNameSuffix": "SusblSourceObservation"
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