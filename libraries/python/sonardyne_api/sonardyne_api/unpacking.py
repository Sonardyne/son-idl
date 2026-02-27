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


class ResultException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class ResultUnspecifiedException(ResultException):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class ResultFailureException(ResultException):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class ResultInvalidException(ResultException):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class ResultRestrictedException(ResultException):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def unpack_message_from_any(message_any: google.protobuf.any_pb2.Any):
    """Unpack an Any message"""
    if not isinstance(message_any, google.protobuf.any_pb2.Any):
        raise Exception("message_any is not a protobuf.Any")

    message_type_url = message_any.type_url
    if message_type_url == "":
        return

    # Get the type name from the Any
    message_type_url_split = message_type_url.split('/')
    if len(message_type_url_split) < 2:
        print(f"message_any type_url `{message_type_url}` did not parse as expected.")
        raise Exception("Could not parse message_any type url.")
    message_type_name_full = message_type_url_split[1]
    message_type_name = message_type_name_full.split('.')[-1]
    # check message type name exists in namespace
    if not hasattr(son, message_type_name):
        print(f"Couldn't unpack '{message_type_name}' message")
        return None
    # Find the type in son-idl which matches this type url
    message_type = getattr(son, message_type_name)
    # Create an object of this type to allow unpacking of the Any
    message_typed = message_type()

    # Now unpack the Any, double check it is a valid type, and add it to the dictionary
    if message_any.Unpack(message_typed):
        return message_typed
    else:
        print(f"Failed to unpack '{message_type_name}' message")
        return None


def unpack_list_from_any(messages: list[google.protobuf.any_pb2.Any]):
    return [unpack_message_from_any(message) for message in messages]


def get_type_name(any_type: any):
    if isinstance(any_type, str):
        return any_type
    type_name = type(any_type).__name__
    if type_name == "MessageMeta":
        return type(any_type()).__name__
    return type_name


def get_type(any_type: any):
    if isinstance(any_type, str):
        # check message type name exists in namespace
        if not hasattr(son, any_type):
            print(f"Couldn't unpack '{any_type}' message")
            return None
        # Find the type in son-idl which matches this type url
        message_type = getattr(son, any_type)
        return message_type
    if type(any_type).__name__ == "MessageMeta":
        return type(any_type())
    return type(any_type)


def handle_result(result: son.Result):
    match result.success:
        case son.Result.OUTCOME_UNSPECIFIED:
            raise ResultUnspecifiedException(result.message)
        case son.Result.OUTCOME_FAILURE:
            raise ResultFailureException(result.message)
        case son.Result.OUTCOME_INVALID:
            raise ResultInvalidException(result.message)
        case son.Result.OUTCOME_RESTRICTED:
            raise ResultRestrictedException(result.message)
