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
                    "@type": "type.googleapis.com/sonardyne.api.sources.time_source.ZdaTimeSourceObservation",
                    "zdaData": {
                        "currentUtcTimeSeconds": 1772207941.182004
                    }
                }
            ]
        }
    ]
}, indent=4).encode())

