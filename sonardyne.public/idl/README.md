# Protocol Documentation
<a name="top"></a>

## Table of Contents

- [configuration.proto](#configuration-proto)
    - [AidingConfiguration](#sonardyne-api-AidingConfiguration)
    - [Configuration](#sonardyne-api-Configuration)
    - [ConfigurationEnvelope](#sonardyne-api-ConfigurationEnvelope)
    - [ConfigurationRequest](#sonardyne-api-ConfigurationRequest)
    - [DopplerVelocityLogConfiguration](#sonardyne-api-DopplerVelocityLogConfiguration)
    - [ResetConfiguration](#sonardyne-api-ResetConfiguration)
    - [SoundVelocityConfiguration](#sonardyne-api-SoundVelocityConfiguration)
  
    - [AidingConfiguration.AIDING_STATE](#sonardyne-api-AidingConfiguration-AIDING_STATE)
    - [DopplerVelocityLogConfiguration.UPDATE_RATE](#sonardyne-api-DopplerVelocityLogConfiguration-UPDATE_RATE)
    - [ResetConfiguration.RESET_TYPE](#sonardyne-api-ResetConfiguration-RESET_TYPE)
    - [SoundVelocityConfiguration.SOUND_VELOCITY](#sonardyne-api-SoundVelocityConfiguration-SOUND_VELOCITY)
  
- [result.proto](#result-proto)
    - [Result](#sonardyne-api-Result)
  
    - [Result.Outcome](#sonardyne-api-Result-Outcome)
  
- [service.proto](#service-proto)
    - [SonardyneService](#sonardyne-api-SonardyneService)
  
- [timestamp.proto](#timestamp-proto)
    - [Timestamp](#sonardyne-api-Timestamp)
  
- [uid.proto](#uid-proto)
    - [Uid](#sonardyne-api-Uid)
  
- [version.proto](#version-proto)
    - [VersionRequest](#sonardyne-api-VersionRequest)
    - [VersionResponse](#sonardyne-api-VersionResponse)
  
- [Scalar Value Types](#scalar-value-types)



<a name="configuration-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## configuration.proto



<a name="sonardyne-api-AidingConfiguration"></a>

### AidingConfiguration
Position aiding configuration, defines which position input(s) to use for aiding


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| id | [Uid](#sonardyne-api-Uid) |  | Used to identify recipient instrument/module |
| result | [Result](#sonardyne-api-Result) |  | Populated by instrument when replying to a SetState |
| enable_gnss | [AidingConfiguration.AIDING_STATE](#sonardyne-api-AidingConfiguration-AIDING_STATE) |  | Used to turn GNSS aiding on or off |
| enable_xpos | [AidingConfiguration.AIDING_STATE](#sonardyne-api-AidingConfiguration-AIDING_STATE) |  | Used to turn XPOS aiding on or off |
| enable_usbl | [AidingConfiguration.AIDING_STATE](#sonardyne-api-AidingConfiguration-AIDING_STATE) |  | Used to turn USBL aiding on or off |






<a name="sonardyne-api-Configuration"></a>

### Configuration
Each type of configuration is repeated to allow multiple recipients per message, e.g. resetting multiple algorithms on an instrument


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| reset_configurations | [ResetConfiguration](#sonardyne-api-ResetConfiguration) | repeated | Collection of reset configurations |
| aiding_configurations | [AidingConfiguration](#sonardyne-api-AidingConfiguration) | repeated | Collection of aiding configurations |
| sound_velocity_configurations | [SoundVelocityConfiguration](#sonardyne-api-SoundVelocityConfiguration) | repeated | Collection of Sound Velocity configurations |
| doppler_velocity_configurations | [DopplerVelocityLogConfiguration](#sonardyne-api-DopplerVelocityLogConfiguration) | repeated | Collection of Doppler Velocity configurations |






<a name="sonardyne-api-ConfigurationEnvelope"></a>

### ConfigurationEnvelope
A container of an instrument configuration and timestamp


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| timestamp | [Timestamp](#sonardyne-api-Timestamp) |  |  |
| result | [Result](#sonardyne-api-Result) |  | Populated by instrument when replying to a SetState |
| configuration | [Configuration](#sonardyne-api-Configuration) |  |  |






<a name="sonardyne-api-ConfigurationRequest"></a>

### ConfigurationRequest



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| timestamp | [Timestamp](#sonardyne-api-Timestamp) |  |  |
| requestor | [string](#string) |  | Optional user-definable field |






<a name="sonardyne-api-DopplerVelocityLogConfiguration"></a>

### DopplerVelocityLogConfiguration
Doppler Velocity Log configuration which controls the update rate


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| id | [Uid](#sonardyne-api-Uid) |  | Used to identify recipient instrument/module |
| result | [Result](#sonardyne-api-Result) |  | Populated by instrument when replying to a SetState |
| update_rate | [DopplerVelocityLogConfiguration.UPDATE_RATE](#sonardyne-api-DopplerVelocityLogConfiguration-UPDATE_RATE) |  | Specifies the update rate in Hz |






<a name="sonardyne-api-ResetConfiguration"></a>

### ResetConfiguration
Set type of reset to execute


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| id | [Uid](#sonardyne-api-Uid) |  | Used to identify recipient instrument/module |
| result | [Result](#sonardyne-api-Result) |  | Populated by instrument when replying to a SetState |
| reset_type | [ResetConfiguration.RESET_TYPE](#sonardyne-api-ResetConfiguration-RESET_TYPE) |  | Indicates the type of reset required |






<a name="sonardyne-api-SoundVelocityConfiguration"></a>

### SoundVelocityConfiguration
Sound Velocity configuration which controls the type of trigger to use


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| id | [Uid](#sonardyne-api-Uid) |  | Used to identify recipient instrument/module |
| result | [Result](#sonardyne-api-Result) |  | Populated by instrument when replying to a SetState |
| sound_velocity_type | [SoundVelocityConfiguration.SOUND_VELOCITY](#sonardyne-api-SoundVelocityConfiguration-SOUND_VELOCITY) |  | Define the Sound Velocity source |
| manual_salinity_value | [double](#double) |  | Used if Sound Velocity type is INTERNAL_SALINITY |
| manual_velocity_value | [double](#double) |  | Used if Sound Velocity type is INTERNAL_MANUAL |





 


<a name="sonardyne-api-AidingConfiguration-AIDING_STATE"></a>

### AidingConfiguration.AIDING_STATE


| Name | Number | Description |
| ---- | ------ | ----------- |
| AIDING_STATE_UNSPECIFIED | 0 | Default value if field is not populated |
| ENABLED | 1 |  |
| DISABLED | 2 |  |



<a name="sonardyne-api-DopplerVelocityLogConfiguration-UPDATE_RATE"></a>

### DopplerVelocityLogConfiguration.UPDATE_RATE


| Name | Number | Description |
| ---- | ------ | ----------- |
| UPDATE_RATE_UNSPECIFIED | 0 | Default value if field is not populated |
| TRIGGER_RISING | 1 | Use external trigger (rising edge) |
| TRIGGER_FALLING | 2 | Use external trigger (falling edge) |
| MAX_RATE | 3 | Use max supported update rate |
| FIXED_1HZ | 4 | Use fixed 1Hz rate |
| FIXED_2HZ | 5 | Use fixed 2Hz rate |
| FIXED_5HZ | 6 | Use fixed 5Hz rate |
| FIXED_10HZ | 7 | Use fixed 10Hz rate |



<a name="sonardyne-api-ResetConfiguration-RESET_TYPE"></a>

### ResetConfiguration.RESET_TYPE


| Name | Number | Description |
| ---- | ------ | ----------- |
| RESET_TYPE_UNSPECIFIED | 0 | Default value if field is not populated |
| SOFT_RESET | 1 | See instrument manual for description |
| HARD_RESET | 2 | See instrument manual for description |



<a name="sonardyne-api-SoundVelocityConfiguration-SOUND_VELOCITY"></a>

### SoundVelocityConfiguration.SOUND_VELOCITY


| Name | Number | Description |
| ---- | ------ | ----------- |
| SOUND_VELOCITY_UNSPECIFIED | 0 | Default value if field is not populated |
| EXTERNAL | 1 | Use external - N.B. The port must be specified in the webUI |
| INTERNAL_SALINITY | 2 | Use internal (derived from salinity) |
| INTERNAL_MANUAL | 3 | Use manually defined value |


 

 

 



<a name="result-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## result.proto



<a name="sonardyne-api-Result"></a>

### Result



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| success | [Result.Outcome](#sonardyne-api-Result-Outcome) |  | Indicates success or failure. True for success, otherwise False |
| message | [string](#string) |  | Description of the operations result |





 


<a name="sonardyne-api-Result-Outcome"></a>

### Result.Outcome


| Name | Number | Description |
| ---- | ------ | ----------- |
| SUCCESS | 0 | Operation has succeeded |
| FAILURE | 1 | Operation has failed |
| INVALID | 2 | Operation has been given invalid parameters |


 

 

 



<a name="service-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## service.proto


 

 

 


<a name="sonardyne-api-SonardyneService"></a>

### SonardyneService


| Method Name | Request Type | Response Type | Description |
| ----------- | ------------ | ------------- | ------------|
| GetVersion | [VersionRequest](#sonardyne-api-VersionRequest) | [VersionResponse](#sonardyne-api-VersionResponse) | Gets the api protocol version |
| SetState | [ConfigurationEnvelope](#sonardyne-api-ConfigurationEnvelope) | [ConfigurationEnvelope](#sonardyne-api-ConfigurationEnvelope) | Sets instrument configuration. Returns the updated configuration, result, and timestamp |
| GetState | [ConfigurationRequest](#sonardyne-api-ConfigurationRequest) | [ConfigurationEnvelope](#sonardyne-api-ConfigurationEnvelope) | Gets instrument configuration. The &#39;ConfigurationRequest&#39; contains required instrument specific configuration type |
| StateStream | [ConfigurationRequest](#sonardyne-api-ConfigurationRequest) | [ConfigurationEnvelope](#sonardyne-api-ConfigurationEnvelope) stream | A stream which publishes all state changes on the instrument. |

 



<a name="timestamp-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## timestamp.proto



<a name="sonardyne-api-Timestamp"></a>

### Timestamp



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| common_time | [double](#double) |  | Time since the UNIX epoch (01/01/1970) in seconds and fractional seconds |
| instrument_time | [double](#double) |  | Monotonically increasing instrument time in seconds and fractional seconds |





 

 

 

 



<a name="uid-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## uid.proto



<a name="sonardyne-api-Uid"></a>

### Uid
Used to identify a recipient


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| uid | [uint32](#uint32) |  | Unique identifier of a recipient |
| name | [string](#string) |  | Human-readable recipient name populated in reply |





 

 

 

 



<a name="version-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## version.proto



<a name="sonardyne-api-VersionRequest"></a>

### VersionRequest







<a name="sonardyne-api-VersionResponse"></a>

### VersionResponse
A message that contains Semantic Versioning which comprises a three part version number: Major.Minor.Patch


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| Major | [uint32](#uint32) |  | MAJOR version incremented for incompatible changes that break existing clients. |
| Minor | [uint32](#uint32) |  | MINOR version incremented for backward-compatible features or enhancements. |
| Patch | [uint32](#uint32) |  | PATCH version incremented for backward-compatible bug fixes or patches. |





 

 

 

 



## Scalar Value Types

| .proto Type | Notes | C++ | Java | Python | Go | C# | PHP | Ruby |
| ----------- | ----- | --- | ---- | ------ | -- | -- | --- | ---- |
| <a name="double" /> double |  | double | double | float | float64 | double | float | Float |
| <a name="float" /> float |  | float | float | float | float32 | float | float | Float |
| <a name="int32" /> int32 | Uses variable-length encoding. Inefficient for encoding negative numbers – if your field is likely to have negative values, use sint32 instead. | int32 | int | int | int32 | int | integer | Bignum or Fixnum (as required) |
| <a name="int64" /> int64 | Uses variable-length encoding. Inefficient for encoding negative numbers – if your field is likely to have negative values, use sint64 instead. | int64 | long | int/long | int64 | long | integer/string | Bignum |
| <a name="uint32" /> uint32 | Uses variable-length encoding. | uint32 | int | int/long | uint32 | uint | integer | Bignum or Fixnum (as required) |
| <a name="uint64" /> uint64 | Uses variable-length encoding. | uint64 | long | int/long | uint64 | ulong | integer/string | Bignum or Fixnum (as required) |
| <a name="sint32" /> sint32 | Uses variable-length encoding. Signed int value. These more efficiently encode negative numbers than regular int32s. | int32 | int | int | int32 | int | integer | Bignum or Fixnum (as required) |
| <a name="sint64" /> sint64 | Uses variable-length encoding. Signed int value. These more efficiently encode negative numbers than regular int64s. | int64 | long | int/long | int64 | long | integer/string | Bignum |
| <a name="fixed32" /> fixed32 | Always four bytes. More efficient than uint32 if values are often greater than 2^28. | uint32 | int | int | uint32 | uint | integer | Bignum or Fixnum (as required) |
| <a name="fixed64" /> fixed64 | Always eight bytes. More efficient than uint64 if values are often greater than 2^56. | uint64 | long | int/long | uint64 | ulong | integer/string | Bignum |
| <a name="sfixed32" /> sfixed32 | Always four bytes. | int32 | int | int | int32 | int | integer | Bignum or Fixnum (as required) |
| <a name="sfixed64" /> sfixed64 | Always eight bytes. | int64 | long | int/long | int64 | long | integer/string | Bignum |
| <a name="bool" /> bool |  | bool | boolean | boolean | bool | bool | boolean | TrueClass/FalseClass |
| <a name="string" /> string | A string must always contain UTF-8 encoded or 7-bit ASCII text. | string | String | str/unicode | string | string | string | String (UTF-8) |
| <a name="bytes" /> bytes | May contain any arbitrary sequence of bytes. | string | ByteString | str | []byte | ByteString | string | String (ASCII-8BIT) |

