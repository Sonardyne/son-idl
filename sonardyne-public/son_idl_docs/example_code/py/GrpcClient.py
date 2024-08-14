#Copyright 2024 Sonardyne

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the “Software”), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is furnished
#to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the software.

#THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
#WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
#CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import proto_generate
proto_generate.proto_generate()

import grpc
import google.protobuf.any_pb2

from sonardyne_public.idl.common import version_pb2
from sonardyne_public.idl.configuration import dvl_configuration_pb2
from sonardyne_public.idl.services import state_service_pb2_grpc
from sonardyne_public.idl.configuration import reset_configuration_pb2
from sonardyne_public.idl.configuration import aiding_configuration_pb2
from sonardyne_public.idl.configuration import configuration_envelope_pb2
from sonardyne_public.idl.configuration import sound_velocity_configuration_pb2

from google.protobuf.json_format import MessageToJson


def SetExampleState(stub):    
    # Create the envelope containing the new config.
    #  Envelopes also contain 'timestamp' and 'result' fields which are populated in the instrument reply.
    configuration_envelope = configuration_envelope_pb2.ConfigurationEnvelope()
    
    # Each type of configuration is stored as a list. This is reserved for future use as not all units support multiple configurations.
    
    # Create and add a reset config to perform a soft reset
    reset_config = reset_configuration_pb2.ResetConfiguration(reset_type="SOFT_RESET")        
    configuration_envelope.configuration.add().CopyFrom(google.protobuf.any_pb2.Any().Pack(reset_config))

    # Create and add an aiding config to enable GNSS aiding and disable USBL aiding
    aiding_config_enable_gnss = aiding_configuration_pb2.AidingConfiguration(enable_gnss="ENABLED", enable_usbl="DISABLED")
    configuration_envelope.configuration.add().CopyFrom(google.protobuf.any_pb2.Any().Pack(aiding_config_enable_gnss))
        
    # Create and add a sound velocity config to set the SV source to salinity-derived and set the SV salinity to an arbitrary value
    sv_config_salinity_derived = sound_velocity_configuration_pb2.SoundVelocityConfiguration(sound_velocity_type="INTERNAL_SALINITY", manual_salinity_value=32.1)
    configuration_envelope.configuration.add().CopyFrom(google.protobuf.any_pb2.Any().Pack(sv_config_salinity_derived))
        
    # Create and add a DVL config to set the update rate to an arbitrary choice
    dvl_config_1Hz = dvl_configuration_pb2.DopplerVelocityLogConfiguration(update_rate="FIXED_1HZ")
    configuration_envelope.configuration.add().CopyFrom(google.protobuf.any_pb2.Any().Pack(dvl_config_1Hz))    
               
    # Perform the SetState with the new envelope
    result_envelope = stub.SetState(configuration_envelope)
    
    # Returned envelope contains the current state of the updated settings, as well as a result field
    print("Received ConfigurationEnvelope reply:\n{}".format(result_envelope))

with grpc.insecure_channel('127.0.0.1:1234') as channel: # NOTE: Change the IP Address and Port to match the Instrument and its gRPC configuration.
    stub = state_service_pb2_grpc.StateServiceStub(channel)

    # Get the version number of the API
    version_result = stub.GetVersion(version_pb2.VersionRequest())
    print("Called GetVersion: v{}.{}".format(version_result.major, version_result.minor))

    # Get the current state of the instrument
    result_config_envelope = stub.GetState(configuration_envelope_pb2.ConfigurationRequest(requestor="PyGrpcClient"))
        
    for (config) in result_config_envelope.configuration:        
        if config.Is(aiding_configuration_pb2.AidingConfiguration.DESCRIPTOR):
            aiding_config = aiding_configuration_pb2.AidingConfiguration()
            config.Unpack(aiding_config)
            print("Current Aiding Configuration: {}".format(MessageToJson(aiding_config)))
        if config.Is(dvl_configuration_pb2.DvlConfiguration.DESCRIPTOR):
            dvl_config = dvl_configuration_pb2.DvlConfiguration()
            config.Unpack(dvl_config)
            print("Current DVL Configuration: {}".format(MessageToJson(dvl_config)))
        if config.Is(reset_configuration_pb2.ResetConfiguration.DESCRIPTOR):
            reset_config = reset_configuration_pb2.ResetConfiguration()
            config.Unpack(reset_config)
            print("Current Reset Configuration: {}".format(MessageToJson(reset_config)))
        if config.Is(sound_velocity_configuration_pb2.SoundVelocityConfiguration.DESCRIPTOR):
            sound_velocity_config = sound_velocity_configuration_pb2.SoundVelocityConfiguration()
            config.Unpack(sound_velocity_config)        
            print("Current Sound Velocity Configuration: {}".format(MessageToJson(sound_velocity_config)))        