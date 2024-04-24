import json
from abc import ABC, abstractmethod


class Command(ABC):
    @abstractmethod
    def execute(self, receiver, context):
        pass


class Context:
    def __init__(self, params):
        self.__context = {}
        if hasattr(params, "secret"):
            self.set("secret", params.secret)
        if hasattr(params, "auth_token"):
            self.set("auth_token", params.auth_token)
        if hasattr(params, "user_id"):
            self.set("user_id", params.user_id)
        if hasattr(params, "password"):
            self.set("password", params.password)
        if hasattr(params, "tenant_id"):
            self.set("tenant_id", params.tenant_id)
        if hasattr(params, "server_id"):
            self.set("server_id", params.server_id)
        if hasattr(params, "image_name"):
            self.set("image_name", params.image_name)
        if hasattr(params, "image_id"):
            self.set("image_id", params.image_id)
        if hasattr(params, "iso_file"):
            self.set("iso_file", params.iso_file)

    def set(self, key, value):
        self.__context[key] = value

    def get(self, key):
        return self.__context.get(key)


class CompositeCommand(Command):
    def __init__(self):
        self.__commands = []

    def append(self, command):
        self.__commands.append(command)

    def execute(self, receiver, context):
        for command in self.__commands:
            command.execute(receiver, context)


class GenerateToken(Command):
    def __init__(self, force=False):
        self.force = force

    def execute(self, receiver, context):
        if context.get("auth_token") is None or self.force:
            receiver.generate_token(context)


class SaveSecret(Command):
    def execute(self, receiver, context):
        if context.get("secret") is not None:
            secrets = {
                "auth_token": context.get("auth_token"),
                "user_id": context.get("user_id"),
                "password": context.get("password"),
                "tenant_id": context.get("tenant_id"),
            }
            with open(context.get("secret"), "w") as fp:
                json.dump(secrets, fp, indent=2, sort_keys=True)


class LoadSecret(Command):
    def execute(self, receiver, context):
        if context.get("secret") is not None:
            with open(context.get("secret"), "r") as fp:
                secrets = json.load(fp)
            context.set("auth_token", secrets.get("auth_token"))
            for key in ["user_id", "password", "tenant_id"]:
                if secrets[key]:
                    context.set(key, secrets[key])


class LoadToken(CompositeCommand):
    def __init__(self):
        super().__init__()
        super().append(LoadSecret())
        super().append(GenerateToken())
        super().append(SaveSecret())


class GenerateImageId(Command):
    def execute(self, receiver, context):
        if context.get("image_id") is None:
            receiver.generate_image_id(context)


class UploadImage(Command):
    def execute(self, receiver, context):
        receiver.upload_image(context)


class DeleteImage(Command):
    def execute(self, receiver, context):
        receiver.delete_image(context)


class ListServer(Command):
    def execute(self, receiver, context):
        receiver.list_server(context)


class StartServer(Command):
    def execute(self, receiver, context):
        receiver.start_server(context)


class StopServer(Command):
    def execute(self, receiver, context):
        receiver.stop_server(context)


class StopServerAndWait(Command):
    def execute(self, receiver, context):
        receiver.stop_server_and_wait(context)


class GetServerStatus(Command):
    def execute(self, receiver, context):
        receiver.get_server_status(context)


class GetServerConsole(Command):
    def execute(self, receiver, context):
        receiver.get_server_console(context)


class ListImage(Command):
    def execute(self, receiver, context):
        receiver.list_image(context)


class MountImage(Command):
    def execute(self, receiver, context):
        receiver.mount_image(context)


class UnmountImage(Command):
    def execute(self, receiver, context):
        receiver.unmount_image(context)
