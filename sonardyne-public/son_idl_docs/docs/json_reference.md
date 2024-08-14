# JSON Protocol Reference

This is a comprehensive reference on how to effectively utilise the JSON interface. You will find detailed explanations and practical examples that illustrate how to interact with and leverage the capabilities of the JSON interface.

#### Getting State
<details>
<summary>Get Version</summary>
<div style="background-color: #f0f0f0; padding: 10px; border-radius: 5px;">
<p>Sending this JSON object will request the current version information</strong></p>
<h4>Command</h4>
```json
{
 "@type": "type.googleapis.com/sonardyne.api.pub.common.VersionRequest"
}
```
<h4>Response</h4>
```json
{
 "@type": "type.googleapis.com/sonardyne.api.pub.common.VersionResponse",
 "major": 2,
 "minor": 0,
 "patch": 0
}
```
</div>
</details>

<details>
<summary>Get Configuration</summary>
<div style="background-color: #f0f0f0; padding: 10px; border-radius: 5px;">
<p>Sending this JSON object will request the current state of the instrument</strong></p>
<h4>Command</h4>
```json
{
  "@type": "type.googleapis.com/sonardyne.api.pub.configuration.ConfigurationRequest",
  "requestor": "Source of Request"
}
```
<h4>Response</h4>
```json
{
 "@type": "type.googleapis.com/sonardyne.api.pub.configuration.ConfigurationEnvelope",
 "timestamp": {
  "common_time_seconds": 0,
  "instrument_time_seconds": 1894856.99781867
 },
 "configuration": [
  {
   "@type": "type.googleapis.com/sonardyne.api.pub.configuration.AidingConfiguration",
   "enable_gnss": {
    "value": "ENABLED",
    "valid_values": [
     "ENABLED",
     "DISABLED"
    ]
   },
   "enable_xpos": {
    "value": "ENABLED",
    "valid_values": [
     "ENABLED",
     "DISABLED"
    ]
   },
   "enable_usbl": {
    "value": "DISABLED",
    "valid_values": [
     "ENABLED",
     "DISABLED"
    ]
   }
  },
  {
   "@type": "type.googleapis.com/sonardyne.api.pub.configuration.SoundVelocityConfiguration",
   "sound_velocity_type": {
    "value": "EXTERNAL",
    "valid_values": [
     "EXTERNAL",
     "INTERNAL_SALINITY",
     "INTERNAL_MANUAL"
    ]
   },
   "manual_salinity_value_parts_per_thousand": {
    "value": 32.1,
    "min": 0,
    "max": 40
   },
   "manual_velocity_value_metres_per_second": {
    "value": 1500,
    "min": 1400,
    "max": 1600
   }
  },
  {
   "@type": "type.googleapis.com/sonardyne.api.pub.configuration.DvlConfiguration",
   "update_rate": {
    "value": "FIXED_1HZ",
    "valid_values": [
     "MAX_RATE",
     "FIXED_1HZ",
     "FIXED_2HZ",
     "FIXED_5HZ",
     "FIXED_10HZ",
     "TRIGGER_RISING",
     "TRIGGER_FALLING"
    ]
   }
  }
 ]
}
```
</div>
</details>
#### Setting State
<details>
<summary>Set State (Introduction)</summary>
<div style="background-color: #f0f0f0; padding: 10px; border-radius: 5px;">
<h4>Command</h4>
 <p>The root JSON object contains two properties :<strong>'@type'</strong> and <strong>configuration</strong></p>
 <ul>
    <li><strong>@type</strong> is a string property with the value <strong>type.googleapis.com/sonardyne.api.pub.configuration.ConfigurationEnvelope</strong></li>
    <li><strong>configuration</strong> is an array which can contain one or more configuration types, each configuration has its own <strong>@type</strong> property</li>
        <li><strong>{ConfigurationType}</strong> shown in the command below is a placeholder and should be replaced with a specific configuration type. This allows the configuration array to hold various types of configuration objects, each identified by their own type</li>
 </ul>
