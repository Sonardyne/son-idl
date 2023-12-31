# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: configuration.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import result_pb2 as result__pb2
import timestamp_pb2 as timestamp__pb2
import uid_pb2 as uid__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x13\x63onfiguration.proto\x12\rsonardyne.api\x1a\x0cresult.proto\x1a\x0ftimestamp.proto\x1a\tuid.proto\"\xa0\x01\n\x15\x43onfigurationEnvelope\x12+\n\ttimestamp\x18\x01 \x01(\x0b\x32\x18.sonardyne.api.Timestamp\x12%\n\x06result\x18\x02 \x01(\x0b\x32\x15.sonardyne.api.Result\x12\x33\n\rconfiguration\x18\x03 \x01(\x0b\x32\x1c.sonardyne.api.Configuration\"V\n\x14\x43onfigurationRequest\x12+\n\ttimestamp\x18\x01 \x01(\x0b\x32\x18.sonardyne.api.Timestamp\x12\x11\n\trequestor\x18\x02 \x01(\t\"\xbe\x02\n\rConfiguration\x12?\n\x14reset_configurations\x18\x64 \x03(\x0b\x32!.sonardyne.api.ResetConfiguration\x12\x41\n\x15\x61iding_configurations\x18\x65 \x03(\x0b\x32\".sonardyne.api.AidingConfiguration\x12P\n\x1dsound_velocity_configurations\x18\x66 \x03(\x0b\x32).sonardyne.api.SoundVelocityConfiguration\x12W\n\x1f\x64oppler_velocity_configurations\x18g \x03(\x0b\x32..sonardyne.api.DopplerVelocityLogConfiguration\"\xe7\x01\n\x12ResetConfiguration\x12\x1e\n\x02id\x18\x01 \x01(\x0b\x32\x12.sonardyne.api.Uid\x12%\n\x06result\x18\x02 \x01(\x0b\x32\x15.sonardyne.api.Result\x12@\n\nreset_type\x18\x03 \x01(\x0e\x32,.sonardyne.api.ResetConfiguration.RESET_TYPE\"H\n\nRESET_TYPE\x12\x1a\n\x16RESET_TYPE_UNSPECIFIED\x10\x00\x12\x0e\n\nSOFT_RESET\x10\x01\x12\x0e\n\nHARD_RESET\x10\x02\"\xf7\x02\n\x13\x41idingConfiguration\x12\x1e\n\x02id\x18\x01 \x01(\x0b\x32\x12.sonardyne.api.Uid\x12%\n\x06result\x18\x02 \x01(\x0b\x32\x15.sonardyne.api.Result\x12\x44\n\x0b\x65nable_gnss\x18\x03 \x01(\x0e\x32/.sonardyne.api.AidingConfiguration.AIDING_STATE\x12\x44\n\x0b\x65nable_xpos\x18\x04 \x01(\x0e\x32/.sonardyne.api.AidingConfiguration.AIDING_STATE\x12\x44\n\x0b\x65nable_usbl\x18\x05 \x01(\x0e\x32/.sonardyne.api.AidingConfiguration.AIDING_STATE\"G\n\x0c\x41IDING_STATE\x12\x1c\n\x18\x41IDING_STATE_UNSPECIFIED\x10\x00\x12\x0b\n\x07\x45NABLED\x10\x01\x12\x0c\n\x08\x44ISABLED\x10\x02\"\xe4\x02\n\x1aSoundVelocityConfiguration\x12\x1e\n\x02id\x18\x01 \x01(\x0b\x32\x12.sonardyne.api.Uid\x12%\n\x06result\x18\x02 \x01(\x0b\x32\x15.sonardyne.api.Result\x12U\n\x13sound_velocity_type\x18\x03 \x01(\x0e\x32\x38.sonardyne.api.SoundVelocityConfiguration.SOUND_VELOCITY\x12\x1d\n\x15manual_salinity_value\x18\x04 \x01(\x01\x12\x1d\n\x15manual_velocity_value\x18\x05 \x01(\x01\"j\n\x0eSOUND_VELOCITY\x12\x1e\n\x1aSOUND_VELOCITY_UNSPECIFIED\x10\x00\x12\x0c\n\x08\x45XTERNAL\x10\x01\x12\x15\n\x11INTERNAL_SALINITY\x10\x02\x12\x13\n\x0fINTERNAL_MANUAL\x10\x03\"\xda\x02\n\x1f\x44opplerVelocityLogConfiguration\x12\x1e\n\x02id\x18\x01 \x01(\x0b\x32\x12.sonardyne.api.Uid\x12%\n\x06result\x18\x02 \x01(\x0b\x32\x15.sonardyne.api.Result\x12O\n\x0bupdate_rate\x18\x03 \x01(\x0e\x32:.sonardyne.api.DopplerVelocityLogConfiguration.UPDATE_RATE\"\x9e\x01\n\x0bUPDATE_RATE\x12\x1b\n\x17UPDATE_RATE_UNSPECIFIED\x10\x00\x12\x12\n\x0eTRIGGER_RISING\x10\x01\x12\x13\n\x0fTRIGGER_FALLING\x10\x02\x12\x0c\n\x08MAX_RATE\x10\x03\x12\r\n\tFIXED_1HZ\x10\x04\x12\r\n\tFIXED_2HZ\x10\x05\x12\r\n\tFIXED_5HZ\x10\x06\x12\x0e\n\nFIXED_10HZ\x10\x07\x42\x0f\xaa\x02\x0cSonardyneApib\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'configuration_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\252\002\014SonardyneApi'
  _CONFIGURATIONENVELOPE._serialized_start=81
  _CONFIGURATIONENVELOPE._serialized_end=241
  _CONFIGURATIONREQUEST._serialized_start=243
  _CONFIGURATIONREQUEST._serialized_end=329
  _CONFIGURATION._serialized_start=332
  _CONFIGURATION._serialized_end=650
  _RESETCONFIGURATION._serialized_start=653
  _RESETCONFIGURATION._serialized_end=884
  _RESETCONFIGURATION_RESET_TYPE._serialized_start=812
  _RESETCONFIGURATION_RESET_TYPE._serialized_end=884
  _AIDINGCONFIGURATION._serialized_start=887
  _AIDINGCONFIGURATION._serialized_end=1262
  _AIDINGCONFIGURATION_AIDING_STATE._serialized_start=1191
  _AIDINGCONFIGURATION_AIDING_STATE._serialized_end=1262
  _SOUNDVELOCITYCONFIGURATION._serialized_start=1265
  _SOUNDVELOCITYCONFIGURATION._serialized_end=1621
  _SOUNDVELOCITYCONFIGURATION_SOUND_VELOCITY._serialized_start=1515
  _SOUNDVELOCITYCONFIGURATION_SOUND_VELOCITY._serialized_end=1621
  _DOPPLERVELOCITYLOGCONFIGURATION._serialized_start=1624
  _DOPPLERVELOCITYLOGCONFIGURATION._serialized_end=1970
  _DOPPLERVELOCITYLOGCONFIGURATION_UPDATE_RATE._serialized_start=1812
  _DOPPLERVELOCITYLOGCONFIGURATION_UPDATE_RATE._serialized_end=1970
# @@protoc_insertion_point(module_scope)
