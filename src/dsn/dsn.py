#
# DSN
#
from __future__ import annotations

from typing import Optional
from urllib.parse import urlparse


class DSN():

    """DSNを表すクラス。

    DSNフォーマット: scheme://user:pass@host:port/path/to/transport
    最小構成: scheme://host/path

    Attributes:
        scheme (str): スキーム、またはプロトコル名
        user (Optional[str]): ユーザ名
        password (Optional[str]): パスワード
        host (str): ホスト名
        port (Optional[int]): ポート番号
        path (str): パス

    """

    def __init__(self, scheme: str, user: Optional[str], password: Optional[str], host: str, port: Optional[int], path: str) -> None:
        if None in [scheme, host, path]:
            raise ValueError(
                "failed to instantiate DSN Object with args: scheme, host, path must not be None.")

        self.scheme: str = scheme
        self.user: Optional[str] = user
        self.password: Optional[str] = password
        self.host: str = host
        self.port: Optional[int] = port
        self.path: str = path

    def __str__(self) -> str:
        """DSNの文字列表現を返します。

        Returns:
            str: インスタンスの文字列表現。

        Note:
            DSNの文字列表現は正しいURLであることを保証しません。
            URLの形式で値を取得したい場合は `DSN.url()` を使用してください。

        """

        return f"{self.scheme}://{self.user or '(None)'}:{self.password or '(None)'}@{self.host}:{self.port or '(None)'}{self.path}"

    def url(self) -> str:
        """DSNのURL表現を返します。

        Returns:
            str: インスタンスのURL表現。

        Raises:
            ValueError: DSNをURLとして表現できない場合。

        Note:
            DSNには最低限 scheme, hostの値が必要です。
            これらが与えられていないインスタンスにこの関数を呼び出すと、
            ValueErrorが送出されます。

        """

        # スキームとホストは最低限
        if "" in [self.scheme, self.host]:
            raise ValueError(
                "This DSN object cannot be converted to a valid URL.")

        # netlocを生成
        netloc = self.host

        # ポートが正しい値で追加されていればnetlocに追加
        if (self.port is not None) and (0 <= self.port and self.port <= 65535):
            netloc = f"{netloc}:{self.port}"

        # ユーザ, パスワードは両方空文字でない場合のみ追加
        user, password = self.user or "", self.password or ""
        if user != "" and password != "":
            netloc = f"{user}:{password}@{netloc}"

        return f"{self.scheme}://{netloc}{self.path}"

    @staticmethod
    def parsefrom(dsnstring: str) -> Optional[DSN]:
        """文字列からDSNインスタンスを生成します。

        Args:
            dsnstring(str): パース対象のDSN文字列。

        Returns:
            Optional[DSN]: パースして生成されたDSNインスタンス。生成に失敗した場合はNoneが返ります。

        """

        try:
            parsed_dsn = urlparse(dsnstring)

            if parsed_dsn.hostname is None:
                raise ValueError("Invalid DSN")

            return DSN(parsed_dsn.scheme, parsed_dsn.username, parsed_dsn.password, parsed_dsn.hostname, parsed_dsn.port, parsed_dsn.path)
        except ValueError:
            return None
