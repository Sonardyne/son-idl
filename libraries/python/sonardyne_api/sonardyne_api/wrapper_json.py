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
from google.protobuf.json_format import MessageToJson, Parse, ParseError
import google.protobuf

import sonardyne_api as son
from sonardyne_api import unpacking
from sonardyne_api import communication

import time
import threading
import os

# Running with the environment variable SONARDYNE_API_OUTPUT_RAW_JSON
# set allows example code to be used to output raw JSON messages when generating documentation.
output_raw_json = False
if os.environ.get('SONARDYNE_API_OUTPUT_RAW_JSON'):
    print("warning env var set: SONARDYNE_API_OUTPUT_RAW_JSON")
    output_raw_json = True
if output_raw_json:
    import json


def _get_json_messages(data_buffer):
    parsed_json_messages = []
    start_index = -1
    message_end_index = -1
    buffer_index = 0
    depth = 0
    while buffer_index < len(data_buffer):
        if data_buffer[buffer_index] == '{':
            if depth == 0:
                start_index = buffer_index
            depth += 1
        elif data_buffer[buffer_index] == '}':
            depth -= 1
            if depth == 0:
                end_index = buffer_index + 1
                if start_index != -1 and start_index < end_index:
                    message = data_buffer[start_index:end_index]
                    message_end_index = end_index
                    start_index = -1
                    parsed_json_messages.append(message)
            elif depth < 0:
                # reset counters
                start_index = -1
                depth = 0
        buffer_index += 1
    return parsed_json_messages, message_end_index


class WrapperJson:
    """A wrapper for the framed protobuf interface which encodes and decodes configurations."""

    count = 1
    def __init__(self, communication_interface: communication.CommunicationInterface):
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
        if output_raw_json:
            self.is_open = True
            return
        self.communication_interface.open()
        WrapperJson.count = 1
        self.request_timeout_seconds = 7
        self.awaiting_responses = {}
        self.envelopes = {}
        self.listener_thread_running = True
        self.listener_thread = threading.Thread(target=self._listener_thread)
        self.listener_thread.start()
        self.is_open = True

    def close(self):
        if output_raw_json:
            self.is_open = False
            return
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
        if output_raw_json:
            return son.GetVersionResponse()
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
        if output_raw_json:
            return []
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
        configurations = self.get_configurations_by_type_suffix(unpacking.get_type_name(any_type))
        if output_raw_json:
            return []
        return configurations

    def get_configuration(self, any_type: any) -> any:
        self.throw_if_not_open()
        configurations = self.get_configurations(any_type)
        if output_raw_json:
            return []
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
        if output_raw_json:
            return None
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
        if output_raw_json:
            return None
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

                if output_raw_json:
                    raise KeyboardInterrupt()

            def recv(self, timeout_seconds=None):
                if output_raw_json:
                    exit(0)
                start_time = time.time()
                while son.ConfigurationEnvelope not in self.parent.envelopes or len(self.parent.envelopes[son.ConfigurationEnvelope]) == 0:
                    time.sleep(0.01)
                    if timeout_seconds is not None and time.time() > start_time + timeout_seconds:
                        raise TimeoutError
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

                if output_raw_json:
                    raise KeyboardInterrupt()

            def recv(self):
                if output_raw_json:
                    exit(0)
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

                if output_raw_json:
                    raise KeyboardInterrupt()

            def recv(self, timeout_seconds=None):
                if output_raw_json:
                    exit(0)
                start_time = time.time()
                while son.ObservationEnvelope not in self.parent.envelopes or len(self.parent.envelopes[son.ObservationEnvelope]) == 0:
                    time.sleep(0.01)
                    if timeout_seconds is not None and time.time() > start_time + timeout_seconds:
                        raise TimeoutError
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

                if output_raw_json:
                    raise KeyboardInterrupt()

            def recv(self, timeout_seconds=None):
                if output_raw_json:
                    exit(0)
                start_time = time.time()
                while son.StatusEnvelope not in self.parent.envelopes or len(self.parent.envelopes[son.StatusEnvelope]) == 0:
                    time.sleep(0.01)
                    if timeout_seconds is not None and time.time() > start_time + timeout_seconds:
                        raise TimeoutError
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
        request_count = WrapperJson.count
        self.awaiting_responses[request_count] = None
        WrapperJson.count = (WrapperJson.count + 1) % 256
        self.send_request(request_envelope, request_count)
        return self.listen_for_response(request_count)

    def send_request(self, envelope: son.RequestEnvelope, request_count=0):
        # Make request
        envelope.MergeFrom(son.RequestEnvelope(uid=request_count))
        message = google.protobuf.any_pb2.Any()
        message.Pack(envelope)
        if output_raw_json:
            print(f"<dev_mode>{json.dumps(json.loads(MessageToJson(message)), indent=4)}</dev_mode>")
            return
        self.communication_interface.send(MessageToJson(message).encode())

    def _listener_thread(self):
        data_buffer = ""
        buffer_length = 65535
        while self.listener_thread_running:
            try:
                data_buffer += self.communication_interface.receive(buffer_length, 0.05).decode()
                parsed_json_messages, message_end_index = _get_json_messages(data_buffer)
                if message_end_index != -1:
                    data_buffer = data_buffer[message_end_index:]
                for parsed_json_message in parsed_json_messages:
                    try:
                        message = Parse(parsed_json_message, google.protobuf.any_pb2.Any(), ignore_unknown_fields=True)
                    except ParseError as e:
                        print(f"Protobuf JSON Parse failed due to: {e}")
                        continue
                    except json.JSONDecodeError as e:
                        print(f"JSON Syntax Error: {e}")
                        continue
                    except TypeError as e:
                        print(f"API Usage Error: {e}")
                        continue

                    response_envelope = son.ResponseEnvelope()
                    if message.Unpack(response_envelope):
                        if response_envelope.uid in self.awaiting_responses:
                            self.awaiting_responses[response_envelope.uid] = response_envelope
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
        if output_raw_json:
            return []
        start_time = time.time()
        while time.time() < start_time + self.request_timeout_seconds:
            if request_count in self.awaiting_responses and self.awaiting_responses[request_count] is not None:
                response = self.awaiting_responses[request_count]
                del self.awaiting_responses[request_count]
                return response
            time.sleep(0.01)
        raise TimeoutError("Request timed out.")
