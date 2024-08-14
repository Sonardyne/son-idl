# Protocol Documentation
<a name="top"></a>

## Table of Contents

- [Protocol Documentation](#protocol-documentation)
  - [Table of Contents](#table-of-contents)
  - [sonardyne-public/idl/common/primitives.proto](#sonardyne-publicidlcommonprimitivesproto)
    - [BoundedDouble](#boundeddouble)
    - [BoundedFloat](#boundedfloat)
    - [BoundedInt32](#boundedint32)
    - [BoundedInt64](#boundedint64)
    - [BoundedUInt32](#boundeduint32)
    - [BoundedUInt64](#boundeduint64)
    - [Fixed32Value](#fixed32value)
    - [Fixed64Value](#fixed64value)
    - [SFixed32Value](#sfixed32value)
    - [SFixed64Value](#sfixed64value)
    - [SInt32Value](#sint32value)
    - [SInt64Value](#sint64value)
  - [sonardyne-public/idl/common/result.proto](#sonardyne-publicidlcommonresultproto)
    - [Result](#result)
    - [Result.Outcome](#resultoutcome)
  - [sonardyne-public/idl/common/timestamp.proto](#sonardyne-publicidlcommontimestampproto)
    - [Timestamp](#timestamp)
  - [sonardyne-public/idl/common/uid.proto](#sonardyne-publicidlcommonuidproto)
    - [Uid](#uid)
  - [sonardyne-public/idl/common/version.proto](#sonardyne-publicidlcommonversionproto)
    - [VersionRequest](#versionrequest)
    - [VersionResponse](#versionresponse)
  - [sonardyne-public/idl/configuration/aiding\_configuration.proto](#sonardyne-publicidlconfigurationaiding_configurationproto)
    - [AidingConfiguration](#aidingconfiguration)
    - [AidingState](#aidingstate)
    - [AidingState.AidingStateEnum](#aidingstateaidingstateenum)
  - [sonardyne-public/idl/configuration/configuration\_envelope.proto](#sonardyne-publicidlconfigurationconfiguration_envelopeproto)
    - [ConfigurationEnvelope](#configurationenvelope)
    - [ConfigurationRequest](#configurationrequest)
  - [sonardyne-public/idl/configuration/dvl\_configuration.proto](#sonardyne-publicidlconfigurationdvl_configurationproto)
    - [DvlConfiguration](#dvlconfiguration)
    - [DvlUpdateRate](#dvlupdaterate)
    - [DvlUpdateRate.DvlUpdateRateEnum](#dvlupdateratedvlupdaterateenum)
  - [sonardyne-public/idl/configuration/reset\_configuration.proto](#sonardyne-publicidlconfigurationreset_configurationproto)
    - [ResetConfiguration](#resetconfiguration)
    - [ResetType](#resettype)
    - [ResetType.ResetTypeEnum](#resettyperesettypeenum)
  - [sonardyne-public/idl/configuration/shutdown\_configuration.proto](#sonardyne-publicidlconfigurationshutdown_configurationproto)
    - [ShutdownConfiguration](#shutdownconfiguration)
  - [sonardyne-public/idl/configuration/sound\_velocity\_configuration.proto](#sonardyne-publicidlconfigurationsound_velocity_configurationproto)
    - [SoundVelocityConfiguration](#soundvelocityconfiguration)
    - [SoundVelocityType](#soundvelocitytype)
    - [SoundVelocityType.SoundVelocityTypeEnum](#soundvelocitytypesoundvelocitytypeenum)
  - [sonardyne-public/idl/services/state\_service.proto](#sonardyne-publicidlservicesstate_serviceproto)
    - [StateService](#stateservice)
  - [Scalar Value Types](#scalar-value-types)



<a name="sonardyne-public_idl_common_primitives-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## sonardyne-public/idl/common/primitives.proto



<a name="sonardyne-api-pub-common-BoundedDouble"></a>

### BoundedDouble



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| value | [double](#double) |  | The value |
| min | [double](#double) |  | The minimum value (read only) |
| max | [double](#double) |  | The maximum value (read only) |






<a name="sonardyne-api-pub-common-BoundedFloat"></a>

### BoundedFloat



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| value | [float](#float) |  | The value |
| min | [float](#float) |  | The minimum value (read only) |
| max | [float](#float) |  | The maximum value (read only) |






<a name="sonardyne-api-pub-common-BoundedInt32"></a>

### BoundedInt32



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| value | [int32](#int32) |  | The value |
| min | [int32](#int32) |  | The minimum value (read only) |
| max | [int32](#int32) |  | The maximum value (read only) |






<a name="sonardyne-api-pub-common-BoundedInt64"></a>

### BoundedInt64



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| value | [int64](#int64) |  | The value |
| min | [int64](#int64) |  | The minimum value (read only) |
| max | [int64](#int64) |  | The maximum value (read only) |






<a name="sonardyne-api-pub-common-BoundedUInt32"></a>

### BoundedUInt32



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| value | [uint32](#uint32) |  | The value |
| min | [uint32](#uint32) |  | The minimum value (read only) |
| max | [uint32](#uint32) |  | The maximum value (read only) |






<a name="sonardyne-api-pub-common-BoundedUInt64"></a>

### BoundedUInt64



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| value | [uint64](#uint64) |  | The value |
| min | [uint64](#uint64) |  | The minimum value (read only) |
| max | [uint64](#uint64) |  | The maximum value (read only) |






<a name="sonardyne-api-pub-common-Fixed32Value"></a>

### Fixed32Value



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| value | [fixed32](#fixed32) |  | The value |
| min | [fixed32](#fixed32) |  | The minimum value (read only) |
| max | [fixed32](#fixed32) |  | The maximum value (read only) |






<a name="sonardyne-api-pub-common-Fixed64Value"></a>

### Fixed64Value



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| value | [fixed64](#fixed64) |  | The value |
| min | [fixed64](#fixed64) |  | The minimum value (read only) |
| max | [fixed64](#fixed64) |  | The maximum value (read only) |






<a name="sonardyne-api-pub-common-SFixed32Value"></a>

### SFixed32Value



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| value | [sfixed32](#sfixed32) |  | The value |
| min | [sfixed32](#sfixed32) |  | The minimum value (read only) |
| max | [sfixed32](#sfixed32) |  | The maximum value (read only) |






<a name="sonardyne-api-pub-common-SFixed64Value"></a>

### SFixed64Value



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| value | [sfixed64](#sfixed64) |  | The value |
| min | [sfixed64](#sfixed64) |  | The minimum value (read only) |
| max | [sfixed64](#sfixed64) |  | The maximum value (read only) |






<a name="sonardyne-api-pub-common-SInt32Value"></a>

### SInt32Value



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| value | [sint32](#sint32) |  | The value |
| min | [sint32](#sint32) |  | The minimum value (read only) |
| max | [sint32](#sint32) |  | The maximum value (read only) |






<a name="sonardyne-api-pub-common-SInt64Value"></a>

### SInt64Value



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| value | [sint64](#sint64) |  | The value |
| min | [sint64](#sint64) |  | The minimum value (read only) |
| max | [sint64](#sint64) |  | The maximum value (read only) |





 

 

 

 



<a name="sonardyne-public_idl_common_result-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## sonardyne-public/idl/common/result.proto



<a name="sonardyne-api-pub-common-Result"></a>

### Result



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| success | [Result.Outcome](#sonardyne-api-pub-common-Result-Outcome) |  | Indicates success or failure. True for success, otherwise False |
| message | [string](#string) |  | Description of the operations result |





 


<a name="sonardyne-api-pub-common-Result-Outcome"></a>

### Result.Outcome


| Name | Number | Description |
| ---- | ------ | ----------- |
| UNSPECIFIED | 0 | Result of operation unspecified (default value) |
| SUCCESS | 1 | Operation has succeeded |
| FAILURE | 2 | Operation has failed |
| INVALID | 3 | Operation has been given invalid parameters |
| RESTRICTED | 4 | Operation is not allowed - user does not have permission, or instrument is not in the correct mode. |


 

 

 



<a name="sonardyne-public_idl_common_timestamp-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## sonardyne-public/idl/common/timestamp.proto



<a name="sonardyne-api-pub-common-Timestamp"></a>

### Timestamp



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| common_time_seconds | [double](#double) |  | Time since the UNIX epoch (01/01/1970) in seconds and fractional seconds |
| instrument_time_seconds | [double](#double) |  | Monotonically increasing instrument time in seconds and fractional seconds |





 

 

 

 



<a name="sonardyne-public_idl_common_uid-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## sonardyne-public/idl/common/uid.proto



<a name="sonardyne-api-pub-common-Uid"></a>

### Uid
Used to identify a recipient


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| uid | [uint32](#uint32) |  | Unique identifier of a recipient |
| name | [string](#string) |  | Human-readable recipient name populated in reply |





 

 

 

 



<a name="sonardyne-public_idl_common_version-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## sonardyne-public/idl/common/version.proto



<a name="sonardyne-api-pub-common-VersionRequest"></a>

### VersionRequest







<a name="sonardyne-api-pub-common-VersionResponse"></a>

### VersionResponse
A message that contains Semantic Versioning which comprises a three part version number: Major.Minor.Patch


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| major | [uint32](#uint32) |  | MAJOR version incremented for incompatible changes that break existing clients. |
| minor | [uint32](#uint32) |  | MINOR version incremented for backward-compatible features or enhancements. |
| patch | [uint32](#uint32) |  | PATCH version incremented for backward-compatible bug fixes or patches. |





 

 

 

 



<a name="sonardyne-public_idl_configuration_aiding_configuration-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## sonardyne-public/idl/configuration/aiding_configuration.proto



<a name="sonardyne-api-pub-configuration-AidingConfiguration"></a>

### AidingConfiguration
Position aiding configuration, defines which position input(s) to use for aiding


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| id | [sonardyne.api.pub.common.Uid](#sonardyne-api-pub-common-Uid) |  | Used to identify recipient instrument/module |
| result | [sonardyne.api.pub.common.Result](#sonardyne-api-pub-common-Result) |  | Populated by instrument when replying to a SetState indicating the success of the operation |
| enable_gnss | [AidingState](#sonardyne-api-pub-configuration-AidingState) |  | Used to turn GNSS aiding on or off |
| enable_xpos | [AidingState](#sonardyne-api-pub-configuration-AidingState) |  | Used to turn XPOS aiding on or off |
| enable_usbl | [AidingState](#sonardyne-api-pub-configuration-AidingState) |  | Used to turn USBL aiding on or off |






<a name="sonardyne-api-pub-configuration-AidingState"></a>

### AidingState



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| value | [AidingState.AidingStateEnum](#sonardyne-api-pub-configuration-AidingState-AidingStateEnum) |  | The state of the aiding |
| valid_values | [AidingState.AidingStateEnum](#sonardyne-api-pub-configuration-AidingState-AidingStateEnum) | repeated | The valid values for the aiding state |





 


<a name="sonardyne-api-pub-configuration-AidingState-AidingStateEnum"></a>

### AidingState.AidingStateEnum


| Name | Number | Description |
| ---- | ------ | ----------- |
| UNKNOWN | 0 |  |
| ENABLED | 1 |  |
| DISABLED | 2 |  |


 

 

 



<a name="sonardyne-public_idl_configuration_configuration_envelope-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## sonardyne-public/idl/configuration/configuration_envelope.proto



<a name="sonardyne-api-pub-configuration-ConfigurationEnvelope"></a>

### ConfigurationEnvelope
A container of instrument configurations, a timestamp and a result.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| timestamp | [sonardyne.api.pub.common.Timestamp](#sonardyne-api-pub-common-Timestamp) |  | Timestamp of the configuration |
| result | [sonardyne.api.pub.common.Result](#sonardyne-api-pub-common-Result) |  | Populated by instrument when replying to a SetState indicating the success of the operation |
| configuration | [google.protobuf.Any](https://protobuf.dev/programming-guides/proto3/#any) | repeated | The configuration data - can be any of [AidingConfiguration](#aidingconfiguration), [DvlConfiguration](#dvlconfiguration), [ResetConfiguration](#resetconfiguration), [ShutdownConfiguration](#shutdownconfiguration) or [SoundVelocityConfiguration](#soundvelocityconfiguration)|






<a name="sonardyne-api-pub-configuration-ConfigurationRequest"></a>

### ConfigurationRequest



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| timestamp | [sonardyne.api.pub.common.Timestamp](#sonardyne-api-pub-common-Timestamp) |  | Timestamp of the request |
| requestor | [string](#string) |  | Optional user-definable field |





 

 

 

 



<a name="sonardyne-public_idl_configuration_dvl_configuration-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## sonardyne-public/idl/configuration/dvl_configuration.proto



<a name="sonardyne-api-pub-configuration-DvlConfiguration"></a>

### DvlConfiguration
Doppler Velocity Log configuration which controls the update rate


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| id | [sonardyne.api.pub.common.Uid](#sonardyne-api-pub-common-Uid) |  | Used to identify recipient instrument/module |
| result | [sonardyne.api.pub.common.Result](#sonardyne-api-pub-common-Result) |  | Populated by instrument when replying to a SetState indicating the success of the operation |
| update_rate | [DvlUpdateRate](#sonardyne-api-pub-configuration-DvlUpdateRate) |  | Specifies the update rate |






<a name="sonardyne-api-pub-configuration-DvlUpdateRate"></a>

### DvlUpdateRate



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| value | [DvlUpdateRate.DvlUpdateRateEnum](#sonardyne-api-pub-configuration-DvlUpdateRate-DvlUpdateRateEnum) |  | The type of reset to execute |
| valid_values | [DvlUpdateRate.DvlUpdateRateEnum](#sonardyne-api-pub-configuration-DvlUpdateRate-DvlUpdateRateEnum) | repeated | The valid values for the reset type |





 


<a name="sonardyne-api-pub-configuration-DvlUpdateRate-DvlUpdateRateEnum"></a>

### DvlUpdateRate.DvlUpdateRateEnum


| Name | Number | Description |
| ---- | ------ | ----------- |
| UNKNOWN | 0 |  |
| TRIGGER_RISING | 1 | Use external trigger (rising edge) |
| TRIGGER_FALLING | 2 | Use external trigger (falling edge) |
| MAX_RATE | 3 | Use max supported update rate |
| FIXED_1HZ | 4 | Use fixed 1Hz rate |
| FIXED_2HZ | 5 | Use fixed 2Hz rate |
| FIXED_5HZ | 6 | Use fixed 5Hz rate |
| FIXED_10HZ | 7 | Use fixed 10Hz rate |


 

 

 



<a name="sonardyne-public_idl_configuration_reset_configuration-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## sonardyne-public/idl/configuration/reset_configuration.proto



<a name="sonardyne-api-pub-configuration-ResetConfiguration"></a>

### ResetConfiguration
Set type of reset to execute


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| id | [sonardyne.api.pub.common.Uid](#sonardyne-api-pub-common-Uid) |  | Used to identify recipient instrument/module |
| result | [sonardyne.api.pub.common.Result](#sonardyne-api-pub-common-Result) |  | Populated by instrument when replying to a SetState indicating the success of the operation |
| reset_type | [ResetType](#sonardyne-api-pub-configuration-ResetType) |  | Indicates the type of reset required |






<a name="sonardyne-api-pub-configuration-ResetType"></a>

### ResetType



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| value | [ResetType.ResetTypeEnum](#sonardyne-api-pub-configuration-ResetType-ResetTypeEnum) |  | The type of reset to execute |
| valid_values | [ResetType.ResetTypeEnum](#sonardyne-api-pub-configuration-ResetType-ResetTypeEnum) | repeated | The valid values for the reset type |





 


<a name="sonardyne-api-pub-configuration-ResetType-ResetTypeEnum"></a>

### ResetType.ResetTypeEnum


| Name | Number | Description |
| ---- | ------ | ----------- |
| UNKNOWN | 0 |  |
| SOFT_RESET | 1 | See instrument manual for description |
| HARD_RESET | 2 | See instrument manual for description |


 

 

 



<a name="sonardyne-public_idl_configuration_shutdown_configuration-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## sonardyne-public/idl/configuration/shutdown_configuration.proto



<a name="sonardyne-api-pub-configuration-ShutdownConfiguration"></a>

### ShutdownConfiguration



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| id | [sonardyne.api.pub.common.Uid](#sonardyne-api-pub-common-Uid) |  | Used to identify recipient instrument/module |
| result | [sonardyne.api.pub.common.Result](#sonardyne-api-pub-common-Result) |  | Populated by instrument when replying to a SetState indicating the success of the operation |





 

 

 

 



<a name="sonardyne-public_idl_configuration_sound_velocity_configuration-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## sonardyne-public/idl/configuration/sound_velocity_configuration.proto



<a name="sonardyne-api-pub-configuration-SoundVelocityConfiguration"></a>

### SoundVelocityConfiguration
Sound Velocity configuration which controls the type of trigger to use


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| id | [sonardyne.api.pub.common.Uid](#sonardyne-api-pub-common-Uid) |  | Used to identify recipient instrument/module |
| result | [sonardyne.api.pub.common.Result](#sonardyne-api-pub-common-Result) |  | Populated by instrument when replying to a SetState indicating the success of the operation |
| sound_velocity_type | [SoundVelocityType](#sonardyne-api-pub-configuration-SoundVelocityType) |  | Define the Sound Velocity source |
| manual_salinity_value_parts_per_thousand | [sonardyne.api.pub.common.BoundedDouble](#sonardyne-api-pub-common-BoundedDouble) |  | Used if Sound Velocity type is INTERNAL_SALINITY |
| manual_velocity_value_metres_per_second | [sonardyne.api.pub.common.BoundedDouble](#sonardyne-api-pub-common-BoundedDouble) |  | Used if Sound Velocity type is INTERNAL_MANUAL |






<a name="sonardyne-api-pub-configuration-SoundVelocityType"></a>

### SoundVelocityType



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| value | [SoundVelocityType.SoundVelocityTypeEnum](#sonardyne-api-pub-configuration-SoundVelocityType-SoundVelocityTypeEnum) |  | Define the Sound Velocity source |
| valid_values | [SoundVelocityType.SoundVelocityTypeEnum](#sonardyne-api-pub-configuration-SoundVelocityType-SoundVelocityTypeEnum) | repeated | Define the range of valid values |





 


<a name="sonardyne-api-pub-configuration-SoundVelocityType-SoundVelocityTypeEnum"></a>

### SoundVelocityType.SoundVelocityTypeEnum


| Name | Number | Description |
| ---- | ------ | ----------- |
| UNKNOWN | 0 |  |
| EXTERNAL | 1 | Use external - N.B. The port must be specified in the webUI |
| INTERNAL_SALINITY | 2 | Use internal (derived from salinity) |
| INTERNAL_MANUAL | 3 | Use manually defined value |


 

 

 



<a name="sonardyne-public_idl_services_state_service-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## sonardyne-public/idl/services/state_service.proto


 

 

 


<a name="sonardyne-api-StateService"></a>

### StateService


| Method Name | Request Type | Response Type | Description |
| ----------- | ------------ | ------------- | ------------|
| GetVersion | [pub.common.VersionRequest](#sonardyne-api-pub-common-VersionRequest) | [pub.common.VersionResponse](#sonardyne-api-pub-common-VersionResponse) | Gets the api protocol version |
| SetState | [pub.configuration.ConfigurationEnvelope](#sonardyne-api-pub-configuration-ConfigurationEnvelope) | [pub.configuration.ConfigurationEnvelope](#sonardyne-api-pub-configuration-ConfigurationEnvelope) | Sets instrument configuration. Returns the updated configuration, result, and timestamp |
| GetState | [pub.configuration.ConfigurationRequest](#sonardyne-api-pub-configuration-ConfigurationRequest) | [pub.configuration.ConfigurationEnvelope](#sonardyne-api-pub-configuration-ConfigurationEnvelope) | Gets instrument configuration. The &#39;ConfigurationRequest&#39; contains required instrument specific configuration type |
| StateStream | [pub.configuration.ConfigurationRequest](#sonardyne-api-pub-configuration-ConfigurationRequest) | [pub.configuration.ConfigurationEnvelope](#sonardyne-api-pub-configuration-ConfigurationEnvelope) stream | A stream which publishes all state changes on the instrument. |

 



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

