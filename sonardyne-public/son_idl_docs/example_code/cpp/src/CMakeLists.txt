#Copyright 2024 Sonardyne

#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
#documentation files (the “Software”), to deal in the Software without restriction, including without limitation the
#rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
#permit persons to whom the Software is furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
#Software.

#THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
#WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
#COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

project (son_grpc_proto)

message("CMAKE_CURRENT_SOURCE_DIR: ${CMAKE_CURRENT_SOURCE_DIR}")

file(GLOB COMMON_PROTO        "${CMAKE_CURRENT_SOURCE_DIR}/../../../../../sonardyne-public/idl/common/*.proto")
file(GLOB CONFIGURATION_PROTO "${CMAKE_CURRENT_SOURCE_DIR}/../../../../../sonardyne-public/idl/configuration/*.proto")
file(GLOB SERVICES_PROTO      "${CMAKE_CURRENT_SOURCE_DIR}/../../../../../sonardyne-public/idl/services/*.proto")

add_library(${PROJECT_NAME} OBJECT ${PROTO_SRC_COMMON_FILES}
                                   ${PROTO_SRC_CONFIGURATION}
                                   ${PROTO_SRC_SERVICE})

target_include_directories(${PROJECT_NAME} PUBLIC "${CMAKE_BINARY_DIR}/sonardyne-public/")
target_include_directories(${PROJECT_NAME} PUBLIC "${CMAKE_BINARY_DIR}/sonardyne-public/idl/common/")
target_include_directories(${PROJECT_NAME} PUBLIC "${CMAKE_BINARY_DIR}/sonardyne-public/idl/configuration/")
target_include_directories(${PROJECT_NAME} PUBLIC "${CMAKE_BINARY_DIR}/sonardyne-public/idl/services/")
target_include_directories(${PROJECT_NAME} PUBLIC "$<BUILD_INTERFACE:${CMAKE_BINARY_DIR}>")


target_sources(${PROJECT_NAME} PUBLIC ${COMMON_PROTO}
                                      ${CONFIGURATION_PROTO}
                                      ${SERVICES_PROTO})

target_link_libraries(${PROJECT_NAME} PUBLIC protobuf::libprotobuf gRPC::grpc++)

#Generate the protobuf files
protobuf_generate(TARGET ${PROJECT_NAME} IMPORT_DIRS ../../../../../
                         PROTOC_OUT_DIR
                         ${CMAKE_BINARY_DIR}
                         LANGUAGE cpp)

#Generate the gRPC files
protobuf_generate(TARGET ${PROJECT_NAME} LANGUAGE grpc
                         GENERATE_EXTENSIONS .grpc.pb.h .grpc.pb.cc PLUGIN "protoc-gen-grpc=\$<TARGET_FILE:gRPC::grpc_cpp_plugin>"
                         IMPORT_DIRS ../../../../../
                         PROTOC_OUT_DIR ${CMAKE_BINARY_DIR})

add_executable(son_grpc_client main.cpp)
target_link_libraries(son_grpc_client ${PROJECT_NAME})