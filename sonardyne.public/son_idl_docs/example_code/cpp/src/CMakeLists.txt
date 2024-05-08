#Copyright 2023 Sonardyne

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

# Compile the .proto files
foreach(_proto configuration result service timestamp uid version)
    get_filename_component(${_proto}_proto "../protos/${_proto}.proto" ABSOLUTE)
    get_filename_component(${_proto}_proto_path "${${_proto}_proto}" PATH)

    set(${_proto}_proto_sources "${CMAKE_CURRENT_BINARY_DIR}/${_proto}.pb.cc")
    set(${_proto}_proto_headers "${CMAKE_CURRENT_BINARY_DIR}/${_proto}.pb.h")
    set(${_proto}_grpc_sources "${CMAKE_CURRENT_BINARY_DIR}/${_proto}.grpc.pb.cc")
    set(${_proto}_grpc_headers "${CMAKE_CURRENT_BINARY_DIR}/${_proto}.grpc.pb.h")

    add_custom_command(
            OUTPUT "${${_proto}_proto_sources}" "${${_proto}_proto_headers}" "${${_proto}_grpc_sources}" "${${_proto}_grpc_headers}"
            COMMAND ${_PROTOBUF_PROTOC}
            ARGS --grpc_out "${CMAKE_CURRENT_BINARY_DIR}" --cpp_out "${CMAKE_CURRENT_BINARY_DIR}"
            -I "${${_proto}_proto_path}"
            --plugin=protoc-gen-grpc="${_GRPC_CPP_PLUGIN_EXECUTABLE}"
            "${${_proto}_proto}"
            DEPENDS "${${_proto}_proto}")
endforeach()

include_directories(${CMAKE_CURRENT_BINARY_DIR})

add_library(son_grpc_proto
        ${configuration_proto_sources}
        ${configuration_proto_headers}
        ${configuration_grpc_sources}
        ${configuration_grpc_headers}
        ${result_proto_sources}
        ${result_proto_headers}
        ${result_grpc_sources}
        ${result_grpc_headers}
        ${service_proto_sources}
        ${service_proto_headers}
        ${service_grpc_sources}
        ${service_grpc_headers}
        ${timestamp_proto_sources}
        ${timestamp_proto_headers}
        ${timestamp_grpc_sources}
        ${timestamp_grpc_headers}
		${uid_proto_sources}
        ${uid_proto_headers}
        ${uid_grpc_sources}
        ${uid_grpc_headers}
        ${version_proto_sources}
        ${version_proto_headers}
        ${version_grpc_sources}
        ${version_grpc_headers})
target_link_libraries(son_grpc_proto
        gRPC::grpc++)

add_executable(son_grpc_client
        main.cpp)
target_link_libraries(son_grpc_client
        son_grpc_proto
        gRPC::grpc++)
