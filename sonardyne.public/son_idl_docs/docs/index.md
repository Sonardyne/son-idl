# About

## What is the API?

Sonardyne's API is designed to use off-the-shelf technologies for interfacing to Sonardyne instruments and systems.  
This software does not collect, process, or store any personal data.

A typical integration will involve using a combination of:  

* Web User Interface
* API
* Input and Output messages
  
Information on these pages will assist a developer or integrator by providing integration examples, suggested tooling, and all required reference documentation. 

## Which products use the API?

The below Sonardyne products support the Sonardyne API:

|System/Instrument|Version|
|--------|--------|
|SPRINT-Nav Mini| 1.2.607|

??? son-info "Future Support"

    Future Sonardyne products will utilise a common version of this API


## Primary interface (gRPC and Protobuf) vs Secondary interface (JSON)

The gRPC interface is in a binary format, and will use fewer bytes to send each command which saves bandwidth and reduces processing time/latency on the instrument. The JSON interface is a layer added to the gRPC interface to allow sending and receiving of JSON string representations of Protocol Buffers.
See the [Technology Explainer](technology-explainer.md) for more details.



