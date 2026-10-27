import sonardyne_api as son
import time

with son.WrapperGrpc('0.0.0.0', 8103) as wrapper:  
    observation_stream = wrapper.open_observation_stream(
        son.ObservationSubscriptionRequest(
            observation_subscriptions=[
                son.ObservationSubscription(matching_criteria=son.MatchingCriteria(match_type_name_suffix="NavigationModuleObservation"))
            ]
        )
    )
    print("\n(listening to observation stream) press ctrl-c to stop stream")
    try:
        while True:
            for message in observation_stream.recv():
                print(type(message), message)
                print("(listening to observation stream) press ctrl-c to stop stream")
                print(time.time())
    except KeyboardInterrupt:
        pass