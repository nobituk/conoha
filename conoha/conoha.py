import json
import time
from abc import ABC, abstractmethod
from urllib.request import Request, urlopen

USER_AGENT = "curl/8.4.0"


class RestApi(ABC):
    @abstractmethod
    def generate_request(self, params):
        pass

    def generate_token_request(self, context):
        params = {}
        params["url"] = "https://identity.c3j1.conoha.io/v3/auth/tokens"
        params["method"] = "post"
        params["headers"] = {
            "User-Agent": USER_AGENT,
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        params["payload"] = json.dumps(
            {
                "auth": {
                    "identity": {
                        "methods": ["password"],
                        "password": {
                            "user": {
                                "id": context.get("user_id"),
                                "password": context.get("password"),
                            }
                        },
                    },
                    "scope": {"project": {"id": context.get("tenant_id")}},
                }
            }
        ).encode("utf-8")
        return self.generate_request(params)

    @abstractmethod
    def generate_token(self, context):
        pass

    def list_image_request(self, context):
        params = {}
        params[
            "url"
        ] = "https://image-service.c3j1.conoha.io/v2/images?owner={}".format(
            context.get("tenant_id")
        )
        params["method"] = "get"
        params["headers"] = {
            "User-Agent": USER_AGENT,
            "Accept": "application/json",
            "X-Auth-Token": context.get("auth_token"),
        }
        params["payload"] = None
        return self.generate_request(params)

    @abstractmethod
    def list_image(self, context):
        pass

    def generate_image_id_request(self, context):
        params = {}
        params["url"] = "https://image-service.c3j1.conoha.io/v2/images"
        params["method"] = "post"
        params["headers"] = {
            "User-Agent": USER_AGENT,
            "Accept": "application/json",
            "X-Auth-Token": context.get("auth_token"),
        }
        params["payload"] = json.dumps(
            {
                "name": context.get("image_name"),
                "disk_format": "iso",
                # "hw_rescue_bus": "ide",
                "hw_rescue_bus": "sata",
                "hw_rescue_device": "cdrom",
                "container_format": "bare",
            }
        ).encode("utf-8")
        return self.generate_request(params)

    @abstractmethod
    def generate_image_id(self, context):
        pass

    def upload_image_request(self, context):
        params = {}
        params[
            "url"
        ] = "https://image-service.c3j1.conoha.io/v2/images/{}/file".format(
            context.get("image_id")
        )
        params["method"] = "put"
        params["headers"] = {
            "User-Agent": USER_AGENT,
            "Accept": "*/*",
            "Content-Type": "application/octet-stream",
            "X-Auth-Token": context.get("auth_token"),
        }
        params["payload"] = open(context.get("iso_file"), "rb")
        return self.generate_request(params)

    @abstractmethod
    def upload_image(self, context):
        pass

    def delete_image_request(self, context):
        params = {}
        params[
            "url"
        ] = "https://image-service.c3j1.conoha.io/v2/images/{}".format(
            context.get("image_id")
        )
        params["method"] = "delete"
        params["headers"] = {
            "User-Agent": USER_AGENT,
            "Accept": "application/json",
            "X-Auth-Token": context.get("auth_token"),
        }
        params["payload"] = None
        return self.generate_request(params)

    @abstractmethod
    def delete_image(self, context):
        pass

    def list_server_request(self, context):
        params = {}
        params["url"] = "https://compute.c3j1.conoha.io/v2.1/servers"
        params["method"] = "get"
        params["headers"] = {
            "User-Agent": USER_AGENT,
            "Accept": "application/json",
            "X-Auth-Token": context.get("auth_token"),
        }
        params["payload"] = None
        return self.generate_request(params)

    @abstractmethod
    def list_server(self, context):
        pass

    def start_server_request(self, context):
        params = {}
        params[
            "url"
        ] = "https://compute.c3j1.conoha.io/v2.1/servers/{}/action".format(
            context.get("server_id")
        )
        params["method"] = "post"
        params["headers"] = {
            "User-Agent": USER_AGENT,
            "Accept": "application/json",
            "X-Auth-Token": context.get("auth_token"),
        }
        params["payload"] = json.dumps(
            {
                "os-start": None,
            }
        ).encode("utf-8")
        return self.generate_request(params)

    @abstractmethod
    def start_server(self, context):
        pass

    def stop_server_request(self, context):
        params = {}
        params[
            "url"
        ] = "https://compute.c3j1.conoha.io/v2.1/servers/{}/action".format(
            context.get("server_id")
        )
        params["method"] = "post"
        params["headers"] = {
            "User-Agent": USER_AGENT,
            "Accept": "application/json",
            "X-Auth-Token": context.get("auth_token"),
        }
        params["payload"] = json.dumps(
            {
                "os-stop": None,
            }
        ).encode("utf-8")
        return self.generate_request(params)

    @abstractmethod
    def stop_server(self, context):
        pass

    def stop_server_and_wait(self, context):
        context.set("server_status", None)
        self.get_server_status(context)
        while context.get("server_status") not in ["SHUTOFF"]:
            self.stop_server(context)
            print("waiting for shutdown...")
            time.sleep(10)
            self.get_server_status(context)
        print("server shutdown completed")

    def get_server_status_request(self, context):
        params = {}
        params[
            "url"
        ] = "https://compute.c3j1.conoha.io/v2.1/servers/{}".format(
            context.get("server_id")
        )
        params["method"] = "get"
        params["headers"] = {
            "User-Agent": USER_AGENT,
            "Accept": "application/json",
            "X-Auth-Token": context.get("auth_token"),
        }
        params["payload"] = None
        return self.generate_request(params)

    @abstractmethod
    def get_server_status(self, context):
        pass

    def get_server_console_request(self, context):
        params = {}
        params[
            "url"
        ] = "https://compute.c3j1.conoha.io/v2.1/servers/{}/remote-consoles".format(
            context.get("server_id")
        )
        params["method"] = "post"
        params["headers"] = {
            "User-Agent": USER_AGENT,
            "Accept": "application/json",
            "X-Auth-Token": context.get("auth_token"),
        }
        params["payload"] = json.dumps(
            {
                "remote_console": {
                    "protocol": "vnc",
                    "type": "novnc",
                }
            }
        ).encode("utf-8")
        return self.generate_request(params)

    @abstractmethod
    def get_server_console(self, context):
        pass

    def mount_image_request(self, context):
        params = {}
        params[
            "url"
        ] = "https://compute.c3j1.conoha.io/v2.1/servers/{}/action".format(
            context.get("server_id")
        )
        params["method"] = "post"
        params["headers"] = {
            "User-Agent": USER_AGENT,
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-Auth-Token": context.get("auth_token"),
        }
        params["payload"] = json.dumps(
            {
                "rescue": {
                    "rescue_image_ref": context.get("image_id"),
                },
            }
        ).encode("utf-8")
        return self.generate_request(params)

    @abstractmethod
    def mount_image(self, context):
        pass

    def unmount_image_request(self, context):
        params = {}
        params[
            "url"
        ] = "https://compute.c3j1.conoha.io/v2.1/servers/{}/action".format(
            context.get("server_id")
        )
        params["method"] = "post"
        params["headers"] = {
            "User-Agent": USER_AGENT,
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-Auth-Token": context.get("auth_token"),
        }
        params["payload"] = json.dumps(
            {
                "unrescue": None,
            }
        ).encode("utf-8")
        return self.generate_request(params)

    @abstractmethod
    def unmount_image(self, context):
        pass


class FakeConohaRestApi(RestApi):
    def generate_request(self, params):
        return params

    def generate_token(self, context):
        request = super().generate_token_request(context)
        print(str(request))
        context.set("auth_token", "fake-token")

    def generate_image_id(self, context):
        request = super().generate_image_id_request(context)
        print(str(request))
        context.set("image_id", "fake-image-id")

    def upload_image(self, context):
        request = super().upload_image_request(context)
        print(str(request))

    def delete_image(self, context):
        request = super().delete_image_request(context)
        print(str(request))

    def list_server(self, context):
        request = super().list_server_request(context)
        print(str(request))

    def start_server(self, context):
        request = super().start_server_request(context)
        print(str(request))

    def stop_server(self, context):
        request = super().stop_server_request(context)
        print(str(request))

    def get_server_status(self, context):
        request = super().get_server_status_request(context)
        print(str(request))
        context.set("server_status", "SHUTOFF")

    def get_server_console(self, context):
        request = super().get_server_console_request(context)
        print(str(request))
        print("http://127.0.0.1/")

    def list_image(self, context):
        request = super().list_image_request(context)
        print(str(request))

    def mount_image(self, context):
        request = super().mount_image_request(context)
        print(str(request))

    def unmount_image(self, context):
        request = super().unmount_image_request(context)
        print(str(request))


class ConohaRestApi(RestApi):
    def generate_request(self, params):
        request = Request(
            params["url"],
            data=params["payload"],
            headers=params["headers"],
            method=params["method"].upper(),
        )
        return request

    def generate_token(self, context):
        request = super().generate_token_request(context)
        with urlopen(request) as response:
            if response.status == 201:
                headers = response.headers
                key = "x-subject-token"
                context.set("auth_token", headers[key])
                print("auth_token: {}".format(headers[key]))
            else:
                print("{}: {}".format(response.status, response.reason))

    def list_image(self, context):
        request = super().list_image_request(context)
        with urlopen(request) as response:
            if response.status == 200:
                body = json.loads(response.read().decode("utf-8"))
                for image in body["images"]:
                    print(
                        "id: {} updated_at: {} name: {} status: {}".format(
                            image["id"],
                            image["updated_at"],
                            image["name"],
                            image["status"],
                        )
                    )
            else:
                print("{}: {}".format(response.status, response.reason))

    def generate_image_id(self, context):
        request = super().generate_image_id_request(context)
        with urlopen(request) as response:
            if response.status == 201:
                body = json.loads(response.read().decode("utf-8"))
                key = "id"
                context.set("image_id", body[key])
                print("id: {}".format(body[key]))
            else:
                print("{}: {}".format(response.status, response.reason))

    def upload_image(self, context):
        request = super().upload_image_request(context)
        with urlopen(request) as response:
            if response.status == 204:
                print("success")
            else:
                print("{}: {}".format(response.status, response.reason))

    def delete_image(self, context):
        request = super().delete_image_request(context)
        with urlopen(request) as response:
            if response.status == 204:
                print("success")
            else:
                print("{}: {}".format(response.status, response.reason))

    def list_server(self, context):
        request = super().list_server_request(context)
        with urlopen(request) as response:
            if response.status == 200:
                body = json.loads(response.read().decode("utf-8"))
                for server in body["servers"]:
                    server["id"]
                    print("id: {}".format(server["id"]))
            else:
                print("{}: {}".format(response.status, response.reason))

    def start_server(self, context):
        request = super().start_server_request(context)
        with urlopen(request) as response:
            if response.status == 202:
                print("success")
            else:
                print("{}: {}".format(response.status, response.reason))

    def stop_server(self, context):
        request = super().stop_server_request(context)
        with urlopen(request) as response:
            if response.status == 202:
                print("success")
            else:
                print("{}: {}".format(response.status, response.reason))

    def get_server_status(self, context):
        request = super().get_server_status_request(context)
        with urlopen(request) as response:
            if response.status == 200:
                body = json.loads(response.read().decode("utf-8"))
                server_status = body["server"]["status"]
                context.set("server_status", server_status)
                print("status: ", server_status)
            else:
                print("{}: {}".format(response.status, response.reason))

    def get_server_console(self, context):
        request = super().get_server_console_request(context)
        with urlopen(request) as response:
            if response.status == 200:
                body = json.loads(response.read().decode("utf-8"))
                url = body["remote_console"]["url"]
                print(url)
            else:
                print("{}: {}".format(response.status, response.reason))

    def mount_image(self, context):
        request = super().mount_image_request(context)
        with urlopen(request) as response:
            if response.status == 200:
                body = json.loads(response.read().decode("utf-8"))
                admin_pass = body["adminPass"]
                print("adminPass: {}".format(admin_pass))
            else:
                print("{}: {}".format(response.status, response.reason))

    def unmount_image(self, context):
        request = super().unmount_image_request(context)
        with urlopen(request) as response:
            if response.status == 202:
                print("success")
            else:
                print("{}: {}".format(response.status, response.reason))
