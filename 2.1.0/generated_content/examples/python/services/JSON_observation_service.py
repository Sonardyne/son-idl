import sonardyne_api as son

with son.WrapperJsonTcp('0.0.0.0', 8103) as wrapper:  
    observation_stream = wrapper.open_observation_stream(
        son.ObservationSubscriptionRequest(observation_subscriptions=[
            son.ObservationSubscription(matching_criteria=son.MatchingCriteria(match_type_name_suffix="GnssSourceObservation")),
            son.ObservationSubscription(matching_criteria=son.MatchingCriteria(match_type_name_suffix="XposSourceObservation")),
            son.ObservationSubscription(matching_criteria=son.MatchingCriteria(match_type_name_suffix="SusblSourceObservation")),
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