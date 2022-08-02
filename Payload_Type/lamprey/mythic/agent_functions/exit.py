# Adapted from the example payload included in Mythic created by @its_a_feature_
from mythic_payloadtype_container.MythicCommandBase import *
from mythic_payloadtype_container.MythicRPC import *


class ExitArguments(TaskArguments):
    def __init__(self, command_line, **kwargs):
        super().__init__(command_line, **kwargs)
        self.args = []

    async def parse_arguments(self):
        pass

class ExitCommand(CommandBase):
    cmd = "exit"
    needs_admin = False
    help_cmd = "exit"
    description = "Exits the agent"
    version = 1
    author = "@darkwire"
    attackmapping = []
    supported_ui_features = ["callback_table:exit"]
    argument_class = ExitArguments
    attributes = CommandAttributes(
        spawn_and_injectable=False,
        builtin=True,
        load_only=False,
        suggested_command=False)

    async def create_tasking(self, task: MythicTask) -> MythicTask:
        return task

    async def process_response(self, response: AgentResponse):
        pass