```json
{
  "@type": "type.googleapis.com/sonardyne.api.pub.configuration.ConfigurationEnvelope",
  "configuration": [
    {
    "@type": "type.googleapis.com/sonardyne.api.pub.configuration.{ConfigurationType}"             
    }
  ]
}
```
<h4>Response</h4>
<p>The response message is also a <strong>type.googleapis.com/sonardyne.api.pub.configuration.ConfigurationEnvelope</strong> type sharing the same properties as the command structure.  The array of returned <strong>{ConfigurationType}</strong> will correspond to the configurations sent</strong>.</p>

```json
{
 "@type": "type.googleapis.com/sonardyne.api.pub.configuration.ConfigurationEnvelope",
 "timestamp": {
  "common_time_seconds": 0,
  "instrument_time_seconds": 1898031.49847554
 },
 "configuration": [
  {
   "@type": "type.googleapis.com/sonardyne.api.pub.configuration.{ConfigurationType}",
   "result": {
    "success": "SUCCESS",
    "message": ""
   },      
  }
 ]
}
```

<h4>Valid Values</h4>
All returned values where applicable within a configuration will contain an array with the valid range of values for that property, for example :

```json
"update_rate": {
    "value": "FIXED_1HZ",
    "valid_values": [
     "MAX_RATE",
     "FIXED_1HZ",
     "FIXED_2HZ",
     "FIXED_5HZ",
     "FIXED_10HZ",
     "TRIGGER_RISING",
     "TRIGGER_FALLING"
    ]
   }
```

<h4>Nested Result</h4>
Each nested <strong>{ConfigurationType}</strong> response will contain a <strong>'result'</strong> property.  This will indicate the success state of all command requests
<ul>
    <li><strong>success</strong> A string indicating command success [SUCCESS,FAILURE,INVALID,RESTRICTED]</li>
    <li><strong>message</strong> A string for any additional messages that may be pertinent if the command is not successful</li>        
 </ul>

 ```json
 "result": {
    "success": "SUCCESS",
    "message": ""
   }
 ```
</div>
</details>

<details>
<summary>Set Aiding Configuration</summary>
<div style="background-color: #f0f0f0; padding: 10px; border-radius: 5px;">
<h4>Command & Parameters</h4>
<ul>
<li><strong>enableGnss</strong> valid values [ENABLED,DISABLED]</li>
<li><strong>enableXpos</strong> valid values [ENABLED,DISABLED]</li>
<li><strong>enableUsbl</strong> valid values [ENABLED,DISABLED]</li>
 </ul>

```json
{
  "@type": "type.googleapis.com/sonardyne.api.pub.configuration.ConfigurationEnvelope",
  "configuration": [
    {
      "@type": "type.googleapis.com/sonardyne.api.pub.configuration.AidingConfiguration",
      "enableGnss": {
        "value": "ENABLED"
      },
      "enableXpos": {
        "value": "DISABLED"
      },
      "enableUsbl": {
        "value": "DISABLED"
      }
    }
  ]
}
```

<strong>Note</strong> : Not all properties need to be set, individual properties can be configured separately

<h4>Response</h4>
```json
{
 "@type": "type.googleapis.com/sonardyne.api.pub.configuration.ConfigurationEnvelope",
 "timestamp": {
  "common_time_seconds": 0,
  "instrument_time_seconds": 1919664.02866484
 },
 "configuration": [
  {
   "@type": "type.googleapis.com/sonardyne.api.pub.configuration.AidingConfiguration",
   "result": {
    "success": "SUCCESS",
    "message": ""
   },
   "enable_gnss": {
    "value": "ENABLED",
    "valid_values": [
     "ENABLED",
     "DISABLED"
    ]
   },
   "enable_xpos": {
    "value": "DISABLED",
    "valid_values": [
     "ENABLED",
     "DISABLED"
    ]
   },
   "enable_usbl": {
    "value": "DISABLED",
    "valid_values": [
     "ENABLED",
     "DISABLED"
    ]
   }
  }
 ]
}
```
</div>
</details>

