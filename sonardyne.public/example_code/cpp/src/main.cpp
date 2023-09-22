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

#include "service.pb.h"
#include "service.grpc.pb.h"

class SonGrpcClient {
public:
  SonGrpcClient(std::string target_ipport) :
    _channel(grpc::CreateChannel(target_ipport, grpc::InsecureChannelCredentials())),
    _stub(sonardyne::api::SonardyneService::NewStub(_channel)) {

  }

  void PrintVersion() {
    std::cout << "Calling GetVersion..." << std::endl;

    sonardyne::api::VersionRequest version_request;
    sonardyne::api::VersionResponse version_response;
    grpc::ClientContext client_context;
    grpc::Status get_version_status = _stub->GetVersion(&client_context, version_request, &version_response);
    if (get_version_status.ok()) {
      std::cout << "Called GetVersion: V" << version_response.major() << "." << version_response.minor() << std::endl;
    }
    else {
      std::cout << "GetVersion failed." << std::endl;
    }
  }

  void PrintAidingStates() {
    sonardyne::api::ConfigurationRequest config_request;
    config_request.set_requestor(_requestor_name);
    sonardyne::api::ConfigurationEnvelope config_envelope;
    grpc::ClientContext client_context;
    std::cout << "Calling GetState..." << std::endl;
    grpc::Status get_state_status = _stub->GetState(&client_context, config_request, &config_envelope);
    if (get_state_status.ok()) {
      sonardyne::api::AidingConfiguration_AIDING_STATE gnss_state = config_envelope.configuration().aiding_configurations()[0].enable_gnss();
      sonardyne::api::AidingConfiguration_AIDING_STATE xpos_state = config_envelope.configuration().aiding_configurations()[0].enable_xpos();
      sonardyne::api::AidingConfiguration_AIDING_STATE usbl_state = config_envelope.configuration().aiding_configurations()[0].enable_usbl();

      std::cout << "Called GetState:" << std::endl;
      PrintAnAidingState("GNSS", gnss_state);
      PrintAnAidingState("XPOS", xpos_state);
      PrintAnAidingState("USBL", usbl_state);
    }
    else {
      std::cout << "GetState Failed." << std::endl;
    }
  }

  grpc::Status SetState(sonardyne::api::ConfigurationEnvelope request_config_envelope) {
    sonardyne::api::ConfigurationEnvelope response_config_envelope;
    grpc::ClientContext client_context;
    std::cout << "Calling SetState..." << std::endl;
    return _stub->SetState(&client_context, request_config_envelope, &response_config_envelope);
  }

private:
  std::shared_ptr<grpc::Channel> _channel;
  std::unique_ptr<sonardyne::api::SonardyneService::Stub> _stub;
  std::string _requestor_name = "C++ Client";

  void PrintAnAidingState(std::string aiding_source, sonardyne::api::AidingConfiguration_AIDING_STATE aiding_state) {
    if (aiding_state == sonardyne::api::AidingConfiguration_AIDING_STATE_ENABLED) {
      std::cout << aiding_source << " Aiding is enabled." << std::endl;
    }
    else if (aiding_state == sonardyne::api::AidingConfiguration_AIDING_STATE_DISABLED) {
      std::cout << aiding_source << " Aiding is disabled." << std::endl;
    }
    else {
      std::cout << aiding_source << " Aiding state unknown." << std::endl;
    }
  }
};

int main (int argc, char *argv[]) {
  SonGrpcClient client("127.0.0.1:1234"); // NOTE: Change the IP Address and Port to match the Instrument and its gRPC configuration.
  client.PrintVersion();
  client.PrintAidingStates();

  sonardyne::api::ConfigurationEnvelope request_config_envelope;
  sonardyne::api::AidingConfiguration *aiding_config = request_config_envelope.mutable_configuration()->add_aiding_configurations();
  aiding_config->set_enable_gnss(sonardyne::api::AidingConfiguration_AIDING_STATE_ENABLED);
  aiding_config->set_enable_xpos(sonardyne::api::AidingConfiguration_AIDING_STATE_ENABLED);
  aiding_config->set_enable_usbl(sonardyne::api::AidingConfiguration_AIDING_STATE_ENABLED);

  grpc::Status setstate_status = client.SetState(request_config_envelope);

  client.PrintAidingStates();

  return 0;
}
