# Getting Started

```commandline
pip install ../../Python/
```
_Installs the sonardyne_api python library._

## API Wrapper Implementations
Three wrapper implementations are provided as part of the **sonardyne_api** Python libary:

- `WrapperGrpc` _Allows command and control via gRPC interface._
- `WrapperJsonTcp` _Allows command and control via JSON interface._
- `WrapperFramedTcp` _Allows command and control via COBS-framed, Sonardyne Simple Binary Protocol messages._

Each of these implementations allow setting and getting of configurations, sending of commands,
configuration streaming, observation streaming, and comms streaming.

If using `WrapperFramedTcp`, it is important that COBS-framing is enabled for the port
in use.

## Exception Handling
Calls to set_configuration, get_configuration, and send_command
will raise an exception if not actioned on the device. Specific exception types are:

- `ResultFailureException` _Action failed._
- `ResultInvalidException` _Action not possible due to invalid request contents._
- `ResultRestrictedException` _Action not possible due to user-level restrictions._
- `ResultUnspecifiedException` _No success was set on the returned message._

These exception types inherit from _ResultException_,
which can be used to catch all the specific exception types.

The following example is taken from
`python3 exception_handling.py`.
```python
import sonardyne_api as son

with son.WrapperGrpc('0.0.0.0', 8103) as wrapper:  # Device IP address & gRPC port:
    try:
        wrapper.set_configuration(son.DeviceInstallationModuleConfiguration(
            lever_arms=son.LeverArms(forward_metres=1, starboard_metres=4, down_metres=2),
        ))
        print("Request successful.")
    except son.ResultInvalidException as exception:
        print(f"Error, request invalid: {exception}")
    except son.ResultFailureException as exception:
        print(f"Error, request failed: {exception}")
    except son.ResultException as exception:
        print(f"Error: {exception}")
```

### Getting the Running API Version
The following example is taken from
`python3 get_version.py`.
```python
import sonardyne_api as son

with son.WrapperGrpc('0.0.0.0', 8103) as wrapper:  # Device IP address & gRPC port:
    version = wrapper.get_version().api_version
    print(f"{version.major}.{version.minor}.{version.patch}")
```
_Returns the API version running on the device.

### Getting Device Information
The following example is taken from
`python3 device_information.py`.
```python
import sonardyne_api as son

with son.WrapperGrpc('0.0.0.0', 8103) as wrapper:  # SPRINT-Nav ip address & port
    print(wrapper.get_configuration(son.DeviceModuleConfiguration))
```
_Returns information about the connected device._

### Getting Device Information
The following example is taken from
`python3 device_information.py`.
```python
import sonardyne_api as son

with son.WrapperGrpc('0.0.0.0', 8103) as wrapper:  # SPRINT-Nav ip address & port
    print(wrapper.get_configuration(son.SprintModuleConfiguration))
```
_Returns information about the connected device, specific to a SPRINT._

## Setting Device Lever Arms
The following example is taken from
`python3 setting_device_lever_arms.py`.
```python
import sonardyne_api as son

with son.WrapperGrpc('0.0.0.0', 8103) as wrapper:  # SPRINT-Nav ip address & port
    print(wrapper.set_configuration(son.DeviceInstallationModuleConfiguration(
        lever_arms=son.LeverArms(forward_metres=0.5, starboard_metres=1.2, down_metres=4.6),
        mounting_angles=son.MountingAngles(roll_radians=0.1, pitch_radians=0.2, heading_radians=0.3)
    )))
```
_Sets the device installation lever arms relative to the vessel._

## Setting Source Lever Arms
The following example is taken from
`python3 setting_source_lever_arms.py`.
```python
import sonardyne_api as son

with son.WrapperGrpc('0.0.0.0', 8103) as wrapper:  # SPRINT-Nav ip address & port
    print(wrapper.set_configuration(son.GnssSourceConfiguration(
        lever_arms=son.LeverArms(forward_metres=1.5, starboard_metres=-2.6, down_metres=3.2)
    )))
    print(wrapper.set_configuration(son.XposSourceConfiguration(
        lever_arms=son.LeverArms(forward_metres=0.5, starboard_metres=-4.1, down_metres=-1.0)
    )))
```
_Sets GNSS and XPOS lever arms._


