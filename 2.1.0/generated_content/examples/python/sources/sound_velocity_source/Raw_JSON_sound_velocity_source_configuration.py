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
                "@type": "type.googleapis.com/sonardyne.api.sources.sound_velocity_source.SoundVelocitySourceConfiguration",
                "inputSoundVelocityDataSourceReference": {
                    "setSalinityPartsPerThousand": 100.0
                }
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
            "@type": "type.googleapis.com/sonardyne.api.services.configuration_service.SetConfigurationRequest",
            "configuration": {
                "@type": "type.googleapis.com/sonardyne.api.sources.sound_velocity_source.SoundVelocitySourceConfiguration",
                "inputSoundVelocityDataSourceReference": {
                    "setManualSoundVelocityMetresPerSecond": 150.0
                }
            }
        }
    ]
}, indent=4).encode())

socket.sendall(json.dumps(
{
    "@type": "type.googleapis.com/sonardyne.api.common.envelope.RequestEnvelope",
    "uid": 3,
    "requests": [
        {
            "@type": "type.googleapis.com/sonardyne.api.services.configuration_service.SetConfigurationRequest",
            "configuration": {
                "@type": "type.googleapis.com/sonardyne.api.sources.sound_velocity_source.SoundVelocitySourceConfiguration",
                "inputSoundVelocityDataSourceReference": {
                    "setAnyEthernetPort": true
                }
            }
        }
    ]
}, indent=4).encode())

socket.sendall(json.dumps(
{
    "@type": "type.googleapis.com/sonardyne.api.common.envelope.RequestEnvelope",
    "uid": 4,
    "requests": [
        {
            "@type": "type.googleapis.com/sonardyne.api.services.configuration_service.SetConfigurationRequest",
            "configuration": {
                "@type": "type.googleapis.com/sonardyne.api.sources.sound_velocity_source.SoundVelocitySourceConfiguration",
                "inputSoundVelocityDataSourceReference": {
                    "setAnyExternalControlPort": true
                }
            }
        }
    ]
}, indent=4).encode())

