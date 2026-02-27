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
    print(wrapper.set_configuration(son.DvlAlgorithmConfiguration(
        dvl_rate=son.DvlRate(value=son.DvlRate.DvlRateEnum.DVL_RATE_ENUM_FIXED_5HZ),
        dvl_mode=son.DvlMode(value=son.DvlMode.DVL_MODE_ENUM_DVL),
        adcp_parameters=son.DvlAdcpParameters(
            number_of_cells=son.BoundedUInt32(value=100),
            preferred_cell_width_metres=son.BoundedDouble(value=0.1),
            pings_to_average=son.BoundedUInt32(value=10),
            dvl_adcp_ping_ratio=son.BoundedUInt32(value=10),
            velocity_limit=son.AdcpVelocityLimit(value=son.AdcpVelocityLimit.ADCP_VELOCITY_LIMIT_ENUM_STANDARD)
        ),
        input_trigger_parameters=son.DvlInputTriggerParameters(
            input_trigger_port=son.TriggerPortReference(set_uid=son.UniqueID(name="Trigger A1")),
            input_trigger_edge=son.TRIGGER_EDGE_RISING,
            input_trigger_delay_seconds=son.BoundedDouble(value=0.1)
        )
    )))
