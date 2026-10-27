import sonardyne_api as son
import time

with son.WrapperGrpc('0.0.0.0', 8103) as wrapper:  
    # write to stream
    observation_stream = wrapper.open_observation_stream()
    print("\n(writing to observation stream) press ctrl-c to stop stream")
    try:
        while True:
            observation_stream.send(son.ZdaTimeSourceObservation(zda_data=son.ZdaData(current_utc_time_seconds = time.time())))
            time.sleep(1)
    except KeyboardInterrupt:
        pass