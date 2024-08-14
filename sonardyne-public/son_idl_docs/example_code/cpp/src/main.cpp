//Copyright 2023 Sonardyne

//Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
//documentation files (the “Software”), to deal in the Software without restriction, including without limitation the
//rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
//permit persons to whom the Software is furnished to do so, subject to the following conditions:

//The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
//Software.

//THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
//WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
//COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
//OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

#include <iostream>

#include <grpc/grpc.h>
#include <grpcpp/channel.h>
#include <grpcpp/client_context.h>
#include <grpcpp/create_channel.h>
#include <grpcpp/security/credentials.h>
#include <google/protobuf/util/json_util.h>

#include <state_service.grpc.pb.h>
#include <aiding_configuration.pb.h>

using namespace sonardyne::api;
using namespace sonardyne::api::pub::common;
using namespace sonardyne::api::pub::configuration;

class SonGrpcClient {
public:
  SonGrpcClient(std::string target_ipport) : _channel(grpc::CreateChannel(target_ipport, grpc::InsecureChannelCredentials())),
                                             _stub(StateService::NewStub(_channel)) {

  }

  void PrintVersion() {
    std::cout << "Calling GetVersion..." << std::endl;

    VersionRequest version_request;
    VersionResponse version_response;
    grpc::ClientContext client_context;
    grpc::Status get_version_status = _stub->GetVersion(&client_context, version_request, &version_response);
    if (get_version_status.ok()) {
      std::cout << "Called GetVersion: V" << version_response.major() << "." << version_response.minor() << std::endl;
    }
    else {
      std::cout << "GetVersion failed." << std::endl;
    }
  }

  void PrintAllStatesAsJSON(){
    ConfigurationRequest config_request;
    config_request.set_requestor(_requestor_name);
    ConfigurationEnvelope config_envelope;
    grpc::ClientContext client_context;
    std::cout << "Calling GetState..." << std::endl;
    grpc::Status get_state_status = _stub->GetState(&client_context, config_request, &config_envelope);

    if (get_state_status.ok()) {
      for(const auto& configuration : config_envelope.configuration()) {
        std::string json_string;
        auto status =google::protobuf::json::MessageToJsonString
            (configuration, &json_string);
        if(status.ok()) {
          std::cout << "Configuration: " << json_string << std::endl;
        }
      }
    }
    else {
      std::cout << "GetState Failed." << std::endl;
    }
  }
  void PrintAidingStates() {
    ConfigurationRequest config_request;
    config_request.set_requestor(_requestor_name);
    ConfigurationEnvelope config_envelope;
    grpc::ClientContext client_context;
    std::cout << "Calling GetState..." << std::endl;
    grpc::Status get_state_status = _stub->GetState(&client_context, config_request, &config_envelope);

    if (get_state_status.ok()) {
      for(const auto& configuration : config_envelope.configuration()) {
        std::cout << "Configuration: " << configuration.DebugString() << std::endl;

        if(configuration.Is<AidingConfiguration>()){
          AidingConfiguration aiding_config;
          configuration.UnpackTo(&aiding_config);

          std::cout << "Called GetState:" << std::endl;
          PrintAnAidingState("GNSS", aiding_config.enable_gnss().value());
          PrintAnAidingState("XPOS", aiding_config.enable_xpos().value());
          PrintAnAidingState("USBL", aiding_config.enable_xpos().value());
        }
      }
    }
    else {
      std::cout << "GetState Failed." << std::endl;
    }
  }

  grpc::Status SetState(ConfigurationEnvelope request_config_envelope) {
    ConfigurationEnvelope response_config_envelope;
    grpc::ClientContext client_context;
    std::cout << "Calling SetState..." << std::endl;
    return _stub->SetState(&client_context, request_config_envelope, &response_config_envelope);
  }

private:
  std::shared_ptr<grpc::Channel> _channel;
  std::unique_ptr<StateService::Stub> _stub;
  std::string _requestor_name = "C++ Client";

  void PrintAnAidingState(std::string aiding_source, AidingState_AidingStateEnum aiding_state) {
    if (aiding_state == AidingState_AidingStateEnum_ENABLED) {
      std::cout << aiding_source << " Aiding is enabled." << std::endl;
    }
    else if (aiding_state == AidingState_AidingStateEnum_DISABLED) {
      std::cout << aiding_source << " Aiding is disabled." << std::endl;
    }
    else {
      std::cout << aiding_source << " Aiding state unknown." << std::endl;
    }
  }
};

int main (int argc, char *argv[]) {
  // NOTE: Change the IP Address and Port to match the Instrument and its gRPC configuration.
  SonGrpcClient client("192.168.179.11:7777");
  client.PrintVersion();
  client.PrintAidingStates();

  ConfigurationEnvelope request_config_envelope;
  AidingConfiguration aiding_config;
  aiding_config.mutable_enable_gnss()->set_value(AidingState_AidingStateEnum_ENABLED);
  aiding_config.mutable_enable_xpos()->set_value(AidingState_AidingStateEnum_ENABLED);
  aiding_config.mutable_enable_usbl()->set_value(AidingState_AidingStateEnum_ENABLED);
  request_config_envelope.add_configuration()->PackFrom(aiding_config);

  client.SetState(request_config_envelope);

  client.PrintAidingStates();
  client.PrintAllStatesAsJSON();

  return 0;
}
