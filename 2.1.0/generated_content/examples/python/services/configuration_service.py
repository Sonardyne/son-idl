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

with son.WrapperGrpc('0.0.0.0', 8103) as wrapper:  # Device IP address & gRPC port:

    print("all configurations:")
    configurations = wrapper.get_configurations("Configuration")
    for configuration in configurations:
        print(f"    • {type(configuration).__name__}")

    print("all configurations ending in SourceConfiguration:")
    configurations = wrapper.get_configurations("SourceConfiguration")
    for configuration in configurations:
        print(f"    • {type(configuration).__name__}")

    configuration_stream = wrapper.open_configuration_stream(
        son.ConfigurationSubscriptionRequest(configuration_subscriptions=[
            son.ConfigurationSubscription(matching_criteria=son.MatchingCriteria(match_type_name_suffix="Configuration"))
        ])
    )
    print("\n(listening to configuration stream) press ctrl-c to stop stream")
    try:
        while True:
            for message in configuration_stream.recv():
                print(type(message), message)
                print("(listening to configuration stream) press ctrl-c to stop stream")
    except KeyboardInterrupt:
        pass
