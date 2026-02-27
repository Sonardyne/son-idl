import sonardyne_api as son
import time

with son.WrapperFramedTcp('0.0.0.0', 8103) as wrapper:  
    # write to stream
    observation_stream = wrapper.open_observation_stream()
    print("\n(writing to observation stream) press ctrl-c to stop stream")
    try:
        while True:
            observation = son.XposSourceObservation(xpos_data=son.XposData(
                time_of_validity=son.Timestamp(common_time_seconds=time.time()),
                latitude_radians=0.0,
                longitude_radians=0.0,
                depth_metres=0.0,
                depth_uncertainty_metres=1.0,
                horizontal_position_uncertainty_metres=0.5,
                source=son.XPOS_SOURCE_GNSS
            ))
            observation_stream.send(observation)
            time.sleep(1)
    except KeyboardInterrupt:
        pass

    # read from stream
    observation_stream = wrapper.open_observation_stream(
        son.ObservationSubscriptionRequest(observation_subscriptions=[
            son.ObservationSubscription(matching_criteria=son.MatchingCriteria(match_type_name_suffix="XposSourceObservation"))
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