<details>
<summary>Set DVL Configuration</summary>
<div style="background-color: #f0f0f0; padding: 10px; border-radius: 5px;">
<h4>Command & Parameters</h4>
<ul>
<li> <strong>updateRate</strong> valid values <strong>[MAX_RATE, FIXED_1HZ, FIXED_2HZ, FIXED_5HZ, FIXED_10HZ, TRIGGER_RISING, TRIGGER_FALLING]</strong></li>
</ul>
```json
{
  "@type": "type.googleapis.com/sonardyne.api.pub.configuration.ConfigurationEnvelope",
  "configuration": [
    {
      "@type": "type.googleapis.com/sonardyne.api.pub.configuration.DvlConfiguration", 
      "updateRate": {
        "value": "FIXED_1HZ"
      }
    }
  ]
}
```
<strong>Note</strong> : Not all properties need to be set, individual properties can be configured separately

<h4>Response</h4>
```json
{
 "@type": "type.googleapis.com/sonardyne.api.pub.configuration.ConfigurationEnvelope",
 "timestamp": {
  "common_time_seconds": 0,
  "instrument_time_seconds": 1916074.48673176
 },
 "configuration": [
  {
   "@type": "type.googleapis.com/sonardyne.api.pub.configuration.DvlConfiguration",   
   "result": {
    "success": "SUCCESS",
    "message": ""
   },
   "update_rate": {
    "value": "FIXED_1HZ",
    "valid_values": [
     "MAX_RATE",
     "FIXED_1HZ",
     "FIXED_2HZ",
     "FIXED_5HZ",
     "FIXED_10HZ",
     "TRIGGER_RISING",
     "TRIGGER_FALLING"
    ]
   }
  }
 ]
```
</div>
</details>

<details>
<summary>Set Sound Velocity Configuration</summary>
<div style="background-color: #f0f0f0; padding: 10px; border-radius: 5px;">
<h4>Command & Parameters</h4>
<ul>
<li> <strong>soundVelocityType</strong> valid values are <strong>[EXTERNAL, INTERNAL_SALINITY, INTERNAL_MANUAL]</strong></li>
<li> <strong>manualSalinityValuePartsPerThousand</strong> valid values are <strong>0 to 40</strong></li>
<li> <strong>manualVelocityValueMetresPerSecond</strong> valid values are <strong>1400 to 1600</strong></li>
 </ul>
```json
{
  "@type": "type.googleapis.com/sonardyne.api.pub.configuration.ConfigurationEnvelope",
  "configuration": [
    {
      "@type": "type.googleapis.com/sonardyne.api.pub.configuration.SoundVelocityConfiguration",
      "soundVelocityType": {
        "value": "EXTERNAL"
      },
      "manualSalinityValuePartsPerThousand": {
        "value": 40.0
      },
      "manualVelocityValueMetresPerSecond": {
        "value": 1500.0
      }
    }
  ]
}
```
<strong>Note</strong> : Not all properties need to be set, individual properties can be configured separately

<h4>Response</h4>
```json
{
 "@type": "type.googleapis.com/sonardyne.api.pub.configuration.ConfigurationEnvelope",
 "timestamp": {
  "common_time_seconds": 0,
  "instrument_time_seconds": 1918491.19956508
 },
 "configuration": [
  {
   "@type": "type.googleapis.com/sonardyne.api.pub.configuration.SoundVelocityConfiguration",
   "result": {
    "success": "SUCCESS",
    "message": ""
   },
   "sound_velocity_type": {
    "value": "EXTERNAL",
    "valid_values": [
     "EXTERNAL",
     "INTERNAL_SALINITY",
     "INTERNAL_MANUAL"
    ]
   },
   "manual_salinity_value_parts_per_thousand": {
    "value": 40,
    "min": 0,
    "max": 40
   },
   "manual_velocity_value_metres_per_second": {
    "value": 1500,
    "min": 1400,
    "max": 1600
   }
  }
 ]
}
```
</div>
</details>

