import sonardyne_api as son

def pascals_to_depth(pressure_pa):
    """
    Converts pressure in Pascals to depth in meters.
    Default is sea water, set sea_water=False for fresh water.
    """
    g = 9.81  # Acceleration due to gravity (m/s^2)
    rho = 1000  # Density of fresh water (kg/m^3)
    depth = pressure_pa / (rho * g)
    return depth

with son.WrapperGrpc('0.0.0.0', 8103) as wrapper:  
    # Set up depth source to use internal sensor with external depth conversion.
    wrapper.set_configuration(son.DepthSourceConfiguration(
        input_depth_data_source_reference=son.DepthDataSourceReference(set_any_pressure_sensor=True),
        pressure_to_depth_conversion=son.DepthSourceConfiguration.PRESSURE_TO_DEPTH_CONVERSION_EXTERNAL
    ))
    # Open stream to start listening for pressure sensor observations, so we can give them an externally calculated depth.
    observation_stream = wrapper.open_observation_stream(son.ObservationSubscriptionRequest(observation_subscriptions=[
        son.ObservationSubscription(matching_criteria=son.MatchingCriteria(match_type_name_suffix="PressureSensorObservation"))
    ]))
    try:
        while True:
            for observation in observation_stream.recv():
                if isinstance(observation, son.PressureSensorObservation):
                    # ignore messages which already have externally_calculated_depth_metres set.
                    if not observation.pressure_data.HasField("externally_calculated_depth_metres"):
                        depth = pascals_to_depth(observation.pressure_data.pressure_pascals)
                        observation.pressure_data.externally_calculated_depth_metres = depth + 10 # Add some offset so the difference is obvious.
                        observation_stream.send(observation)
    except KeyboardInterrupt:
        pass