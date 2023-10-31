## HNAV
The Hybrid Navigation (HNAV) message includes all information required for vehicle guidance, control and navigation.
All fields will be initialised to 0, once a field has been assigned a value it will retain that value until a further update is available. The status bits should be used to determine when data is old/stale.
The HNAV requires the Simple binary protocol to successfully decode the message, see appendix G3 Simple Binary Protocol. 
All data is transmitted LSB first.
 
[A C++ HNAV Decoder is available on Sonardyne's Github](https://github.com/Sonardyne/sprint-nav-mini-hnav)

### Simple Binary Protocol

|Data Field|LSB/(FixedValue)|Range|Data Type|Size(Bytes)|Notes|
|---|---|---|---|---|---|
| Header | (0xAA 0xBF) | 0 to 255 | UINT8 | 2 | Header to denote the start of the packet |
| Version | (0) | 0 to 255 | UINT8 | 1 | Version of protocol |
| ID | (0) | 0 to 65535 | UINT16 | 2 | Message ID (HNAV = 0) see Note 1 |
| Size | \- | 0 - 4096 | \- | 2 | Size of data field in bytes, see note 2 |
| Counter | \- | 0 to 255 | \- | 1 | Counter per message, increments before rolling over to 0. Allows detection of out of order receipt. |
| Spare | \- | \- | \- | 2 | Not Used |
| Payload | \- | \- | \- | \- | Message data (e.g. HNAV) |
| Checksum | \- | \- | UINT16 | 2 | CRC-X.25: 0x1021. Covers all bytes before and including data bytes. 

??? son-info "Notes"

    Each Output message has its own Message ID, the message ID of HNAV is 0

    Each Output message will have a fixed size, the HNAV is 55 Bytes


### HNAV Definition

|Data Field|LSB/(FixedValue)|Range|Data Type|Size(Bytes)|Notes|
|---|---|---|---|---|---|
| Version | 0 | 0 to 255 | UINT8 | 1 | Version of message |
| Time of Validity (UTC) | 10\-6 seconds | \- | UINT64 | 8 |  |
| Latitude | 2-31×90 deg | +/- 90 deg | INT32 | 4 | Not populated in Guidance |
| Longitude | 2-31×180 deg | +/- 180 deg | INT32 | 4 | Not populated in Guidance |
| Depth | 1mm | +/- 12,000m | INT32 | 4 | Depth at vehicle CRP |
| Altitude | 0.01m | 0 to 600m | UINT16 | 2 | Altitude is referenced from SPRINT-Nav Mini’s measurement point to the seabed (not compensated for CRP measurements). |
| Roll | 0.0055 deg | +/- 180 deg | INT16 | 2 |  |
| Pitch | 0.0055 deg | +/- 90 deg | INT16 | 2 |  |
| Heading | 0.0055 deg | 0 to 360 deg | UINT16 | 2 |  |
| Fwd Velocity | 1mm/s | +/-30m/s | INT16 | 2 |  |
| Stbd Velocity | 1mm/s | +/-30m/s | INT16 | 2 |  |
| Dwn Velocity | 1mm/s | +/-30m/s | INT16 | 2 |  |
| Fwd Ang Rate | 0.011 deg/s | +/-300deg/s | INT16 | 2 |  |
| Stbd Ang Rate | 0.011 deg/s | +/-300deg/s | INT16 | 2 |  |
| Dwn Ang Rate | 0.011 deg/s | +/-300deg/s | INT16 | 2 |  |
| Sound Velocity | 0.03m/s | 1375 to 1900 m/s | UINT16 | 2 |  |
| Temperature | 0.01°C | +/- 100°C | INT16 | 2 |  |
| Position Quality | \- | \- | FLOAT32 | 4 | Not populated in Guidance 2D Quality (CEP50) |
| Heading Quality | 0.005° | 0 to 180 deg | UINT16 | 2 |  |
| Velocity Quality | 1mm/s | 0 to 30 m/s | UINT16 | 2  | 2D Quality       |
| Status           | \-    | \-          | \-     | \- | See Status table |

### HNAV Bit Fields

|Status Bit|Field name|Notes/Bit Set|
|---|---|---|
| 0 | System Error | No error reported by system = 0 System Error reported = 1 |
| 1 | Mode | Alignment mode = 0 Hybrid mode = 1 |
| 2 | Heading | valid = 0 Invalid = 1 |
| 3 | Altitude | valid = 0 Invalid = 1 |
| 4 | Velocity | valid = 0 Invalid = 1 |
| 5 | Depth | valid = 0 Invalid = 1 |
| 6 | Sound Velocity | valid = 0 Invalid = 1 |
| 7 | Temperature | valid = 0 Invalid = 1 |
| 8 | Spare | Not Used |
| 9 | Position | valid = 0 Invalid = 1 |
| 10 | UTC Time | valid = 0 Invalid = 1 |
| 11 | Spare | Not Used |
| 12 | Spare | Not Used |
| 13 | Spare | Not Used |
| 14 | Spare | Not Used |
| 15 | Spare | Not Used |
