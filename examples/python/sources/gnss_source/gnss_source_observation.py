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

with son.WrapperGrpc('0.0.0.0', 8103) as wrapper:  # Device IP address & gRPC port:
    # write to stream
    observation_stream = wrapper.open_observation_stream()
    print("\n(writing to observation stream) press ctrl-c to stop stream")
    try:
        while True:
            observation_stream.send(son.GnssSourceObservation(gga_telegram=son.GgaTelegram(
                time_of_validity=son.Timestamp(common_time_seconds=time.time()),
                latitude_radians=0.0,
                longitude_radians=0.0,
                altitude_metres=0.0,
                geoid_separation_metres=0.0,
                hdop=0.5,
                age_seconds=0.0,
                number_of_satellites=10,
                reference_station_id=None,
                fix_quality=son.GgaTelegram.FIX_QUALITY_GNSS_FIX
            )))
            time.sleep(1)
    except KeyboardInterrupt:
        pass

    # read from stream
    observation_stream = wrapper.open_observation_stream(
        son.ObservationSubscriptionRequest(observation_subscriptions=[
            son.ObservationSubscription(matching_criteria=son.MatchingCriteria(match_type_name_suffix="GnssSourceObservation"))
        ])
    )
    print("\n(listening to observation stream) press ctrl-c to stop stream")
    try:
        while True:
            for message in observation_stream.recv():
                print(type(message), message)
                print("(listening to observation stream) press ctrl-c to stop stream")
    except KeyboardInterrupt:
        pass
