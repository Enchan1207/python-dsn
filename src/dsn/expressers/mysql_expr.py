#
# MySQL DSN Expresser
#
from src.dsn import DSN
from urllib.parse import urlunparse

from .base_expr import Base


class MySQLExpresser(Base):

    """ MySQLのExpresser """

    __pattern__: str = "^mysql\+*.*$"

    @staticmethod
    def urlexpr(dsn: DSN) -> str:

        # mysql://<user>:<password>@<host>:<port>/<database_path>?<options>

        # 最低限 user, host は必要
        if dsn.user is None or dsn.host is None:
            raise ValueError("convert failed: MySQL requires user, host but includes None")

        # pathが空文字なのもアウト
        if dsn.path == "":
            raise ValueError("convert failed: path must not be None or blank")

        # netlocを生成

        # ログインクレデンシャル部分
        login_credential = dsn.user
        if (dsn.password or "") != "":
            login_credential += f":{dsn.password}"

        # サーバ・ポート部分
        serverloc = dsn.host
        if dsn.port is not None:
            serverloc += f":{dsn.port}"

        netloc = f"{login_credential}@{serverloc}"

        # urlunparseで戻す
        return urlunparse((dsn.scheme, netloc, dsn.path, dsn.params, dsn.query, dsn.fragment))
