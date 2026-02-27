import os
import shutil
import re
from pathlib import Path
from hatchling.builders.hooks.plugin.interface import BuildHookInterface
from hatch_protobuf.hooks import ProtocHook

"""
The intention is to have build steps before and after ProtocHook.

We cannot use the initialise & finalise methods of one custom hook
to wrap the ProtocHook. This is because the finalise method is more
for cleanup, and does not affect the artefacts written to site_packages.

So we effectively want two "initialise" methods to happen around the ProtocHook,
so we run the ProtocHook from within this custom hook.
"""

class CustomHook(BuildHookInterface):
    protos_dir = "protos"

    def tidy_up(self):
        # Remove generated python
        entries_to_remove = [
            "sonardyne_api/sonardyne",
            "sonardyne_api/sonardyne/__init__.py",
            "sonardyne_api/sonardyne_private",
            "sonardyne_api/sonardyne_public"
        ]
        for entry_to_remove in entries_to_remove:
            if os.path.isdir(entry_to_remove):
                for filename in os.listdir(entry_to_remove):
                    file_path = os.path.join(entry_to_remove, filename)
                    try:
                        if os.path.isfile(file_path) or os.path.islink(file_path):
                            os.unlink(file_path)
                        elif os.path.isdir(file_path):
                            shutil.rmtree(file_path)
                    except Exception as e:
                        print('Failed to delete %s. Reason: %s' % (file_path, e))
                shutil.rmtree(entry_to_remove)
            if os.path.isfile(entry_to_remove):
                try:
                    os.unlink(entry_to_remove)
                except Exception as e:
                    print('Failed to delete %s. Reason: %s' % (entry_to_remove, e))

        # Remove tmp protos
        if os.path.isdir(CustomHook.protos_dir):
            shutil.rmtree(CustomHook.protos_dir)

    def pre_protoc(self, version: str, build_data) -> None:
        proto_paths = self.config.get('proto_paths_source', [])
        exclude_dirs = self.config.get('exclude_dirs', [])
        for proto_path in proto_paths:
            for dp, dn, fn in os.walk(proto_path):
                for f in fn:
                    if not f.endswith(".proto"):
                        continue

                    # Prevent self from being copied into self recursively
                    path = os.path.abspath(dp)
                    cwd = os.getcwd()
                    is_inside = os.path.commonpath([path, cwd]) == cwd
                    if is_inside:
                        continue
                    # Prevent excluded folders from being copied
                    path = Path(str(os.path.join(dp, f)))
                    exclude_folder = False
                    for part in path.parts:
                        for exclude_dir in exclude_dirs:
                            if re.match(exclude_dir, part):
                                exclude_folder = True
                    if exclude_folder:
                        continue
                    # Copy file to tmp area
                    base_path = Path(proto_path)
                    relative_path = path.relative_to(base_path)
                    new_path = os.path.join(CustomHook.protos_dir, relative_path)
                    os.makedirs(os.path.dirname(new_path), exist_ok=True)
                    shutil.copy(path, new_path)

    def post_protoc(self, version: str, build_data) -> None:
        # Create __init__.py with imports for every generated python file
        output_directory = "sonardyne_api"
        filepaths = []
        for dp, dn, fn in os.walk(output_directory):
            for f in fn:
                filepaths.append(os.path.join(dp, f))

        init_lines = []
        for filepath in filepaths:
            if os.path.isfile(filepath) and (filepath[-6:] == "pb2.py" or filepath[-11:] == "pb2_grpc.py") and filepath != "__init__.py":
                with open(filepath, "r") as proto_filehandle:
                    new_text = proto_filehandle.read()
                    new_text = new_text.replace("from sonardyne_public.idl.", f"from {output_directory}.sonardyne_public.idl.")
                    new_text = new_text.replace("from sonardyne_private.idl.", f"from {output_directory}.sonardyne_private.idl.")
                    new_text = new_text.replace("from sonardyne.api.", f"from {output_directory}.sonardyne.api.")
                with open(filepath, "w") as proto_filehandle:
                    proto_filehandle.write(new_text)
                file = filepath[:-3]
                file = file.replace('/', '.')
                file = file.replace('\\', '.')
                init_lines.append(f"from {file} import *\n")
        with open(f"{output_directory}/__init__.py", "w") as init_filehandle:
            for init_line in init_lines:
                if ".sonardyne.api." in init_line:
                    init_filehandle.write(init_line)
            init_filehandle.write(f"from {output_directory}.wrapper_grpc import WrapperGrpc\n")
            init_filehandle.write(f"from {output_directory}.wrapper_json_tcp import WrapperJsonTcp\n")
            init_filehandle.write(f"from {output_directory}.wrapper_framed_tcp import WrapperFramedTcp\n")
            init_filehandle.write(f"from {output_directory}.unpacking import *\n")


class ProtocWrapperHook(BuildHookInterface):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pb_hook = ProtocHook(
            self.root, self.config, self.build_config,
            self.metadata, self.directory, self.target_name
        )
        self.custom_hook = CustomHook(
            self.root, self.config, self.build_config,
            self.metadata, self.directory, self.target_name
        )

    def initialize(self, version, build_data):
        self.custom_hook.tidy_up()
        self.custom_hook.pre_protoc(version, build_data)
        self.pb_hook.initialize(version, build_data)
        self.custom_hook.post_protoc(version, build_data)

    def finalize(self, version, build_data, artifact_path):
        self.pb_hook.finalize(version, build_data, artifact_path)
        self.custom_hook.tidy_up()


def get_build_hook():
    return ProtocWrapperHook
