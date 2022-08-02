# Originally written by @its_a_feature_, adapted by @darkwire

from mythic_payloadtype_container.MythicCommandBase import *
from mythic_payloadtype_container.MythicRPC import *


class ShellArguments(TaskArguments):
    def __init__(self, command_line, **kwargs):
        super().__init__(command_line, **kwargs)
        self.args = [
            CommandParameter(name="command", display_name="Command", type=ParameterType.String, description="Command to run"),
        ]

    async def parse_arguments(self):
        if len(self.command_line) == 0:
            raise ValueError("Must supply a command to run")
        self.add_arg("command", self.command_line)

    async def parse_dictionary(self, dictionary_arguments):
        self.load_args_from_dictionary(dictionary_arguments)

class ShellOpsec(CommandOPSEC):
    injection_method=""
    process_creation="os.popen(,shell=True)"
    authentication=""
    async def opsec_pre(self, task: MythicTask):
        task.opsec_pre_message= "This runs os.popen(), just FYI"

    async def opsec_post(self, task: MythicTask):
        task.opsec_pre_message= "You just ran os.popen()!!!"



class ShellCommand(CommandBase):
    cmd = "shell"
    needs_admin = False
    help_cmd = "shell {command}"
    description = "Calls a command with python os.popen"
    version = 1
    author = "@darkwire"
    attackmapping = ["T1059"]
    argument_class = ShellArguments
    opsec_class = ShellOpsec
    attributes = CommandAttributes(
        spawn_and_injectable=False,
        builtin=True,
        load_only=False,
        suggested_command=False)

    async def create_tasking(self, task: MythicTask) -> MythicTask:
        resp = await MythicRPC().execute("create_artifact", task_id=task.id,
            artifact="os.popen({},shell=True)".format(task.args.get_arg("command")),
            artifact_type="Process Create",
        )
        resp = await MythicRPC().execute("create_artifact", task_id=task.id,
            artifact="{}".format(task.args.get_arg("command")),
            artifact_type="Process Create",
        )
        task.display_params = task.args.get_arg("command")
        return task

    async def process_response(self, response: AgentResponse):
        pass