<details>
<summary>Set Multiple Configurations Simultaneously</summary>
<div style="background-color: #f0f0f0; padding: 10px; border-radius: 5px;">
<h4>Command</h4>
The following command show how to embed multiple configuration objects in the <strong>configuration</strong> array
```json
{
  "@type": "type.googleapis.com/sonardyne.api.pub.configuration.ConfigurationEnvelope",
  "configuration": [
    {
      "@type": "type.googleapis.com/sonardyne.api.pub.configuration.AidingConfiguration",       
      "enableGnss": {
        "value": "ENABLED"
      },
      "enableXpos": {
        "value": "DISABLED"
      },
      "enableUsbl": {
        "value": "DISABLED"
      }
    },
    {
      "@type": "type.googleapis.com/sonardyne.api.pub.configuration.SoundVelocityConfiguration",
      "soundVelocityType": {
        "value": "EXTERNAL"
      },
      "manualSalinityValuePartsPerThousand": {
        "value": 40.0
      },
      "manualVelocityValueMetresPerSecond": {
        "value": 1500.0
      }
    },
    {
      "@type": "type.googleapis.com/sonardyne.api.pub.configuration.DvlConfiguration",
      "updateRate": {
        "value": "FIXED_1HZ"
      }
    }
  ]
}
```

<h4>Response</h4>
The response show how multiple responses being delivered, each one with a <strong>result</strong> object indicating success state
```json
 "@type": "type.googleapis.com/sonardyne.api.pub.configuration.ConfigurationEnvelope",
 "timestamp": {
  "common_time_seconds": 0,
  "instrument_time_seconds": 1922242.57665971
 },
 "configuration": [
  {
   "@type": "type.googleapis.com/sonardyne.api.pub.configuration.AidingConfiguration",
   "result": {
    "success": "SUCCESS",
    "message": ""
   },
   "enable_gnss": {
    "value": "ENABLED",
    "valid_values": [
     "ENABLED",
     "DISABLED"
    ]
   },
   "enable_xpos": {
    "value": "DISABLED",
    "valid_values": [
     "ENABLED",
     "DISABLED"
    ]
   },
   "enable_usbl": {
    "value": "DISABLED",
    "valid_values": [
     "ENABLED",
     "DISABLED"
    ]
   }
  },
  {
   "@type": "type.googleapis.com/sonardyne.api.pub.configuration.SoundVelocityConfiguration",
   "result": {
    "success": "SUCCESS",
    "message": ""
   },
   "sound_velocity_type": {
    "value": "EXTERNAL",
    "valid_values": [
     "EXTERNAL",
     "INTERNAL_SALINITY",
     "INTERNAL_MANUAL"
    ]
   },
   "manual_salinity_value_parts_per_thousand": {
    "value": 40,
    "min": 0,
    "max": 40
   },
   "manual_velocity_value_metres_per_second": {
    "value": 1500,
    "min": 1400,
    "max": 1600
   }
  },
  {
   "@type": "type.googleapis.com/sonardyne.api.pub.configuration.DvlConfiguration",
   "result": {
    "success": "SUCCESS",
    "message": ""
   },
   "update_rate": {
    "value": "FIXED_1HZ",
    "valid_values": [
     "MAX_RATE",
     "FIXED_1HZ",
     "FIXED_2HZ",
     "FIXED_5HZ",
     "FIXED_10HZ",
     "TRIGGER_RISING",
     "TRIGGER_FALLING"
    ]
   }
  }
 ]
}
```
</div>
</details>