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
from sonardyne_api import communication
from sonardyne_api.simple_binary_protocol import simple_binary_protocol as sbp

import time
import threading
from cobs import cobs


class WrapperFramed:
    """A wrapper for the framed protobuf interface which encodes and decodes configurations."""

    count = 1
    def __init__(self, communication_interface: communication.CommunicationInterface):
        """The port should match the TCP server configured as the External Control port."""
        self.request_timeout_seconds = 7
        self.awaiting_responses = {}
        self.envelopes = {}
        self.listener_thread_running = False
        self.listener_thread = None
        self.is_open = False
        self.communication_interface = communication_interface

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close()

    def open(self):
        self.communication_interface.open()
        WrapperFramed.count = 1
        self.request_timeout_seconds = 7
        self.awaiting_responses = {}
        self.envelopes = {}
        self.listener_thread_running = True
        self.listener_thread = threading.Thread(target=self._listener_thread)
        self.listener_thread.start()
        self.is_open = True

    def close(self):
        self.listener_thread_running = False
        self.listener_thread.join()
        self.is_open = False
        self.communication_interface.close()

    def throw_if_not_open(self):
        if not self.is_open:
            raise RuntimeError("open() not called")

    def get_version(self) -> son.GetVersionResponse:
        self.throw_if_not_open()
        request_envelope = son.RequestEnvelope()
        any_get_version_request = google.protobuf.any_pb2.Any()
        get_version_request = son.GetVersionRequest()
        any_get_version_request.Pack(get_version_request)
        request_envelope.requests.append(any_get_version_request)
        response = self.send_request_await_response(request_envelope)
        if len(response.responses) == 0:
            raise Exception("No response found.")
        get_version_response = son.GetVersionResponse()
        if response.responses[0].Unpack(get_version_response):
            return get_version_response
        raise Exception("Failed to unpack response.")

    def get_configurations_by_type_suffix(self, type_name_suffix: str) -> list[object]:
        self.throw_if_not_open()
        request_envelope = son.RequestEnvelope()
        any_get_configuration_request = google.protobuf.any_pb2.Any()
        get_configuration_request = son.GetConfigurationRequest(matching_criteria=son.MatchingCriteria(match_type_name_suffix=type_name_suffix))
        any_get_configuration_request.Pack(get_configuration_request)
        request_envelope.requests.append(any_get_configuration_request)
        response = self.send_request_await_response(request_envelope)
        if len(response.responses) == 0:
            raise Exception("No response found.")
        get_configuration_response = son.GetConfigurationResponse()
        if response.responses[0].Unpack(get_configuration_response):
            typed_messages = []
            for any_message in get_configuration_response.configuration_messages:
                typed_messages.append(unpacking.unpack_message_from_any(any_message))
            return typed_messages
        raise Exception("Failed to unpack response.")

    def get_configurations(self, any_type: any) -> list[object]:
        self.throw_if_not_open()
        return self.get_configurations_by_type_suffix(unpacking.get_type_name(any_type))

    def get_configuration(self, any_type: any) -> any:
        self.throw_if_not_open()
        configurations = self.get_configurations(any_type)
        for configuration in configurations:
            if isinstance(configuration, unpacking.get_type(any_type)):
                return configuration
        raise RuntimeError(f"Configuration '{unpacking.get_type_name(any_type)}' not found.")

    def set_configuration(self, request: any) -> any:
        self.throw_if_not_open()
        request_envelope = son.RequestEnvelope()
        any_set_configuration_request = google.protobuf.any_pb2.Any()
        set_configuration_request = son.SetConfigurationRequest()
        set_configuration_request.configuration.Pack(request)
        any_set_configuration_request.Pack(set_configuration_request)
        request_envelope.requests.append(any_set_configuration_request)
        response = self.send_request_await_response(request_envelope)
        if len(response.responses) == 0:
            raise Exception("No response found.")
        set_configuration_response = son.SetConfigurationResponse()
        if response.responses[0].Unpack(set_configuration_response):
            unpacking.handle_result(set_configuration_response.result)
            return unpacking.unpack_message_from_any(set_configuration_response.configuration)
        raise Exception("Failed to unpack response.")

    def send_command(self, request: any):
        self.throw_if_not_open()
        request_envelope = son.RequestEnvelope()
        any_set_configuration_request = google.protobuf.any_pb2.Any()
        send_command_request = son.SendCommandRequest()
        send_command_request.command.Pack(request)
        any_set_configuration_request.Pack(send_command_request)
        request_envelope.requests.append(any_set_configuration_request)
        response = self.send_request_await_response(request_envelope)
        if len(response.responses) == 0:
            raise Exception("No response found.")
        send_command_response = son.SendCommandResponse()
        if response.responses[0].Unpack(send_command_response):
            unpacking.handle_result(send_command_response.result)
            return
        raise Exception("Failed to unpack response.")

    def open_configuration_stream(self, subscription_request: son.ConfigurationSubscriptionRequest | None = None):
        self.throw_if_not_open()

        class ConfigurationStream:
            def __init__(self, parent):
                self.parent = parent

            def send(self, message):
                any_message = google.protobuf.any_pb2.Any()
                any_message.Pack(message)
                envelope = son.ConfigurationEnvelope(configuration_messages=[any_message])
                any_message = google.protobuf.any_pb2.Any()
                any_message.Pack(envelope)
                request_envelope = son.RequestEnvelope(requests=[any_message])

                # Wait for matching response if sending request
                if message.DESCRIPTOR.name.endswith("SubscriptionRequest"):
                    self.parent.send_request_await_response(request_envelope)
                else:
                    self.parent.send_request(request_envelope)

            def recv(self):
                while son.ConfigurationEnvelope not in self.parent.envelopes or len(self.parent.envelopes[son.ConfigurationEnvelope]) == 0:
                    time.sleep(0.01)
                latest_message = self.parent.envelopes[son.ConfigurationEnvelope][0]
                del self.parent.envelopes[son.ConfigurationEnvelope][0]
                typed_messages = []
                for any_message in latest_message.configuration_messages:
                    typed_messages.append(unpacking.unpack_message_from_any(any_message))
                return typed_messages

        stream = ConfigurationStream(self)
        if subscription_request is not None:
            stream.send(subscription_request)
        return stream

    def open_comms_stream(self, subscription_request: son.CommsSubscriptionRequest | None = None):
        self.throw_if_not_open()

        class CommsStream:
            def __init__(self, parent):
                self.parent = parent

            def send(self, message):
                any_message = google.protobuf.any_pb2.Any()
                any_message.Pack(message)
                envelope = son.CommsEnvelope(comms_messages=[any_message])
                any_message = google.protobuf.any_pb2.Any()
                any_message.Pack(envelope)
                request_envelope = son.RequestEnvelope(requests=[any_message])

                # Wait for matching response if sending request
                if message.DESCRIPTOR.name.endswith("SubscriptionRequest"):
                    self.parent.send_request_await_response(request_envelope)
                else:
                    self.parent.send_request(request_envelope)

            def recv(self):
                while son.CommsEnvelope not in self.parent.envelopes or len(self.parent.envelopes[son.CommsEnvelope]) == 0:
                    time.sleep(0.01)
                latest_message = self.parent.envelopes[son.CommsEnvelope][0]
                del self.parent.envelopes[son.CommsEnvelope][0]
                typed_messages = []
                for any_message in latest_message.comms_messages:
                    typed_messages.append(unpacking.unpack_message_from_any(any_message))
                return typed_messages

        stream = CommsStream(self)
        if subscription_request is not None:
            stream.send(subscription_request)
        return stream

    def open_observation_stream(self, subscription_request: son.ObservationSubscriptionRequest | None = None):
        self.throw_if_not_open()

        class ObservationStream:
            def __init__(self, parent):
                self.parent = parent

            def send(self, message):
                any_message = google.protobuf.any_pb2.Any()
                any_message.Pack(message)
                envelope = son.ObservationEnvelope(observation_messages=[any_message])
                any_message = google.protobuf.any_pb2.Any()
                any_message.Pack(envelope)
                request_envelope = son.RequestEnvelope(requests=[any_message])

                # Wait for matching response if sending request
                if message.DESCRIPTOR.name.endswith("SubscriptionRequest"):
                    self.parent.send_request_await_response(request_envelope)
                else:
                    self.parent.send_request(request_envelope)

            def recv(self):
                while son.ObservationEnvelope not in self.parent.envelopes or len(self.parent.envelopes[son.ObservationEnvelope]) == 0:
                    time.sleep(0.01)
                latest_message = self.parent.envelopes[son.ObservationEnvelope][0]
                del self.parent.envelopes[son.ObservationEnvelope][0]
                typed_messages = []
                for any_message in latest_message.observation_messages:
                    typed_messages.append(unpacking.unpack_message_from_any(any_message))
                return typed_messages

        stream = ObservationStream(self)
        if subscription_request is not None:
            stream.send(subscription_request)
        return stream

    def open_status_stream(self, subscription_request: son.StatusSubscriptionRequest | None = None):
        self.throw_if_not_open()

        class StatusStream:
            def __init__(self, parent):
                self.parent = parent

            def send(self, message):
                any_message = google.protobuf.any_pb2.Any()
                any_message.Pack(message)
                envelope = son.StatusEnvelope(status_messages=[any_message])
                any_message = google.protobuf.any_pb2.Any()
                any_message.Pack(envelope)
                request_envelope = son.RequestEnvelope(requests=[any_message])

                # Wait for matching response if sending request
                if message.DESCRIPTOR.name.endswith("SubscriptionRequest"):
                    self.parent.send_request_await_response(request_envelope)
                else:
                    self.parent.send_request(request_envelope)

            def recv(self):
                while son.StatusEnvelope not in self.parent.envelopes or len(self.parent.envelopes[son.StatusEnvelope]) == 0:
                    time.sleep(0.01)
                latest_message = self.parent.envelopes[son.StatusEnvelope][0]
                del self.parent.envelopes[son.StatusEnvelope][0]
                typed_messages = []
                for any_message in latest_message.status_messages:
                    typed_messages.append(unpacking.unpack_message_from_any(any_message))
                return typed_messages

        stream = StatusStream(self)
        if subscription_request is not None:
            stream.send(subscription_request)
        return stream

    def send_request_await_response(self, request_envelope: son.RequestEnvelope) -> list[object]:
        request_count = WrapperFramed.count
        self.awaiting_responses[request_count] = None
        WrapperFramed.count = (WrapperFramed.count + 1) % 256
        self.send_request(request_envelope, request_count)
        return self.listen_for_response(request_count)

    def send_request(self, envelope: son.RequestEnvelope, request_count=0):
        # Make request
        message = google.protobuf.any_pb2.Any()
        message.Pack(envelope)
        # Serialise message and wrap with Simple Binary Protocol & COBS
        raw_bytes = sbp.encode(message.SerializeToString(), sbp.MessageType.GoogleProtobufAny, request_count)
        # COBS handles any length, so encode the whole message as a single frame
        self.communication_interface.send(cobs.encode(raw_bytes) + b'\x00')

    def _listener_thread(self):
        tcp_buffer = bytes([])
        buffer_length = 65535
        while self.listener_thread_running:
            try:
                tcp_data = self.communication_interface.receive(buffer_length, 0.05)

                tcp_buffer += tcp_data
                if len(tcp_data) == buffer_length:
                    continue
                if not tcp_data:
                    raise Exception("Disconnected.")

                # Unwrap COBS
                cobs_packets = tcp_buffer.split(b'\x00')
                tcp_buffer = cobs_packets[-1]

                if not cobs_packets:
                    continue
                decoded_packets = []
                for cobs_packet in cobs_packets[:-1]:
                    if len(cobs_packet) == 0:
                        continue
                    try:
                        decoded_packets.append(cobs.decode(cobs_packet))
                    except Exception as e:
                        print(f'Encountered invalid COBS packet: {e}')

                sbp_messages = []
                for decoded_packet in decoded_packets:
                    # Unwrap Simple Binary Protocol
                    if len(decoded_packet) <= 12:
                        continue
                    if decoded_packet[0] != sbp.sync_byte_1:
                        continue
                    if decoded_packet[1] != sbp.sync_byte_2:
                        continue
                    try:
                        sbp_message = sbp.decode(decoded_packet)
                        if sbp_message:
                            sbp_messages.append(sbp_message)
                    except Exception as e:
                        print(f"Failed to decode response: {e}")

                for sbp_message in sbp_messages:
                    # Parse serialised message
                    message = google.protobuf.any_pb2.Any()
                    if not message.ParseFromString(sbp_message.payload):
                        print("Failed to parse message from string.")
                        continue
                    # If count matches one of our sent messages, try as response...
                    if sbp_message.count in self.awaiting_responses:
                        response_envelope = son.ResponseEnvelope()
                        if message.Unpack(response_envelope):
                            self.awaiting_responses[sbp_message.count] = response_envelope
                        pass
                    config_envelope = son.ConfigurationEnvelope()
                    if message.Unpack(config_envelope):
                        if son.ConfigurationEnvelope not in self.envelopes:
                            self.envelopes[son.ConfigurationEnvelope] = []
                        self.envelopes[son.ConfigurationEnvelope].append(config_envelope)
                        if len(self.envelopes[son.ConfigurationEnvelope]) > 100:
                            self.envelopes[son.ConfigurationEnvelope] = self.envelopes[son.ConfigurationEnvelope][-100:]
                    config_envelope = son.ObservationEnvelope()
                    if message.Unpack(config_envelope):
                        if son.ObservationEnvelope not in self.envelopes:
                            self.envelopes[son.ObservationEnvelope] = []
                        self.envelopes[son.ObservationEnvelope].append(config_envelope)
                        if len(self.envelopes[son.ObservationEnvelope]) > 100:
                            self.envelopes[son.ObservationEnvelope] = self.envelopes[son.ObservationEnvelope][-100:]
                    config_envelope = son.StatusEnvelope()
                    if message.Unpack(config_envelope):
                        if son.StatusEnvelope not in self.envelopes:
                            self.envelopes[son.StatusEnvelope] = []
                        self.envelopes[son.StatusEnvelope].append(config_envelope)
                        if len(self.envelopes[son.StatusEnvelope]) > 100:
                            self.envelopes[son.StatusEnvelope] = self.envelopes[son.StatusEnvelope][-100:]
                    config_envelope = son.CommsEnvelope()
                    if message.Unpack(config_envelope):
                        if son.CommsEnvelope not in self.envelopes:
                            self.envelopes[son.CommsEnvelope] = []
                        self.envelopes[son.CommsEnvelope].append(config_envelope)
                        if len(self.envelopes[son.CommsEnvelope]) > 100:
                            self.envelopes[son.CommsEnvelope] = self.envelopes[son.CommsEnvelope][-100:]
            except TimeoutError:
                pass

    def listen_for_response(self, request_count):
        start_time = time.time()
        while time.time() < start_time + self.request_timeout_seconds:
            if request_count in self.awaiting_responses and self.awaiting_responses[request_count] is not None:
                response = self.awaiting_responses[request_count]
                del self.awaiting_responses[request_count]
                return response
            time.sleep(0.01)
        raise TimeoutError("Request timed out.")
