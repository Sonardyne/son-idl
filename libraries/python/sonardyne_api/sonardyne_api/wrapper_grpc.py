#
# MIT License
#
# Copyright (c) 2025 Sonardyne International Limited
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import google.protobuf.any_pb2
import google.protobuf.empty_pb2
import google.protobuf

import sonardyne_api as son
from sonardyne_api import unpacking

import grpc
import grpc._channel
import queue


class WrapperGrpc:

    def __init__(self, ipaddress: str, port: int):
        self.ipaddress = ipaddress
        self.port = port
        self.channel = None
        self.configuration_service_stub = None
        self.comms_service_stub = None
        self.observation_service_stub = None
        self.command_service_stub = None
        self.is_open = False

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close()

    def open(self):
        self.channel = grpc.insecure_channel(self.ipaddress + ":" + str(self.port))
        self.configuration_service_stub = son.ConfigurationServiceStub(self.channel)
        self.comms_service_stub = son.CommsServiceStub(self.channel)
        self.observation_service_stub = son.ObservationServiceStub(self.channel)
        self.command_service_stub = son.CommandServiceStub(self.channel)
        self.is_open = True

    def close(self):
        self.channel.close()
        self.is_open = False

    def throw_if_not_open(self):
        if not self.is_open:
            raise RuntimeError("open() not called")

    def get_version(self) -> son.GetVersionResponse:
        self.throw_if_not_open()
        return self.configuration_service_stub.GetVersion(son.GetVersionRequest())

    def get_configurations_by_type_suffix(self, type_name_suffix: str) -> list[object]:
        self.throw_if_not_open()
        get_configuration_request = son.GetConfigurationRequest(matching_criteria=son.MatchingCriteria(match_type_name_suffix=type_name_suffix))
        self.configuration_service_stub.GetConfiguration(get_configuration_request)
        get_configuration_response = self.configuration_service_stub.GetConfiguration(get_configuration_request)
        typed_messages = []
        for any_message in get_configuration_response.configuration_messages:
            typed_messages.append(unpacking.unpack_message_from_any(any_message))
        return typed_messages

    def get_configurations(self, any_type: any) -> list[object]:
        self.throw_if_not_open()
        return self.get_configurations_by_type_suffix(unpacking.get_type_name(any_type))

    def get_configuration(self, any_type: any) -> any:
        self.throw_if_not_open()
        configurations = self.get_configurations(any_type)
        if len(configurations) == 0 or not isinstance(configurations[0], unpacking.get_type(any_type)):
            raise RuntimeError(f"Configuration '{unpacking.get_type_name(any_type)}' not found.")
        return configurations[0]

    def set_configuration(self, request: any) -> any:
        self.throw_if_not_open()
        set_configuration_request = son.SetConfigurationRequest()
        set_configuration_request.configuration.Pack(request)
        set_configuration_response = self.configuration_service_stub.SetConfiguration(set_configuration_request)
        unpacking.handle_result(set_configuration_response.result)
        return unpacking.unpack_message_from_any(set_configuration_response.configuration)

    def send_command(self, request: any):
        self.throw_if_not_open()
        send_command_request = son.SendCommandRequest()
        send_command_request.command.Pack(request)
        send_command_response = self.command_service_stub.SendCommand(send_command_request)
        unpacking.handle_result(send_command_response.result)

    def open_comms_stream(self, subscription_request: son.CommsSubscriptionRequest | None = None, timeout_seconds=None):
        self.throw_if_not_open()

        class CommsStream:
            def __init__(self, stub):
                self.send_queue = queue.SimpleQueue()
                self.stream_response_iterator = stub.CommsStream(iter(self.send_queue.get, None), timeout=timeout_seconds)

            def send(self, port_comms: son.DataPortComms | son.CommsSubscriptionRequest | list):
                comms_envelope = son.CommsEnvelope()
                if not isinstance(port_comms, list):
                    port_comms = [port_comms]
                for msg in port_comms:
                    target = google.protobuf.any_pb2.Any()
                    target.Pack(msg)
                    comms_envelope.comms_messages.append(target)
                self.send_queue.put(comms_envelope)

            def recv(self):
                response = next(self.stream_response_iterator)
                if not isinstance(response, son.CommsEnvelope):
                    return []
                return unpacking.unpack_list_from_any(response.comms_messages)

        stream = CommsStream(self.comms_service_stub)
        if subscription_request is not None:
            stream.send(subscription_request)
        return stream

    def open_observation_stream(self, subscription_request: son.ObservationSubscriptionRequest | None = None, timeout_seconds=None):
        self.throw_if_not_open()

        class ObservationStream:
            def __init__(self, stub):
                self.send_queue = queue.SimpleQueue()
                self.stream_response_iterator = stub.ObservationStream(iter(self.send_queue.get, None), timeout=timeout_seconds)

            def send(self, port_observation: son.GnssSourceObservation | son.XposSourceObservation | son.SusblSourceObservation | son.ObservationSubscriptionRequest | list):
                observation_envelope = son.ObservationEnvelope()
                if not isinstance(port_observation, list):
                    port_observation = [port_observation]
                for msg in port_observation:
                    target = google.protobuf.any_pb2.Any()
                    target.Pack(msg)
                    observation_envelope.observation_messages.append(target)
                self.send_queue.put(observation_envelope)

            def recv(self):
                response = next(self.stream_response_iterator)
                if not isinstance(response, son.ObservationEnvelope):
                    return []
                return unpacking.unpack_list_from_any(response.observation_messages)

        stream = ObservationStream(self.observation_service_stub)
        if subscription_request is not None:
            stream.send(subscription_request)
        return stream

    def open_configuration_stream(self, subscription_request: son.ConfigurationSubscriptionRequest | None = None, timeout_seconds=None):
        self.throw_if_not_open()

        class ConfigurationStream:
            def __init__(self, stub):
                self.send_queue = queue.SimpleQueue()
                self.stream_response_iterator = stub.ConfigurationStream(iter(self.send_queue.get, None), timeout=timeout_seconds)

            def send(self, subscription_request: son.ConfigurationSubscriptionRequest | list):
                configuration_envelope = son.ConfigurationEnvelope()
                if not isinstance(subscription_request, list):
                    subscription_request = [subscription_request]
                for msg in subscription_request:
                    target = google.protobuf.any_pb2.Any()
                    target.Pack(msg)
                    configuration_envelope.configuration_messages.append(target)
                self.send_queue.put(configuration_envelope)

            def recv(self):
                response = next(self.stream_response_iterator)
                if not isinstance(response, son.ConfigurationEnvelope):
                    return []
                return unpacking.unpack_list_from_any(response.configuration_messages)

        stream = ConfigurationStream(self.configuration_service_stub)
        if subscription_request is not None:
            stream.send(subscription_request)
        return stream
