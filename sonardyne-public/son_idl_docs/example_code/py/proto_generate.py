import os
import pipes
import subprocess

def _proto_generate(filename):
    process = subprocess.Popen(["python", "-m" "grpc_tools.protoc", "--proto_path=.", "--python_out", "sonardyne-public/example_code/py/", "--grpc_python_out", "sonardyne-public/example_code/py/", filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    # errcode = process.returncode
    print(out.decode("utf-8"))
    print(err.decode("utf-8"))

def proto_generate():
    os.chdir('../../..')
    _proto_generate('sonardyne-public/idl/common/*.proto')
    _proto_generate('sonardyne-public/idl/configuration/*.proto')
    _proto_generate('sonardyne-public/idl/services/*.proto')


