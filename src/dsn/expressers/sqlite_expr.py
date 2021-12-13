#
# SQLite DSN Expresser
#
from src.dsn import DSN
from urllib.parse import urlunparse

from .base_expr import Base


class SQLiteExpresser(Base):

    """ SQLiteのExpresser """

    __pattern__: str = "^sqlite$"

    @staticmethod
    def urlexpr(dsn: DSN) -> str:

        # sqlite://<nohost>/<database_path>

        # user, pass, host, portは全部Noneか空文字であってほしい
        user = dsn.user or ""
        password = dsn.password or ""
        host = dsn.host or ""
        port = dsn.port or ""

        if not ("" in [user, password, host, port]):
            raise ValueError("convert failed: SQLite user, password, host, port must be blank or None")

        # pathが空文字だとアウト
        if dsn.path == "":
            raise ValueError("convert failed: path must not be None or blank")

        # urlunparseで戻す
        return urlunparse((dsn.scheme, "", dsn.path, dsn.params, dsn.query, dsn.fragment))
