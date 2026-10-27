import sonardyne_api as son
import time
import random

with son.WrapperFramedTcp('0.0.0.0', 8103) as wrapper:  
    # write to stream
    observation_stream = wrapper.open_observation_stream()
    print("\n(writing to observation stream) press ctrl-c to stop stream")
    try:
        while True:
            observation = son.SoundVelocitySourceObservation(sound_velocity_data=son.SoundVelocityData(
                time_of_validity=son.Timestamp(common_time_seconds=time.time()),
                sound_velocity_meters_per_second=1500.0 + random.randrange(-500,500) * 0.01
            ))
            observation_stream.send(observation)
            time.sleep(1)
    except KeyboardInterrupt:
        pass

    # read from stream
    observation_stream = wrapper.open_observation_stream(
        son.ObservationSubscriptionRequest(observation_subscriptions=[
            son.ObservationSubscription(matching_criteria=son.MatchingCriteria(match_type_name_suffix="SoundVelocitySourceObservation"))
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