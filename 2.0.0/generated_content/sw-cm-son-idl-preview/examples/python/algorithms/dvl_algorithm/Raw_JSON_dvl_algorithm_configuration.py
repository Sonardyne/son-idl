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
                "@type": "type.googleapis.com/sonardyne.api.algorithms.dvl_algorithm.DvlAlgorithmConfiguration",
                "dvlRate": {
                    "value": "DVL_RATE_ENUM_FIXED_5HZ"
                },
                "dvlMode": {
                    "value": "DVL_MODE_ENUM_DVL"
                },
                "inputTriggerParameters": {
                    "inputTriggerPort": {
                        "setUid": {
                            "name": "Trigger A1"
                        }
                    },
                    "inputTriggerEdge": "TRIGGER_EDGE_RISING",
                    "inputTriggerDelaySeconds": {
                        "value": 0.1
                    }
                },
                "adcpParameters": {
                    "numberOfCells": {
                        "value": 100
                    },
                    "preferredCellWidthMetres": {
                        "value": 0.1
                    },
                    "pingsToAverage": {
                        "value": 10
                    },
                    "dvlAdcpPingRatio": {
                        "value": 10
                    },
                    "velocityLimit": {
                        "value": "ADCP_VELOCITY_LIMIT_ENUM_STANDARD"
                    }
                }
            }
        }
    ]
}, indent=4).encode())

