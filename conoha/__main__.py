import argparse
import tomllib
from pathlib import Path

from conoha.command import (
    CompositeCommand,
    Context,
    DeleteImage,
    GenerateImageId,
    GenerateToken,
    GetServerConsole,
    GetServerStatus,
    ListImage,
    ListServer,
    LoadSecret,
    LoadToken,
    MountImage,
    SaveSecret,
    StartServer,
    StopServerAndWait,
    UnmountImage,
    UploadImage,
)
from conoha.conoha import ConohaRestApi, FakeConohaRestApi


def version_template():
    project_metadata = Path(__file__).parent.parent.joinpath("pyproject.toml")
    with open(project_metadata, mode="rb") as metadata:
        version_number = tomllib.load(metadata)["tool"]["poetry"]["version"]
        return "%(prog)s {}".format(version_number)


def generate_token(api, args):
    context = Context(args)
    command = CompositeCommand()
    command.append(LoadSecret())
    command.append(GenerateToken(force=True))
    command.append(SaveSecret())
    command.execute(api, context)


def list_server(api, args):
    context = Context(args)
    command = CompositeCommand()
    command.append(LoadToken())
    command.append(ListServer())
    command.execute(api, context)


def start_server(api, args):
    context = Context(args)
    command = CompositeCommand()
    command.append(LoadToken())
    command.append(StartServer())
    command.execute(api, context)


def stop_server(api, args):
    context = Context(args)
    command = CompositeCommand()
    command.append(LoadToken())
    command.append(StopServerAndWait())
    command.execute(api, context)


def get_server_status(api, args):
    context = Context(args)
    command = CompositeCommand()
    command.append(LoadToken())
    command.append(GetServerStatus())
    command.execute(api, context)


def get_server_console(api, args):
    context = Context(args)
    command = CompositeCommand()
    command.append(LoadToken())
    command.append(GetServerConsole())
    command.execute(api, context)


def list_image(api, args):
    context = Context(args)
    command = CompositeCommand()
    command.append(LoadToken())
    command.append(ListImage())
    command.execute(api, context)


def generate_image(api, args):
    context = Context(args)
    command = CompositeCommand()
    command.append(LoadToken())
    command.append(GenerateImageId())
    command.execute(api, context)


def upload_image(api, args):
    context = Context(args)
    command = CompositeCommand()
    command.append(LoadToken())
    command.append(UploadImage())
    command.execute(api, context)


def delete_image(api, args):
    context = Context(args)
    command = CompositeCommand()
    command.append(LoadToken())
    command.append(DeleteImage())
    command.execute(api, context)


def mount_image(api, args):
    context = Context(args)
    command = CompositeCommand()
    command.append(LoadToken())
    command.append(StopServerAndWait())
    command.append(MountImage())
    command.append(GetServerStatus())
    command.execute(api, context)


def unmount_image(api, args):
    context = Context(args)
    command = CompositeCommand()
    command.append(LoadToken())
    command.append(UnmountImage())
    command.append(GetServerStatus())
    command.execute(api, context)


