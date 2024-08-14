## Sprint-Nav Mini

SPRINT-Nav Mini is designed to be easily integrated into multiple classes of vehicle/vessel. All available inputs and outputs, as well as detailed integration documents, are described in the product manual and the manual should be considered the reference for the use of these systems. This section provides a broad overview of how the API alongside other messages can be used with a SPRINT-Nav mini.

#### Physical installation

SPRINT-Nav Mini can be installed at any convenient location where the DVL has an unobstructed view of the seabed. However, to gain optimal performance there are some guidelines. 

CAD .stp files are available on Sonardyne's [knowledge base](https://www.sonardyne.com/products-knowledge-base/sprint-nav-mini-stp-files/)

??? son-info "Installation Guidelines"
    - The location must not be subject to excessive vibration or impulse shock.  
    - The location must not exceed the environmental limits for the temperature.  
    - The location must provide a mounting surface that is of sufficient strength to support the weight of the SPRINT-Nav Mini safely and without flexing.  
    - The location must provide access for power and communication connections.  
    - The location must provide line of sight to the seabed for all four DVL transducers abiding by the clearance levels. 

 
#### Time

The SPRINT-Nav Mini can be time synchronised to UTC. This can be achieved via NTP or by providing a 1PPS signal and ZDA NMEA-0183 message from a GPS receiver or similar clock source. 

If the serial communication link has a known, stable latency then it is possible to use ZDA only, but 1PPS is recommended where possible. If the SPRINT-Nav Mini has been time synchronised and its quality is less than or equal to 0.5s it is possible to stop providing ZDA messages and simply rely on 1PPS aiding without any loss of accuracy.

To improve robustness and usability, the SPRINT-Nav Mini incorporates a feature that automatically detects the relationship between the ZDA and 1PPS without any configuration. The SPRINT-Nav Mini achieves this by treating ZDA and 1PPS aiding separately: by filtering over several ZDA and 1PPS observations, it alleviates the requirement for a user to configure the ZDA and 1PPS relationship. In addition, the SPRINT-Nav Mini automatically detects the leading edge of the 1PPS trigger (assuming the pulse width is much less than 0.5s). 
If external time synchronisation is lost the INS can continue to maintain an estimate of UTC time using its internal clock (~5ppm drift).

The ZDA message should conform to the NMEA 0183 standard. The message can be received on any channel or over Ethernet. The 1PPS signal should be a 5V DC pulse with >1 µs duration. The signal can be fed to SPRINT-Nav Mini via any of the trigger channels. 

There are three modes available:  

* None 
* ZDA (+1PPS)
* NTP

Time can also be output by a SPRINT-Nav Mini via an output ZDA + 1PPS, typically used for time synchronising other onboard survey sensors. 

#### Sound velocity

Accurate knowledge of Sound Velocity is crucial for Hybrid (DVL/INS) navigation, as such SPRINT-Nav Mini supports three types of SV. It is recommended to always use external SV for operations requiring high navigation accuracy. 

* Manual
    * Provides an ability to type in a Manual SV, to be used when SV is very stable or as a backup. 
* Derived
    * Uses water temperature and a manually entered salinity value to calculate SV.
* External 
    * Uses an external SV sensor to input a direct read sound velocity into the SPRINT-Nav Mini.

![Valeport SV Sensors](./assets/Images/Valeport.jpg){: style="width: 40%;" data-title="Valeport SV Sensors."  }

??? son-info "Notes on SV"
    - Sonardyne find that a 25mm SV sensor provides enough accuracy for navigation and minimises risk of damage to the SV sensor.
    - Place the SV sensor as close to the DVL as possible.
    - Place the SV Sensor within the same body of water as the DVL.
    - Any error in SV will often appear as an along track error if no external aiding source is provided i.e. GNSS or USBL.    

#### DVL mounting

SPRINT-Nav Mini can be mounted at any angle however, typically the DVL is mounted facing directly down on the vehicle providing the best tracking of the seabed. Occasionally on trenchers or other vehicles where a direct view of the seabed is not possible, the DVL may be installed at an angle. 

![DVL_Beams](./assets/Images/Mini_Beams.gif){: style="width: 40%;" data-title="SPRINT-Nav Mini beams."  }

#### Position aiding

##### USBL
SPRINT-Nav Mini supports USBL aiding via industry-standard telegrams. 

##### GNSS
SPRINT-Nav Mini uses GNSS for aiding of both time and position via industry-standard telegrams.

##### XPOS
SPRINT-Nav Mini supports Sonardyne's proprietary XPOS message for aiding of generic position observations. Typically an XPOS message is provided to a SPRINT-Nav Mini when a vehicle is docked, initialising on deck or any scenario whereby a GNSS or USBL message is not appropriate. 

## AUV x SPRINT-Nav Mini

SPRINT-Nav Mini has been designed for AUV integration and this section will describe an example integration into a 10" AUV, with a common setup with a mix of input, output, C2 (command & control) and peripheral survey sensors. 

??? son-info "Inputs"
    - GNSS
    - USBL
    - Sound Velocity 

??? son-info "Outputs"
    - HNAV
    - ZDA + 1PPS

??? son-info "C2"
    - gRPC API

??? son-info "Survey Sensors"
    - Voyis Recon - Laser
    - Voyis Recon - Camera

![Sparus](./assets/Images/Sparus.jpeg){: style="height: 50vh;" data-title="Sparus AUV" }

### Mounting location

