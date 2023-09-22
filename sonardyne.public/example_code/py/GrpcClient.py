#Copyright 2023 Sonardyne

#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
#documentation files (the “Software”), to deal in the Software without restriction, including without limitation the
#rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
#permit persons to whom the Software is furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
#Software.

#THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
#WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
#COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import grpc
import service_pb2_grpc
import version_pb2
import configuration_pb2

def SetExampleState(stub):
    # Create a device configuration. This contains configurations for Reset, Aiding, Sound Velocity, and DVL
    config = configuration_pb2.Configuration()
    
    # Each type of configuration is stored as a list. This is reserved for future use as not all units support multiple configurations.
    
    # Create and add a reset config to perform a soft reset
    reset_config = configuration_pb2.ResetConfiguration(reset_type="SOFT_RESET")
    config.reset_configurations.append(reset_config)

    # Create and add an aiding config to enable GNSS aiding and disable USBL aiding
    aiding_config_enable_gnss = configuration_pb2.AidingConfiguration(enable_gnss="ENABLED", enable_usbl="DISABLED")
    config.aiding_configurations.append(aiding_config_enable_gnss)
    
    # Create and add a sound velocity config to set the SV source to salinity-derived and set the SV salinity to an arbitrary value
    sv_config_salinity_derived = configuration_pb2.SoundVelocityConfiguration(sound_velocity_type="INTERNAL_SALINITY", manual_salinity_value=32.1)
    config.sound_velocity_configurations.append(sv_config_salinity_derived)
    
    # Create and add a DVL config to set the update rate to an arbitrary choice
    dvl_config_1Hz = configuration_pb2.DopplerVelocityLogConfiguration(update_rate="FIXED_1HZ")
    config.doppler_velocity_configurations.append(dvl_config_1Hz)
    
    # Create the envelope containing the new config.
    #  Envelopes also contain 'timestamp' and 'result' fields which are populated in the instrument reply.
    config_envelope = configuration_pb2.ConfigurationEnvelope(configuration=config)
    
    # Perform the SetState with the new envelope
    result_envelope = stub.SetState(config_envelope)
    
    # Returned envelope contains the current state of the updated settings, as well as a result field
    print("Received ConfigurationEnvelope reply:\n{}".format(result_envelope))


with grpc.insecure_channel('127.0.0.1:1234') as channel: # NOTE: Change the IP Address and Port to match the Instrument and its gRPC configuration.
    stub = service_pb2_grpc.SonardyneServiceStub(channel)

    # Get the version number of the API
    version_result = stub.GetVersion(version_pb2.VersionRequest())
    print("Called GetVersion: v{}.{}".format(version_result.Major, version_result.Minor))

    # Get the current state of the instrument
    result_config_envelope = stub.GetState(configuration_pb2.ConfigurationRequest(requestor="PyGrpcClient"))
    print("Called GetState:\n{}".format(result_config_envelope))
    # For example, get the current GNSS aiding state
    result_config = result_config_envelope.configuration
    result_aiding_configuration = result_config.aiding_configurations[0]
    result_gnss_aiding_state = result_aiding_configuration.enable_gnss
    print("GNSS aiding state: {}".format(result_gnss_aiding_state))

    # Set an example state
    SetExampleState(stub)