def create_parser():
    formatter = argparse.ArgumentDefaultsHelpFormatter
    parser = argparse.ArgumentParser(prog="conoha", formatter_class=formatter)
    parser.add_argument(
        "--pretend",
        help="テスト実行します",
    )
    subparsers = parser.add_subparsers(required=True)

    # token
    token_parser = subparsers.add_parser(
        "token",
        help="トークン関連",
    )
    token_subparser = token_parser.add_subparsers(required=True)

    # generate
    generate_token_parser = token_subparser.add_parser(
        "generate",
        help="トークンを生成します",
        formatter_class=formatter,
    )
    generate_token_parser.set_defaults(func=generate_token)
    generate_token_parser.add_argument(
        "--secret",
        help="トークンファイル",
    )
    generate_token_parser.add_argument(
        "--user-id",
        help="ConoHa VPS API ユーザID",
    )
    generate_token_parser.add_argument(
        "--password",
        help="ConoHa VPS API パスワード",
    )
    generate_token_parser.add_argument(
        "--tenant-id",
        help="ConoHa VPS テナントID",
    )

    # server
    server_parser = subparsers.add_parser(
        "server",
        help="サーバ関連",
    )
    server_subparser = server_parser.add_subparsers(required=True)

    ## list
    list_server_parser = server_subparser.add_parser(
        "list",
        help="サーバを一覧表示します",
        formatter_class=formatter,
    )
    list_server_parser.set_defaults(func=list_server)
    list_server_parser.add_argument(
        "--secret",
        help="トークンファイル",
    )
    list_server_parser.add_argument(
        "--auth-token",
        help="トークン",
    )
    list_server_parser.add_argument(
        "--user-id",
        help="ConoHa VPS API ユーザID",
    )
    list_server_parser.add_argument(
        "--password",
        help="ConoHa VPS API パスワード",
    )
    list_server_parser.add_argument(
        "--tenant-id",
        help="ConoHa VPS テナントID",
    )

    ## start
    start_server_parser = server_subparser.add_parser(
        "start",
        help="サーバを起動します",
        formatter_class=formatter,
    )
    start_server_parser.set_defaults(func=start_server)
    start_server_parser.add_argument(
        "--secret",
        help="トークンファイル",
    )
    start_server_parser.add_argument(
        "--auth-token",
        help="トークン",
    )
    start_server_parser.add_argument(
        "--user-id",
        help="ConoHa VPS API ユーザID",
    )
    start_server_parser.add_argument(
        "--password",
        help="ConoHa VPS API パスワード",
    )
    start_server_parser.add_argument(
        "--tenant-id",
        help="ConoHa VPS テナントID",
    )
    start_server_parser.add_argument(
        "--server-id",
        required=True,
        help="サーバID",
    )

    ## stop
    stop_server_parser = server_subparser.add_parser(
        "stop",
        help="サーバを停止します",
        formatter_class=formatter,
    )
    stop_server_parser.set_defaults(func=stop_server)
    stop_server_parser.add_argument(
        "--secret",
        help="トークンファイル",
    )
    stop_server_parser.add_argument(
        "--auth-token",
        help="トークン",
    )
    stop_server_parser.add_argument(
        "--user-id",
        help="ConoHa VPS API ユーザID",
    )
    stop_server_parser.add_argument(
        "--password",
        help="ConoHa VPS API パスワード",
    )
    stop_server_parser.add_argument(
        "--tenant-id",
        help="ConoHa VPS テナントID",
    )
    stop_server_parser.add_argument(
        "--server-id",
        required=True,
        help="サーバID",
    )

    ## status
    get_server_status_parser = server_subparser.add_parser(
        "status",
        help="サーバのステータスを確認します",
        formatter_class=formatter,
    )
    get_server_status_parser.set_defaults(func=get_server_status)
    get_server_status_parser.add_argument(
        "--secret",
        help="トークンファイル",
    )
    get_server_status_parser.add_argument(
        "--auth-token",
        help="トークン",
    )
    get_server_status_parser.add_argument(
        "--user-id",
        help="ConoHa VPS API ユーザID",
    )
    get_server_status_parser.add_argument(
        "--password",
        help="ConoHa VPS API パスワード",
    )
    get_server_status_parser.add_argument(
        "--tenant-id",
        help="ConoHa VPS テナントID",
    )
    get_server_status_parser.add_argument(
        "--server-id",
        required=True,
        help="サーバID",
    )

    ## console
    get_server_console_parser = server_subparser.add_parser(
        "console",
        help="サーバのコンソールアクセスURLを確認します",
        formatter_class=formatter,
    )
    get_server_console_parser.set_defaults(func=get_server_console)
    get_server_console_parser.add_argument(
        "--secret",
        help="トークンファイル",
    )
    get_server_console_parser.add_argument(
        "--auth-token",
        help="トークン",
    )
    get_server_console_parser.add_argument(
        "--user-id",
        help="ConoHa VPS API ユーザID",
    )
    get_server_console_parser.add_argument(
        "--password",
        help="ConoHa VPS API パスワード",
    )
    get_server_console_parser.add_argument(
        "--tenant-id",
        help="ConoHa VPS テナントID",
    )
    get_server_console_parser.add_argument(
        "--server-id",
        required=True,
        help="サーバID",
    )

    # image
    image_parser = subparsers.add_parser(
        "image", help="ISOイメージ関連", formatter_class=formatter
    )
    image_subparser = image_parser.add_subparsers(required=True)

    ## list
    list_image_parser = image_subparser.add_parser(
        "list",
        help="イメージを一覧表示します",
        formatter_class=formatter,
    )
    list_image_parser.set_defaults(func=list_image)
    list_image_parser.add_argument(
        "--secret",
        help="トークンファイル",
    )
    list_image_parser.add_argument(
        "--auth-token",
        help="トークン",
    )
    list_image_parser.add_argument(
        "--user-id",
        help="ConoHa VPS API ユーザID",
    )
    list_image_parser.add_argument(
        "--password",
        help="ConoHa VPS API パスワード",
    )
    list_image_parser.add_argument(
        "--tenant-id",
        help="ConoHa VPS テナントID",
    )

    ## generate
    generate_image_parser = image_subparser.add_parser(
        "generate",
        help="イメージIDを作成します",
        formatter_class=formatter,
    )
    generate_image_parser.set_defaults(func=generate_image)
    generate_image_parser.add_argument(
        "--secret",
        help="トークンファイル",
    )
    generate_image_parser.add_argument(
        "--auth-token",
        help="トークン",
    )
    generate_image_parser.add_argument(
        "--user-id",
        help="ConoHa VPS API ユーザID",
    )
    generate_image_parser.add_argument(
        "--password",
        help="ConoHa VPS API パスワード",
    )
    generate_image_parser.add_argument(
        "--tenant-id",
        help="ConoHa VPS テナントID",
    )
    generate_image_parser.add_argument(
        "--image-name",
        required=True,
        help="イメージ名",
    )

    ## delete
    delete_image_parser = image_subparser.add_parser(
        "delete",
        help="イメージを削除します",
        formatter_class=formatter,
    )
    delete_image_parser.set_defaults(func=delete_image)
    delete_image_parser.add_argument(
        "--secret",
        help="トークンファイル",
    )
    delete_image_parser.add_argument(
        "--auth-token",
        help="トークン",
    )
    delete_image_parser.add_argument(
        "--user-id",
        help="ConoHa VPS API ユーザID",
    )
    delete_image_parser.add_argument(
        "--password",
        help="ConoHa VPS API パスワード",
    )
    delete_image_parser.add_argument(
        "--tenant-id",
        help="ConoHa VPS テナントID",
    )
    delete_image_parser.add_argument(
        "--image-id",
        required=True,
        help="イメージID",
    )

    ## upload
    upload_image_parser = image_subparser.add_parser(
        "upload",
        help="ISOイメージをアップロードします",
        formatter_class=formatter,
    )
    upload_image_parser.set_defaults(func=upload_image)
    upload_image_parser.add_argument(
        "--secret",
        help="トークンファイル",
    )
    upload_image_parser.add_argument(
        "--auth-token",
        help="トークン",
    )
    upload_image_parser.add_argument(
        "--user-id",
        help="ConoHa VPS API ユーザID",
    )
    upload_image_parser.add_argument(
        "--password",
        help="ConoHa VPS API パスワード",
    )
    upload_image_parser.add_argument(
        "--tenant-id",
        help="ConoHa VPS テナントID",
    )
    upload_image_parser.add_argument(
        "--image-id",
        required=True,
        help="イメージID",
    )
    upload_image_parser.add_argument(
        "--iso-file",
        required=True,
        help="ISO ファイル",
    )

    ## mount
    mount_image_parser = image_subparser.add_parser(
        "mount",
        help="イメージをマウントします",
        formatter_class=formatter,
    )
    mount_image_parser.set_defaults(func=mount_image)
    mount_image_parser.add_argument(
        "--secret",
        help="トークンファイル",
    )
    mount_image_parser.add_argument(
        "--auth-token",
        help="トークン",
    )
    mount_image_parser.add_argument(
        "--user-id",
        help="ConoHa VPS API ユーザID",
    )
    mount_image_parser.add_argument(
        "--password",
        help="ConoHa VPS API パスワード",
    )
    mount_image_parser.add_argument(
        "--tenant-id",
        help="ConoHa VPS テナントID",
    )
    mount_image_parser.add_argument(
        "--server-id",
        required=True,
        help="サーバID",
    )
    mount_image_parser.add_argument(
        "--image-id",
        required=True,
        help="イメージID",
    )

    ## unmount
    unmount_image_parser = image_subparser.add_parser(
        "unmount",
        help="イメージをアンマウントします",
        formatter_class=formatter,
    )
    unmount_image_parser.set_defaults(func=unmount_image)
    unmount_image_parser.add_argument(
        "--secret",
        help="トークンファイル",
    )
    unmount_image_parser.add_argument(
        "--auth-token",
        help="トークン",
    )
    unmount_image_parser.add_argument(
        "--user-id",
        help="ConoHa VPS API ユーザID",
    )
    unmount_image_parser.add_argument(
        "--password",
        help="ConoHa VPS API パスワード",
    )
    unmount_image_parser.add_argument(
        "--tenant-id",
        help="ConoHa VPS テナントID",
    )
    unmount_image_parser.add_argument(
        "--server-id",
        required=True,
        help="サーバID",
    )

    return parser


if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()
    func = args.func.__name__

    if func == "generate_token":
        if args.secret is None:
            if (
                args.user_id is None
                or args.password is None
                or args.tenant_id is None
            ):
                parser.error("トークンファイル又はユーザID, パスワード, テナントIDを指定して下さい")
    else:
        if args.secret is None and args.auth_token is None:
            if (
                args.user_id is None
                or args.password is None
                or args.tenant_id is None
            ):
                parser.error("トークンファイル、トークン又はユーザID, パスワード, テナントIDを指定して下さい")

    if args.pretend:
        api = FakeConohaRestApi()
    else:
        api = ConohaRestApi()

    args.func(api, args)
