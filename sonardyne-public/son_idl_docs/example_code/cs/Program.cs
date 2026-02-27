//Copyright 2024 Sonardyne

//Permission is hereby granted, free of charge, to any person obtaining a copy
//of this software and associated documentation files (the “Software”), to deal
//in the Software without restriction, including without limitation the rights
//to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
//copies of the Software, and to permit persons to whom the Software is furnished
//to do so, subject to the following conditions:

//The above copyright notice and this permission notice shall be included in
//all copies or substantial portions of the software.

//THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
//IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
//FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
//AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
//WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
//CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

using Grpc.Net.Client;
using Google.Protobuf.WellKnownTypes;
using Sonardyne.Api.Pub.Common;
using Sonardyne.Api.Pub.Configuration;

namespace Sonardyne.Api.Example
{
    internal class Program
    {
        // This example demonstrates how to connect to and get the current state of the instrument.
        static void Main(string[] args)
        {
            // NOTE: Change the IP Address and Port to match the instrument and its gRPC configuration.
            const string address = "http://127.0.0.1:1234"; 

            var channel = GrpcChannel.ForAddress(address); 
            var client = new StateService.StateServiceClient(channel);
            
            // Get the version
            var getVersionReply = client.GetVersion(new VersionRequest());
            Console.WriteLine($"\nCalled GetVersion: v.{getVersionReply.Major}.{getVersionReply.Minor}");

            // Get the current state of the instrument            
            var getStateReply = client.GetState(new ConfigurationRequest());

            if (getStateReply?.Configuration.Count > 0)
            {
                OutputState(getStateReply);
            }
                       
            // Create a device configuration.
            // Create the envelope containing the new config.
            // Envelopes also contain 'timestamp' and 'result' fields which are populated in the instrument reply.
            var configurationEnvelope = new ConfigurationEnvelope();

            // Create and add a reset config to perform a soft reset
            var resetConfig = new ResetConfiguration();

            resetConfig.ResetType = new ResetType { Value = ResetType.Types.ResetTypeEnum.SoftReset };            
            configurationEnvelope.Configuration.Add(Any.Pack(resetConfig));

            // Create and add an aiding config to enable GNSS aiding and disable USBL aiding
            var aidingConfig = new AidingConfiguration();
            aidingConfig.EnableGnss = new AidingState { Value = AidingState.Types.AidingStateEnum.Enabled };
            aidingConfig.EnableUsbl = new AidingState { Value = AidingState.Types.AidingStateEnum.Disabled };
            configurationEnvelope.Configuration.Add(Any.Pack(aidingConfig));

            // Create and add a sound velocity config to set the SV source to salinity-derived and set the SV salinity to an arbitrary value
            var svConfig = new SoundVelocityConfiguration();
            svConfig.SoundVelocityType = new SoundVelocityType { Value = SoundVelocityType.Types.SoundVelocityTypeEnum.External };
            svConfig.ManualSalinityValuePartsPerThousand = new BoundedDouble { Value = 32.1 };
            configurationEnvelope.Configuration.Add(Any.Pack(svConfig));

            // Create and add a DVL config to set the update rate to an arbitrary choice
            var dvlConfig = new DvlConfiguration();
            dvlConfig.UpdateRate = new DvlUpdateRate { Value = DvlUpdateRate.Types.DvlUpdateRateEnum.Fixed1Hz };
            configurationEnvelope.Configuration.Add(Any.Pack(dvlConfig));

            // Perform the SetState with the new envelope
            Console.WriteLine($"\nSetting State...");            
            var replyEnvelope = client.SetState(configurationEnvelope);

            // Returned envelope contains the current state of the updated settings, as well as a result field
            if (getStateReply?.Configuration.Count > 0)
            {
                OutputState(replyEnvelope);
            }            
        }        
        
        static void OutputState(ConfigurationEnvelope configurationEnvelope)
        {
            foreach (var configuration in configurationEnvelope.Configuration)
            {
                if (configuration.Is(AidingConfiguration.Descriptor))
                {
                    Console.WriteLine($"Aiding configuration received = {configuration.Unpack<AidingConfiguration>()}");
                }                
                else if (configuration.Is(ResetConfiguration.Descriptor))
                {
                    Console.WriteLine($"Reset configuration received = {configuration.Unpack<ResetConfiguration>()}");
                }
                else if (configuration.Is(SoundVelocityConfiguration.Descriptor))
                {
                    Console.WriteLine($"Sound velocity configuration received = {configuration.Unpack<SoundVelocityConfiguration>()}");
                }
                else if (configuration.Is(DvlConfiguration.Descriptor))
                {
                    Console.WriteLine($"DVL configuration received = {configuration.Unpack<DvlConfiguration>()}");
                }                                
                else
                {
                    Console.WriteLine("Unknown configuration");
                }
            }
        }
    }
}
