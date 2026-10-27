import sonardyne_api as son
import time
import random

with son.WrapperGrpc('0.0.0.0', 8103) as wrapper:  
    comms_stream  = wrapper.open_comms_stream(
        son.CommsSubscriptionRequest(comms_subscriptions=[
            son.CommsSubscription(matching_criteria=son.MatchingCriteria(match_uids=[son.UniqueID(name="TCP-8110")]))
        ])
    )

    # write to stream
    print("\n(writing to comms stream) press ctrl-c to stop stream")
    try:
        while True:
            comms_stream.send(
                son.DataPortComms(
                    uid=son.UniqueID(name="TCP-8110"),
                    data_direction=son.DataDirection.DATA_DIRECTION_OUTPUT,
                    data=f"Hello World! {random.randrange(100)}".encode()
                )
            )
            time.sleep(1)
    except KeyboardInterrupt:
        pass

    # read from stream
    print("\n(listening to comms stream) press ctrl-c to stop stream")
    try:
        while True:
            for message in comms_stream.recv():
                print(type(message), message)
                print("(listening to comms stream) press ctrl-c to stop stream")
    except KeyboardInterrupt:
        pass