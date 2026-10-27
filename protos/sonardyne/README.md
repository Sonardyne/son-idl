# Sonardyne API 2.1.0

Version 2 of the Sonardyne API aims to simplify & standardise the existing API. 
The API continues the "envelope" pattern, making it backwards and forwards compatible with the V1 API.



**Table of Contents**

- [Services](#services)
  - [Configuration Service](#configuration-service)
  - [Command Service](#command-service)
  - [Observation Service](#observation-service)
  - [Comms Service](#comms-service)
- [Message Types](#message-types)
  - [Component Messages](#component-messages)
    - [Modules](#modules)
    - [Algorithms](#algorithms)
    - [Sources](#sources)
    - [Sensors](#sensors)
    - [Port Lists](#port-lists)
  - [Common Messages](#common-messages)
  - [Additional Message Types](#additional-message-types)
    - [Reference Messages](#reference-messages)
  - [Using Non-gRPC Modes](#using-non-grpc-modes)



## Services

The API provides services which all follow a regular pattern.

| Service                | Sends and receives      | Envelope contains     | What is this for?                                |
|------------------------|-------------------------|-----------------------|--------------------------------------------------|
| `ConfigurationService` | `ConfigurationEnvelope` | `[name]Configuration` | Set/Get e.g. set lever arms                      |
| `CommandService`       | `CommandEnvelope`       | `[name]Command`       | Run Task e.g. reset INS                          |
| `ObservationService`   | `ObservationEnvelope`   | `[name]Observation`   | In/Out stream of data e.g. GNSS received         |
| `CommsService`         | `CommsEnvelope`         | `[name]Comms`         | In/Out stream of comms data e.g. write to serial |


### Configuration Service
The configuration service is used for setting and getting configurations.
For each configuration sent in an envelope, we can expect the same configuration types
returned in the same order. Configurations contain a result to signify the success
of the configuration application.

The configuration service provides a `ConfigurationStream`, which outputs any configurations
which change. Listening on the `ConfigurationStream` is an efficient way to track the entire
state of the product you are connected to.

Typically, all fields in a configuration are `optional`. This allows the application of 
partial configurations. 


### Command Service
The command service is for command and control. Whereas the configuration
service is used to configure the state of a product (typically at startup), the command service
is used to perform actions (typically throughout runtime) such as algorithm resets, triggering acoustics
or commanding the system to shut down.


### Observation Service
The observation service provides a bidirectional stream, allowing us to send and listen to observations. An
observation is a piece of structured data e.g. a GNSS observation containing latitude and longitude fields, 
unlike _comms_ which is unstructured data, containing a variable number of raw bytes.

Example use cases for the observation services are streaming data from a pressure sensor, streaming
GNSS readings from a GNSS source, and streaming navigation solutions from a navigation module.

For information on subscribing to observation streams, see [Subscribing to Streams](#subscribing-to-streams).


### Comms Service
The comms service allows bidirectional communication with data ports e.g. ethernet ports and serial ports.
This allows monitoring of incoming and outgoing data over a port, or the sending of data out over a port.

An example comms message as JSON:
```json
{
 "@type": "type.googleapis.com/sonardyne.api.services.comms_service.CommsEnvelope",
 "comms_messages": [
  {
   "@type": "type.googleapis.com/sonardyne.api.common.ports.DataPortComms",
   "uid": {
    "value": "1518954244",
    "name": "TCP-8110"
   },
   "timestamp": {
    "common_time_seconds": 1765206239.1132329,
    "instrument_time_seconds": 251542.067792193
   },
   "data_direction": "DATA_DIRECTION_OUTPUT",
   "data": "SGVsbG8gV29ybGQhIDUw"
  }
 ]
}
```
_A `CommsEnvelope` containing a `DataPortComms` message with bytes to output over a TCP port named TCP-8110. 
Note that although these bytes are not human-readable in the serialised JSON, they do deserialise to a human-readable string._


## Message Types

The API makes use of message suffixes which give information on how a message may be used.

- There are messages which represent a [component](#component-messages) of the device.
- There are messages which represent a [reference](#reference-messages) to a component.
- There are [common messages](#common-messages) which represent commonly used concepts (e.g. ethernet ports) and have no required suffix.

### Component Messages

A product can be considered as a collection of _components_. These components are
_modules, algorithms, sources,_ and _port lists._

| Component   | Message name must be | Can be combined with service names e.g. |
|-------------|----------------------|-----------------------------------------|
| `Module`    | `[name]Module`       | `[name]ModuleConfiguration`             |
| `Algorithm` | `[name]Algorithm`    | `[name]AlgorithmCommand`                |
| `Source`    | `[name]Source`       | `[name]SourceObservation`               |
| `Sensor`    | `[name]Sensor`       | `[name]SensorObservation`               |
| `Port List` | `[name]PortList`     | `[name]PortListComms`                   |

#### Modules
The _**Module**_ component represents non-algorithm, non-sensor, non-data source components e.g. a `BatteryModule` is responsible for managing a battery and enabling/disabling charging. Another example module is the `NetworkModule`.

- `AlarmsModule` Allows raising/acknowledging/clearing of alarms.
- `BatteryModule` Allows battery management e.g. enabling charging.
- `DeviceInstallationModule` Allows configuration of the device's lever arms & mounting angles relative to the vessel.
- `DeviceModule` Allows reading of product name and serial number as well as sending of shutdown & factory reset commands.
- `EventsModule` Allows management of system and user events.
- `ExternalLoggingModule` Allows configuration of logging to an external client via a TCP server.
- `NavigationModule` Allows streaming of navigation solutions, in SPRINT this is the combined result of the AHRS & INS algorithm.
- `NetworkModule` Allows configuration of the device's network interface e.g. changing the device IP address.
- `OutputMessageModule` Allows configuration of output messages over data ports e.g. outputting GGA messages on a serial port.
- `PortLinkModule` Allows bidirectional routing between a serial and ethernet port.
- `RemotePointsModule` Allows configuration of remote points on the vessel, the navigation module can output data valid at these remote points.
- `SprintModule` Allows reading of SPRINT-specific device information.
- `TimeModule` Allows selection of time input sources in order to set UTC and instrument time.

An example request and response sent as JSON:
```json
{
  "@type": "type.googleapis.com/sonardyne.api.common.envelope.RequestEnvelope",
  "uid": 1,
  "requests": [
    {
      "@type": "type.googleapis.com/sonardyne.api.services.configuration_service.SetConfigurationRequest",
      "configuration": {
        "@type": "type.googleapis.com/sonardyne.api.modules.battery_module.BatteryModuleConfiguration",
        "isBatteryChargingEnabled": false
      }
    }
  ]
}
```
_A request to disable battery charging._
```json
{
 "@type": "type.googleapis.com/sonardyne.api.common.envelope.ResponseEnvelope",
 "uid": 1,
 "responses": [
  {
   "@type": "type.googleapis.com/sonardyne.api.services.configuration_service.SetConfigurationResponse",
   "timestamp": {
    "common_time_seconds": 1765193736.1050346,
    "instrument_time_seconds": 239039.059659313
   },
   "configuration": {
    "@type": "type.googleapis.com/sonardyne.api.modules.battery_module.BatteryModuleConfiguration",
    "uid": {
     "value": "2388163018",
     "name": "Output Message Module"
    },
    "is_battery_charging_enabled": false
   },
   "result": {
    "success": "OUTCOME_SUCCESS"
   }
  }
 ]
}
```
_The response to the battery module configuration request._

##### Alarms Module
An _**Alarm**_ is an ongoing state that tracks a problem until it is resolved, e.g. "No GNSS data received".
Alarms have a lifespan, transitioning between: Raised -> Acknowledged -> Cleared.
Alarms alert a user to problems as they arise and advise intervention may be required. They can be streamed over gRPC or
visualised on a dashboard.
An alarm can be latched (e.g. IMU error which is only cleared by power cycling) or non-latched (e.g. serial tx overflow which resolves
by increasing the baud rate).

##### Events Module
An _**Event**_ is a permanent record of timestamped actions, e.g. "TCP Client X connected".
Events are a single point in time, appended to a list and stored permanently.
Events provide a history of system usage, useful for diagnosing and replicating issues. They can be streamed over gRPC or read from logfiles.
Events are also created when an alarm is raised of lowered, allowing visibility of alarms in the event log. 


#### Algorithms

The _**Algorithm**_ component represents internal algorithms e.g. an INS algorithm.


- `AhrsAlgorithm` Allows sending of reset commands and configuring AHRS coarse latitude and longitude.
- `InsAlgorithm` Allows sending of reset commands and configuring INS aiding.
- `DvlAlgorithm` Allows configuration of DVL algorithm settings e.g. max ping rate & trigger inputs.


An example request and response sent as JSON:
```json
{
  "@type": "type.googleapis.com/sonardyne.api.common.envelope.RequestEnvelope",
  "uid": 2,
  "requests": [
    {
      "@type": "type.googleapis.com/sonardyne.api.services.configuration_service.SetConfigurationRequest",
      "configuration": {
        "@type": "type.googleapis.com/sonardyne.api.algorithms.ins_algorithm.InsAlgorithmConfiguration",
        "isGnssEnabled": true,
        "isXposEnabled": false
      }
    }
  ]
}
```
_A request to enable GNSS aiding to the INS, and to disable XPOS aiding._
```json
{
 "@type": "type.googleapis.com/sonardyne.api.common.envelope.ResponseEnvelope",
 "uid": 2,
 "responses": [
  {
   "@type": "type.googleapis.com/sonardyne.api.services.configuration_service.SetConfigurationResponse",
   "timestamp": {
    "common_time_seconds": 1765193984.8364909,
    "instrument_time_seconds": 239287.79105141
   },
   "configuration": {
    "@type": "type.googleapis.com/sonardyne.api.algorithms.ins_algorithm.InsAlgorithmConfiguration",
    "uid": {
     "value": "3646079212",
     "name": "INS Algorithm"
    },
    "is_gnss_enabled": true,
    "is_susbl_enabled": true,
    "is_xpos_enabled": false
   },
   "result": {
    "success": "OUTCOME_SUCCESS"
   }
  }
 ]
}
```
_The response to the INS algorithm configuration request. Note that other aiding sources (SUSBL, in this case) are left unchanged._


#### Sources

The _**Source**_ component represents "aiding" or "input" sources e.g. GNSS or Time.
These sources typically have configurable lever arms. The SPRINT Nav has a pressure sensor and a depth source. 
The depth source selects either a data port (receiving depth messages e.g. PSONPD) 
or a built-in pressure sensor for use as the source of depth.


- `DepthSource` Allows configuration of a data port or pressure sensor for deriving depth.
- `GnssSource` Allows configuration of a data port for a GNSS input (receiving GGA & GST messages).
- `SoundVelocitySource` Allows configuration of a manual value, data port, or derived sound velocity.
- `SusblSource` Allows configuration of a data port for an SUSBL input (receiving PSIMSSB messages).
- `NtpTimeSource` Allows configuration of a connection to an NTP server.
- `ZdaTimeSource` Allows configuration of a data port for a ZDA input (receiving ZDA messages).
- `PpsTimeSource` Allows configuration of a trigger port for a 1-pulse-per-second time input.
- `XposSource` Allows configuration of a data port for an XPOS input (receiving XPOS messages).


Many of the sources support observation streaming, which allows the monitoring of data received by these sources 
e.g. a `GnssSourceObservation`.

Sources typically have lever arms, and may have mounting angles, which relate their position to the Vessel's common reference point.


#### Sensors

The _**Sensor**_ component represents physical devices which observe data. The observation stream can be
used to monitor these observations. Example sensors are depth, temperature - these can be configured
using the Configuration Service.


- `DvlSensor` Represents a doppler velocity log (DVL) on the device.
- `PressureSensor` Represents a pressure sensor on the device.
- `TemperatureSensor` Represents a temperature sensor on the device.

#### Port Lists

The _**Port List**_ component represents collections of data inputs/outputs. 
Some port lists, e.g. ethernet port lists, can have entries added and removed. 
Other port lists, e.g. serial port lists, represent physical ports on the device and are fixed length.
On a data port such as a `SerialPort` or an `EthernetPort`, it is possible to send and receive bytes using the `CommsService`.

- `EthernetPortList` Allows adding, removing & configuring of TCP & UDP ports, these may be used as inputs to supported _sources_, 
and can be set as outputs in the _output message module_.
- `ExternalControlPortList` Represents external control ports on the device, these may be used as inputs to supported _sources_.
- `PowerPassPortList` Allows management of power pass ports (e.g. enabling/disabling).
- `SerialPortList` Allows management of serial ports (e.g. setting baud rate), these may be used as inputs to supported _sources_,
  and can be set as outputs in the _output message module_.
- `TriggerPortList` Allows management of trigger ports.


### Common Messages

Unlike the component messages, the common messages have no required suffixes. 
Common messages may only contain other common messages, whereas _component_ messages
may contain other component messages _and_ common messages.

Common messages include `LeverArms`, `MountingAngles`, `EthernetPort`, `SerialPort`, and more.
Common messages also include the `RequestEnvelope` and `ResponseEnvelope` - to see how these are used,
see [Using Non-gRPC Modes](#using-non-grpc-modes).

### Additional Message Types
#### Reference Messages
Messages ending in the word _"Reference"_ allow one message to point to another.
Note that these references are read-only.
```python
import sonardyne_api as son
with son.WrapperGrpc('0.0.0.0', 8103) as wrapper:  # Device IP address & gRPC port:
    result = wrapper.set_configuration(son.GnssSourceConfiguration(input_data_port=son.DataPortReference(set_uid=son.UniqueID(name="TCP-5000"))))
    print(result)
```
In this example, the _input_data_port_ of a GNSS source is set using a `DataPortReference`.
the `DataPortReference` references a data port - an ethernet, serial, or external control port.
The `DataPortReference` can be set using `set_uid`, which allows us to refer to other configuration by
unique ID value or by name.

```python
son.DataPortReference(set_uid=son.UniqueID(name="TCP-5000"))
son.DataPortReference(set_uid=son.UniqueID(value=3245395109))
```
The data port reference has "set" fields which are used to reference to a particular data port.
```python
son.DataPortReference(set_none=True)
```
The `set_none` field may be used to clear the reference.
```python
son.DataPortReference(set_any_ethernet_port=True)
son.DataPortReference(set_any_external_control_port=True)
son.DataPortReference(set_any_serial_port=True)
```
The data port reference also has `set_any` fields, these allow data port references
to be set when no unique ID values are known.

Below is an example of a `DataPortReference` being set:
```python
import sonardyne_api as son
with son.WrapperJsonTcp('0.0.0.0', 8111) as wrapper:  # Device IP address & gRPC port:
    print(wrapper.set_configuration(son.GnssSourceConfiguration(input_data_port=son.DataPortReference(set_uid=son.UniqueID(name="TCP-5000")))))
```
When using the JSON interface over a TCP server (in this example on port 8111) 
the following message contents can be observed; these can be seen by using
the 'Comms Viewer' functionality in the SPRINT-Nav UI.
```json
{
  "@type": "type.googleapis.com/sonardyne.api.common.envelope.RequestEnvelope",
  "uid": 1,
  "requests": [
    {
      "@type": "type.googleapis.com/sonardyne.api.services.configuration_service.SetConfigurationRequest",
      "configuration": {
        "@type": "type.googleapis.com/sonardyne.api.sources.gnss_source.GnssSourceConfiguration",
        "inputDataPort": {
          "setUid": {
            "name": "TCP-5000"
          }
        }
      }
    }
  ]
}
```
This is the JSON message sent by the running the example, with the partially populated _inputDataPort_ field.
```json
{
 "@type": "type.googleapis.com/sonardyne.api.common.envelope.ResponseEnvelope",
 "uid": 10,
 "responses": [
  {
   "@type": "type.googleapis.com/sonardyne.api.services.configuration_service.SetConfigurationResponse",
   "timestamp": {
    "common_time_seconds": 1764954922.1296844,
    "instrument_time_seconds": 225.084287999
   },
   "configuration": {
    "@type": "type.googleapis.com/sonardyne.api.sources.gnss_source.GnssSourceConfiguration",
    "uid": {
     "value": "887217899",
     "name": "GNSS Source"
    },
    "input_data_port": {
     "readonly_uid": {
      "value": "3245395109",
      "name": "TCP-5000"
     },
     "readonly_ethernet_port_reference": {
      "uid": {
       "value": "3245395109",
       "name": "TCP-5000"
      },
      "source_port": 5000,
      "data_encoding": "DATA_ENCODING_NONE",
      "tcp_server": {
       "maximum_connections": 20
      }
     }
    },
    "lever_arms": {},
    "fallback_horizontal_uncertainty_metres": 5,
    "scale_uncertainty": 1,
    "gnss_depth_mode": "GNSS_DEPTH_MODE_ELLIPSOIDAL"
   },
   "result": {
    "success": "OUTCOME_SUCCESS"
   }
  }
 ]
}
```
This is the received message, with the fully populated _inputDataPort_ (with _input_data_port_ and
_readonly_ethernet_port_reference_ fields).

The data port reference has "set" fields, and "readonly" fields.
The readonly fields are populated when a data port reference is returned from the device.

## Using Non-gRPC Modes
The API may be used without gRPC by sending proto messages as either JSON or Framed binary messages. 
Framed messages are serialised Protobuf messages wrapped in a Sonardyne Simple Binary Message and
[COBS](https://en.wikipedia.org/wiki/Consistent_Overhead_Byte_Stuffing) encoded.

In non-gRPC modes, only message types ending in _"Envelope"_ can be sent over the API. For example,
a `RequestEnvelope` can be sent as JSON and a corresponding `ResponseEnvelope` will be returned.
These envelopes can be matched by setting the UID on the `RequestEnvelope`.

A `RequestEnvelope` can contain any number of messages ending in _"Request"_ 
e.g. `SetConfigurationRequest` or `SendCommandRequest`, 
and the returned `ResponseEnvelope` will match one to one with responses e.g. (`SetConfigurationResponse` or `SendCommandResponse`).

When streaming data in or out over non-gRPC modes, the `ObservationEnvelope` is used. When subscribing
to changing configurations, the `ConfigurationEnvelopes` is used. For more information on subscribing
to streams, see [Subscribing to Streams](#subscribing-to-streams).

## Subscribing to Streams

Several services allow data streaming, these are:

- `ObservationStream` (on the `ObservationService`). _Allows the monitoring of outputs from components e.g.
streaming out readings from a `PressureSensor` or `GnssSource`. Data can also be streamed into these components e.g.
streaming `GnssSourceObservations` into a `GnssSource`._
- `CommsStream` (on the `CommsService`). _Allows the monitoring of data being sent and received over serial and ethernet,
also allows data to be sent out over these ports._
- `ConfigurationStream` (on the `ConfigurationService`). _Allows the monitoring changing configurations._


Messages ending in _"SubscriptionRequest"_ (e.g. `CommsSubscriptionRequest`) allow the setting of
matching and rejection criteria based on message typenames and UniqueIDs.

For example, possible subscriptions include:

- All messages with a specified suffix e.g. _"SensorObservation"_.
- All messages excluding a specified suffix e.g. _"Observation"_ messages excluding _"SourceObservation"_.
- All messages matching a specified unique ID name e.g. "GNSS Source.
- All messages matching a specified unique ID value e.g. 19572865462 (supposing this is the UID of a particular component).

Streams can be subscribed to by sending a _"SubscriptionRequest"_ message. For example, an `ObservationSubscriptionRequest`
can be sent to the `ObservationStream` on the [observation service](#observation-service) to listen to pressure sensor readings.

The `ConfigurationSubscriptionRequest` may be used to monitor changing configurations.


The `CommsSubscriptionRequest` may be used to monitor incoming and outgoing data over a port (serial or ethernet).
The `CommsEnvelope` allows the sending of data out over a port, and must contain messages ending in _"Comms"_ e.g.
`DataPortComms`.




