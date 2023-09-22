## gRPC and Protocol Buffers

#### What is gRPC?

[gRPC](https://grpc.io/) (a self-containing acronym: '**g**RPC **R**emote **P**rocedure **C**alls') is an open source universal RPC framework [licensed under Apache 2.0](https://github.com/grpc/grpc/blob/master/LICENSE). It allows clients and servers to be generated in a variety of supported languages and run on a variety of platforms. Complexity from communicating between different languages or platforms is handled for the developer by gRPC.

#### What are Protocol Buffers?

[Protocol Buffers](https://protobuf.dev/) (or Protobuf) are a language-neutral, platform-neutral extensible mechanism for serialising structured data. They allow data to be stored in an efficient way when serialised, while still being easy to use for the programmer and allowing backwards-compatible updates to the interface. They are used by gRPC as the Interface Definition Language (IDL) and serialisation toolset.

#### Building gRPC for different languages

gRPC + Protobuf can be used with [a variety of platforms](https://grpc.io/docs/languages/). In general, the steps are:
- Install dependencies (protoc etc).
- Use protoc to generate code from the .proto files.
- Include the generated code in clients/servers.

#### gRPC advantages and disadvantages

- `+` gRPC is high-performance and produces compact binary messages. 
- `+` It can generate the necessary code for multiple platforms/languages.
- `-` The binary format of Protobuf is not human-readable.



## JSON

#### What is the JSON interface?

The JSON interface is a layer in front of the gRPC interface, which allows a user to send a JSON string representation of the Protocol Buffer. The instrument will receive this string and convert it, using the same backend code as the gRPC interface (this ensures that both interfaces are guaranteed to behave in the same way).

#### JSON advantages and disadvantages

- `+` JSON is human-readable and may be a more user-friendly way of performing comms with the instrument.
- `+` It can be used for sending commands by hand for testing, without use of extra software tools.
- `-` Use of JSON strings will make messages larger, and will add a parsing overhead on the instrument.

#### How to use it

Configure the API using the instrument's webUI. Select JSON and select which port is to be used, then send a string representation of the Protocol Buffer to this port.
Below is an example JSON string to perform a SetState command, which will perform the following:

- Enable GNSS, XPOS, and USBL as aiding sources
- Set sound velocity source to salinity-derived
- Set salinity to 39
- Set DVL update rate to 5Hz fixed

``` json title="JSON string for SetState"
{
  "configuration": {
    "aiding_configurations": [
      {
        "enable_gnss": "ENABLED",
        "enable_xpos": "ENABLED",
        "enable_usbl": "ENABLED"
      }
    ],
    "sound_velocity_configurations": [
      {
        "sound_velocity_type": "INTERNAL_SALINITY",
        "manual_salinity_value": 39
      },
    ],
    "doppler_velocity_configurations": [
      {
        "update_rate": "FIXED_5HZ"
      }
    ]
  }
}
```
