from mythic_payloadtype_container.PayloadBuilder import *
from mythic_payloadtype_container.MythicCommandBase import *
from mythic_payloadtype_container.MythicRPC import *
import sys
import json
import base64

#define your payload type class here, it must extend the PayloadType class though
class Lamprey(PayloadType):

    name = "lamprey"  # name that would show up in the UI
    file_extension = "py"  # default file extension to use when creating payloads
    author = "@darkwire37"  # author of the payload type
    supported_os = [  # supported OS and architecture combos
        SupportedOS.Linux # update this list with all the OSes your agent supports
    ]
    wrapper = False  # does this payload type act as a wrapper for another payloads inside of it?
    # if the payload supports any wrapper payloads, list those here
    wrapped_payloads = [] # ex: "service_wrapper"
    note = "Should run on anything that runs python3"
    supports_dynamic_loading = False  # setting this to True allows users to only select a subset of commands when generating a payload
    build_parameters = [
       BuildParameter(
            name="encoding",
            parameter_type=BuildParameterType.ChooseOne,
            description="Choose payload encoding",
            choices=["py", "base64"],
            default_value="py"
        ),
    ]
    #  the names of the c2 profiles that your agent supports
    c2_profiles = ["http"]
    translation_container = None
    # after your class has been instantiated by the mythic_service in this docker container and all required build parameters have values
    # then this function is called to actually build the payload
    async def build(self) -> BuildResponse:
        # this function gets called to create an instance of your payload
        base_code = open(self.agent_code_path / "base_agent.py", "r").read()
        base_code = base_code.replace("UUID_Here",self.uuid)
        for c2 in self.c2info:
            profile = c2.get_c2profile()["name"]
            for key, val in c2.get_parameters_dict().items():
                for c2 in self.c2info:
                    profile = c2.get_c2profile()["name"]
                    for key, val in c2.get_parameters_dict().items():
                        if not isinstance(val, str):
                            base_code = base_code.replace(key, \
                            json.dumps(val).replace("false", "False").replace("true","True").replace("null","None"))
                        else:
                            base_code = base_code.replace(key, val)
        if self.get_parameter("encoding") == "base64":
            encoded_code = base64.b64encode(base_code.encode())
            decoder_code = open(self.agent_code_path / "decoder.py", "r").read()
            base_code = decoder_code.replace("encoded_code",encoded_code.decode())
        resp = BuildResponse(status=BuildStatus.Success)
        resp.payload = base_code.encode()
        return resp
