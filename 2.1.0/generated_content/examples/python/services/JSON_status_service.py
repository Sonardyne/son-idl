import sonardyne_api as son

with son.WrapperJsonTcp('0.0.0.0', 8103) as wrapper:  
    status_stream = wrapper.open_status_stream(
        son.StatusSubscriptionRequest(status_subscriptions=[
            son.StatusSubscription(matching_criteria=son.MatchingCriteria(match_type_name_suffix="InsAlgorithmStatus"))
        ])
    )
    print("\n(listening to status stream) press ctrl-c to stop stream")
    try:
        while True:
            for message in status_stream.recv():
                print(type(message), message)
                print("(listening to status stream) press ctrl-c to stop stream")
    except KeyboardInterrupt:
        pass