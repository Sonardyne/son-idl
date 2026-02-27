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

import sonardyne_api as son
import time
import random

with son.WrapperGrpc('0.0.0.0', 8103) as wrapper:  # Device IP address & gRPC port:
    comms_stream  = wrapper.open_comms_stream(
        son.CommsSubscriptionRequest(comms_subscriptions=[
            son.CommsSubscription(matching_criteria=son.MatchingCriteria(match_uids=[son.UniqueID(name="TCP-8110")]))
        ])
    )

    # write to stream
    print("\n(writing to comms stream) press ctrl-c to stop stream")
    try:
        while True:
            comms_stream.send(
                son.DataPortComms(
                    uid=son.UniqueID(name="TCP-8110"),
                    data_direction=son.DataDirection.DATA_DIRECTION_OUTPUT,
                    data=f"Hello World! {random.randrange(100)}".encode()
                )
            )
            time.sleep(1)
    except KeyboardInterrupt:
        pass

    # read from stream
    print("\n(listening to comms stream) press ctrl-c to stop stream")
    try:
        while True:
            for message in comms_stream.recv():
                print(type(message), message)
                print("(listening to comms stream) press ctrl-c to stop stream")
    except KeyboardInterrupt:
        pass