## Basic Commands
Several of the following examples are taken from
`python3 basic_commands.py`.
```python
import sonardyne_api as son

with son.WrapperGrpc('0.0.0.0', 8103) as wrapper:  # SPRINT-Nav ip address & port
    wrapper.send_command(son.AhrsAlgorithmCommandReset())
```
_Performs a hard reset._

```python
import sonardyne_api as son

with son.WrapperGrpc('0.0.0.0', 8103) as wrapper:  # SPRINT-Nav ip address & port
    wrapper.send_command(son.EthernetPortListCommandAddPort(ethernet_port=son.EthernetPort(source_port=8130, tcp_server=son.TcpServerParameters())))
```
_Adds a TCP server on port 8130._

```python
import sonardyne_api as son

with son.WrapperGrpc('0.0.0.0', 8103) as wrapper:  # SPRINT-Nav ip address & port
    wrapper.send_command(son.EthernetPortListCommandRemovePort(uid_to_delete=son.UniqueID(name="TCP-8130")))
```
_Removes the TCP server on port 8130 by name._

```python
import sonardyne_api as son

with son.WrapperGrpc('0.0.0.0', 8103) as wrapper:  # SPRINT-Nav ip address & port
    wrapper.send_command(son.EthernetPortListCommandRemovePort(source_port_to_delete=8130))
```
_Removes the TCP server on port 8130 by port._

```python
import sonardyne_api as son

with son.WrapperGrpc('0.0.0.0', 8103) as wrapper:  # SPRINT-Nav ip address & port
    wrapper.send_command(son.DeviceModuleCommandShutdown())
```
_Shuts the device down._

## Observing Pressure Sensor & Depth Source Data
The following example is taken from
`python3 observing_sensor_data.py`.

```python
import sonardyne_api as son

with son.WrapperGrpc('0.0.0.0', 8103) as wrapper:  # SPRINT-Nav ip address & port
    observation_stream = wrapper.open_observation_stream(son.ObservationSubscriptionRequest(
        observation_subscriptions=[
            son.ObservationSubscription(match_type_name_suffix="PressureSensorObservation"),
            son.ObservationSubscription(match_type_name_suffix="DepthSourceObservation")
        ]
    ))
    try:
        while True:
            for message in observation_stream.recv():
                if isinstance(message, son.PressureSensorObservation):
                    print("pressure (pascals):", message.pressure_data.pressure_pascals)
                elif isinstance(message, son.DepthSourceObservation):
                    print("depth (metres):    ", message.depth_data.depth_metres)
    except KeyboardInterrupt:
        pass    
```
_Prints recorded pressure and depth derived from pressure._


## Observing Navigation Data
The following example is taken from
`python3 observing_navigation_data.py`.

```python
import sonardyne_api as son

with son.WrapperGrpc('0.0.0.0', 8103) as wrapper:  # SPRINT-Nav ip address & port
    observation_stream = wrapper.open_observation_stream(son.ObservationSubscriptionRequest(
        observation_subscriptions=[
            son.ObservationSubscription(
                match_uids=[son.UniqueID(name="Common Reference Point")],  # Try 'Remote Point 1'
                match_type_name_suffix="Observation")
        ]
    ))
    try:
        while True:
            for message in observation_stream.recv():
                if isinstance(message, son.NavigationModuleObservation):
                    print(message)
    except KeyboardInterrupt:
        pass
```
_Prints navigation data valid to the common reference point._


## Writing Messages to Serial Ports
The following examples are taken from
`python3 writing_to_ethernet_ports.py`.

