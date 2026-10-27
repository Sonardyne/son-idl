import sonardyne_api as son

with son.WrapperJsonTcp('0.0.0.0', 8103) as wrapper:  

    print("all configurations:")
    configurations = wrapper.get_configurations("Configuration")
    for configuration in configurations:
        print(f"    • {type(configuration).__name__}")

    print("all configurations ending in SourceConfiguration:")
    configurations = wrapper.get_configurations("SourceConfiguration")
    for configuration in configurations:
        print(f"    • {type(configuration).__name__}")

    configuration_stream = wrapper.open_configuration_stream(
        son.ConfigurationSubscriptionRequest(configuration_subscriptions=[
            son.ConfigurationSubscription(matching_criteria=son.MatchingCriteria(match_type_name_suffix="Configuration"))
        ])
    )
    print("\n(listening to configuration stream) press ctrl-c to stop stream")
    try:
        while True:
            for message in configuration_stream.recv():
                print(type(message), message)
                print("(listening to configuration stream) press ctrl-c to stop stream")
    except KeyboardInterrupt:
        pass