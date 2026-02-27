The _**Port List**_ component represents some collection of data inputs/outputs.

Some port lists, e.g. ethernet port lists, can have entries added and removed.
Other port lists, e.g. serial port lists, represent physical ports on the device, so are fixed-length.

On a data port such as a SerialPort or an EthernetPort, it is possible to send and receive _**PortComms**_
using the _**CommsService**_.