```python
import time
import random
import sonardyne_api as son

with son.WrapperGrpc('0.0.0.0', 8103) as wrapper:  # SPRINT-Nav ip address & port
    comms_stream = wrapper.open_comms_stream()
    try:
        while True:
            comms_stream.send(son.DataPortComms(
                uid=son.UniqueID(name="TCP-8110"),  # Try 'Serial A1'
                data_direction=son.DataDirection.DATA_DIRECTION_OUTPUT,  # DATA_DIRECTION_INPUT spoofs inputs on this port.
                data=f"Hello World! {random.randrange(100)}".encode())
            )
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass
```
_Sends 'Hello World!' messages at 10Hz, post-fixed with a random number._


## Ports, Outputs & Observing TCP Outputs
The following examples are taken from
`python3 observing_tcp_outputs.py`.

```python
import sonardyne_api as son

with son.WrapperGrpc('0.0.0.0', 8103) as wrapper:  # SPRINT-Nav ip address & port
    print(wrapper.set_configuration(son.EthernetPortListConfiguration(ethernet_ports=[
        son.EthernetPort(source_port=8110, tcp_server=son.TcpServerParameters()),
        son.EthernetPort(source_port=8111, tcp_server=son.TcpServerParameters()),
        son.EthernetPort(source_port=8112, tcp_server=son.TcpServerParameters()),
        son.EthernetPort(source_port=8113, tcp_server=son.TcpServerParameters()),
        son.EthernetPort(source_port=8114, tcp_client=son.TcpClientParameters(server_ip_address="192.168.179.50")),
        son.EthernetPort(source_port=8115, udp_socket=son.UdpSocketParameters(destination_ip_address="192.168.179.60"))
    ])))
```
_Sets 6 ethernet ports for use on the device. 4 TCP servers, 1 TCP client & 1 UDP socket._

```python
import sonardyne_api as son

with son.WrapperGrpc('0.0.0.0', 8103) as wrapper:  # SPRINT-Nav ip address & port
    print(wrapper.set_configuration(son.OutputMessageModuleConfiguration(
        output_message_list=son.OutputMessageList(
            output_messages=[
                son.OutputMessage(
                    output_message_type=son.OutputMessageType.OUTPUT_MESSAGE_TYPE_GGA,
                    rate_hz=100.0,
                    remote_point=son.RemotePointReference(set_uid=son.UniqueID(name="Common Reference Point")),
                    data_port_output=son.DataPortReference(set_uid=son.UniqueID(name="TCP-8110"))
                )
            ]
        )
    )))
```
_Outputs GGA messages at 100Hz on TCP-8110._

```python
import sonardyne_api as son

with son.WrapperGrpc('0.0.0.0', 8103) as wrapper:  # SPRINT-Nav ip address & port
    comms_stream = wrapper.open_comms_stream(son.CommsSubscriptionRequest(
        comms_subscriptions=[
            son.CommsSubscription(match_uids=[son.UniqueID(name="TCP-8110")])
        ]
    ))
    try:
        while True:
            for message in comms_stream.recv():
                if isinstance(message, son.DataPortComms):
                    print("->" if message.data_direction == son.DATA_DIRECTION_INPUT else "<-", message.data)
    except KeyboardInterrupt:
        pass
```
_Listens to data on the TCP-8110 port._


## Communicating with JSON & Framed Ports
The API can be interfaced with without gRPC, by sending data via TCP, UDP, or serial ports.
This can be done by sending "Envelope" messages as either JSON or "framed" messages.
The framed messages are serialised protos, packed in Sonardyne Simple Binary Messages, and COBS encoded.

"Envelope" messages include:
- `RequestEnvelope`
- `ResponseEnvelope`
- `ConfigurationEnvelope`
- `ObservationEnvelope`
- `CommsEnvelope`

For each `RequestEnvelope`, a `ResponseEnvelope` will be returned with a matching unique ID.
A `RequestEnvelope` can be packed with any message with the suffix "Request".

Any of the examples which use `WrapperGrpc` can be replaced with `WrapperFramedTcp`
or `WrapperJsonTcp`. If sending framed messages, the port used for communication must have 
framing enabled.


## Additional Examples
For additional examples, see the _algorithms_, _modules_, _ports_, _sensors_, _services_ & _sources_ folders.

