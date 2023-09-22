//Copyright 2023 Sonardyne

//Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
//documentation files (the “Software”), to deal in the Software without restriction, including without limitation the
//rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
//permit persons to whom the Software is furnished to do so, subject to the following conditions:

//The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
//Software.

//THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
//WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
//COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
//OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

using Grpc.Net.Client;
using SonardyneApi;

GrpcChannel channel = GrpcChannel.ForAddress("http://127.0.0.1:1234"); // NOTE: Change the IP Address and Port to match the Instrument and its gRPC configuration.
SonardyneService.SonardyneServiceClient client = new SonardyneService.SonardyneServiceClient(channel);

// Get the version number of the API
var getVersionReply = client.GetVersion(new VersionRequest());
Console.WriteLine($"\nCalled GetVersion: v.{getVersionReply.Major}.{getVersionReply.Minor}");

// Get the current state of the instrument
var getStateReply = client.GetState(new ConfigurationRequest());
Console.WriteLine("\nCalled GetState:\n" + getStateReply.Configuration.ToString());

if (getStateReply.Configuration.AidingConfigurations.Count > 0)
{
    Console.WriteLine("\ne.g. GNSS aiding state: " + getStateReply.Configuration.AidingConfigurations[0].EnableGnss);
}

// Create a device configuration. This contains configurations for Reset, Aiding, Sound Velocity, and DVL
var config = new Configuration();

// Each type of config is stored as a list. This is reserved for future use as not all units support multiple configurations.

// Create and add a reset config to perform a soft reset
var resetConfig = new ResetConfiguration();
resetConfig.ResetType = ResetConfiguration.Types.RESET_TYPE.SoftReset;
config.ResetConfigurations.Add(resetConfig);

// Create and add an aiding config to enable GNSS aiding and disable USBL aiding
var aidingConfig = new AidingConfiguration();
aidingConfig.EnableGnss = AidingConfiguration.Types.AIDING_STATE.Enabled;
aidingConfig.EnableUsbl = AidingConfiguration.Types.AIDING_STATE.Disabled;
config.AidingConfigurations.Add(aidingConfig);

// Create and add a sound velocity config to set the SV source to salinity-derived and set the SV salinity to an arbitrary value
var svConfig = new SoundVelocityConfiguration();
svConfig.SoundVelocityType = SoundVelocityConfiguration.Types.SOUND_VELOCITY.InternalSalinity;
svConfig.ManualSalinityValue = 32.1;
config.SoundVelocityConfigurations.Add(svConfig);

// Create and add a DVL config to set the update rate to an arbitrary choice
var dvlConfig = new DopplerVelocityLogConfiguration();
dvlConfig.UpdateRate = DopplerVelocityLogConfiguration.Types.UPDATE_RATE.Fixed1Hz;
config.DopplerVelocityConfigurations.Add(dvlConfig);

// Create the envelope containing the new config.
//  Envelopes also contain 'timestamp' and 'result' fields which are populated in the instrument reply.
var configEnvelope = new ConfigurationEnvelope();
configEnvelope.Configuration = config;
Console.WriteLine($"\nCreated an example ConfigurationEnvelope:\n{configEnvelope}\nSending now...");

// Perform the SetState with the new envelope
var replyEnvelope = client.SetState(configEnvelope);

// Returned envelope contains the current state of the updated settings, as well as a result field
Console.WriteLine($"\nReceived ConfigurationEnvelope reply:\n{replyEnvelope}");