In this example the SPRINT-Nav Mini is mounted in the free flooded nose cone of a [Sparus](https://ocean.soton.ac.uk/smarty200). The DVL has a clear view of the seabed with no obstructed beams. 

![Sparus inner view](./assets/Images/sparus_inside.jpg){: style="height: 50vh;" data-title="Sparus AUV mounting location" }

### Aiding sensors
SPRINT-Nav Mini can have multiple aiding sensors enabled at once so it will seamlessly use GNSS on surface and USBL when it becomes available subsea. 

#### GNSS
When on the surface the AUV receives both positioning updates (GGA) and timing (ZDA + 1PPS) from the onboard GNSS which is mounted on a mast at the rear of the vehicle. 

??? son-info "GNSS aiding on an AUV"
    * When configuring a GNSS in SPRINT-Nav Mini, consider that GNSS accuracy estimates are often optimistic. Sonardyne recommend setting a relaxed manual GNSS quality.
    * GNSS often gives erroneous positions as a vehicle surfaces and when a vehicle dives. SPRINT-Nav Mini will reject data that falls outside its own position error estimate however, why not consider disabling GNSS when diving and for a period of time after breaking the surface. 
    * SPRINT-Nav Mini doesn't currently use VTG for velocity aiding, but will in the future. 


#### USBL
When submerged, the AUV utilises Sonardyne's Mini Ranger 2 Robotics Pack to track an [AvTrak 6 Nano](https://www.sonardyne.com/products/avtrak-6-nano-auv-swarm-tracking-and-communications/) mounted in the AUV. This AvTrak 6 Nano is used for communicating with the surface and also for sending position updates into the SPRINT-Nav Mini. 

??? son-info "USBL Aiding a SPRINT-Nav Mini on an AUV"
    * All AvTrak 6 nano's, when being tracked by "Robotics Pack", can output a time-stamped GGA message directly from their serial port in addition to the native SPOS format which can be interfaced directly to the SPRINT-Nav Mini. See the AvTrak 6 Nano manual for more details. 
    * Ranger 2 Robotics Pack can track up to 10 vehicles at once, simultaneously sending them correct absolute position information as well as exchanging telemetry. 

#### Sound velocity
For sound velocity a Valeport 25 mm SVS is used, outputting the valeport standard telegram into the vehicle control system and then over UDP into the SPRINT-Nav Mini.  

### Outputs

#### HNAV
HNAV is output at 100 Hz for vehicle guidance purposes. All status flags are decoded and presented in the AUV Web UI so that the operator knows when it is ok for the vehicle to begin operations. Certain flags from the HNAV are decoded which will cause vehicle behaviours. See [Reference](reference.md) for further details.

??? son-info "HNAV Notes"
    * If an output message is populated at a rate quicker than the rate of the incoming sensor the HNAV status field will reflect invalid (because the flag indicates invalid or old). For example in a 100Hz output HNAV message, if DVL is coming into the SPRINT-Nav Mini at 10Hz, in excess of 90% of messages would be expected to have an invalid altitude flag. 
    * HNAV can be input directly into EIVA Naviscan in a traditional survey setup. 

#### Timing
Timing is crucial for survey deliverables as all sensors which are logging data must log against a common time base. This is typically UTC. SPRINT-Nav Mini can be configured to both receive time updates and will also persist time when subsea.

In this example a ZDA + 1PPS output is configured from the SPRINT-Nav Mini into all survey sensors on the AUV. 

??? son-info "ZDA + 1PPS output"
    * Outputting a ZDA + 1PPS doesn't mean that time won't drift when the vehicle is subsea, but all sensors will be in the same time base. 
    * SPRINT-Nav Mini constantly models and monitors time, as such when the AUV surfaces and GNSS timing is available once again, SPRINT-Nav Mini's UTC time will adjust to reflect the correct UTC time. 

### C2
Command and Control of a SPRINT-Nav Mini uses the Sonardyne gRPC API to modify settings dynamically during a mission as and when required, either autonomously or via the user-developed AUV interface. 

??? son-info "Suggested SPRINT-Nav Mini C2"
    * Via the user-developed AUV interface the AUV operator can reset the INS algorithm instantaneously if required.
    * If the vehicle/operator knows that GNSS is erroneous it can be disabled as an aiding source for a period of time. 
    * If the SPRINT-Nav HNAV message flags a problem with the Sound Velocity sensor, the C2 changes the SV configuration to derived and then manual. 
    * The user-developed AUV interface allows a user to select which aiding sources should be used by the AUV pre-dive without using the SPRINT-Nav Mini user interface.
    * The gRPC API is much lower bandwidth than the web UI allowing for over the horizon low bandwidth operations. 
     


### Data 
For high accuracy survey products, [Janus] (https://www.sonardyne.com/products/janus-ins-post-processing-software/) is commonly used. In this example logfiles are downloaded at the end of the mission via the web UI. 

??? son-info "Data for long duration AUVs"
    * SPRINT-Nav Mini will log data internally for 2 to 3 days. Less if raw DVL data is logged. 
    * For long duration missions the vehicle control system can periodically download logfiles from the unit via SFTP. 

### AUV lessons learnt
Sonardyne's applications engineering team have integrated SPRINT-Nav Mini into many different vehicles and have collated some best practice.  

??? son-info "Lessons learned"
    * Consider the orientation of DVL beams, if following a pipeline is there a better orientation to keep all DVL beams facing the seabed?
    * If HNAV indicates that SV is no longer valid, why not switch back to derived, or manual?



