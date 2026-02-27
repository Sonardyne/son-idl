import sonardyne_api as son
import time

with son.WrapperJsonTcp('0.0.0.0', 8103) as wrapper:  
    # write to stream
    observation_stream = wrapper.open_observation_stream()
    print("\n(writing to observation stream) press ctrl-c to stop stream")
    try:
        while True:
            observation_stream.send(son.SusblSourceObservation(psimssb_telegram=son.PsimssbTelegram(
                time_of_validity=son.Timestamp(common_time_seconds=time.time()),
                coordinate_type=son.PsimssbTelegram.PSIMSSB_COORDINATE_SYSTEM_RADIANS,
                x_coordinate=0,
                y_coordinate=0,
                transponder_code=0,
                is_valid=True,
                orientation_type=son.PsimssbTelegram.PSIMSSB_ORIENTATION_NORTH,
                error_code="",
                software_filter=son.PsimssbTelegram.PSIMSSB_SOFTWARE_FILTER_UNKNOWN,
                depth_metres=0,
                position_uncertainty_metres=1
            )))
            time.sleep(1)
    except KeyboardInterrupt:
        pass

    # read from stream
    observation_stream = wrapper.open_observation_stream(
        son.ObservationSubscriptionRequest(observation_subscriptions=[
            son.ObservationSubscription(matching_criteria=son.MatchingCriteria(match_type_name_suffix="SusblSourceObservation"))
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