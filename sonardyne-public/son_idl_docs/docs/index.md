# About

## What is the API?

Sonardyne's API is designed to use off-the-shelf technologies for interfacing to Sonardyne instruments and systems.  
This software does not collect, process, or store any personal data.

A typical integration will involve using a combination of:  

* Web User Interface
* API
* Input and Output messages
  
Information on these pages will assist a developer or integrator by providing [integration examples](integration.md), [suggested tooling](external_reference.md), [code examples](quick-start.md), and all required reference documentation. 

## Which products use the API?

The Sonardyne products listed below support the Sonardyne API:

|System/Instrument|Version|
|--------|--------|
|SPRINT-Nav Mini| 1.3.x|

??? son-info "Future Support"

    Future Sonardyne products will utilise a common version of this API

??? son-info "Previous versions"

    When major updates are made to the interface previous versions of this documentation can be found below.

    |System/Instrument|Instrument version|Last idl version|
    |---|---|---|
    |SPRINT-Nav mini|1.2.x|[v0.9.2](https://github.com/Sonardyne/son-idl/releases/tag/v0.9.2)|

## Primary interface (gRPC and Protobuf) vs Secondary interface (JSON)

The gRPC interface is in a binary format, and will use fewer bytes to send each command, which saves bandwidth and reduces processing time/latency on the instrument. The JSON interface is a layer added to the gRPC interface to allow sending and receiving of JSON string representations of Protocol Buffers. In future the gRPC interface will be expanded to include streaming data for complete command and control, this may not be enabled or possible with the JSON interface.
See the [Technology Explainer](technology-explainer.md) for more details.



