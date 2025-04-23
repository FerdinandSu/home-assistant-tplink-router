from logging import Logger


from .common.exception import ClientException
from .client.c6u import TplinkRouter
from .client.deco import TPLinkDecoClient
from .client_abstract import AbstractRouter
from .client.mr import TPLinkMRClient
from .client.ex import TPLinkEXClient
from .client.c5400x import TplinkC5400XRouter
from .client.c1200 import TplinkC1200Router
from .client.c80 import TplinkC80Router
from .client.vr import TPLinkVRClient
from .client.xdr import TPLinkXDRClient
from .client.wdr import TplinkWDRRouter


class TplinkRouterProvider:
    @staticmethod
    def get_client(host: str, password: str, username: str = 'admin', logger: Logger = None,
                   verify_ssl: bool = True, timeout: int = 30) -> AbstractRouter:
        for client in [TPLinkVRClient, TPLinkEXClient, TPLinkMRClient, TPLinkDecoClient,
                       TPLinkXDRClient, TplinkRouter, TplinkC80Router, TplinkWDRRouter, TplinkC5400XRouter]:
            router = client(host, password, username, logger, verify_ssl, timeout)
            if router.supports():
                return router

        message = ('Login failed! Please check if your router local password is correct or '
                   'try to use web encrypted password instead. Check the documentation!')
        router = TplinkC1200Router(host, password, username, logger, verify_ssl, timeout)
        try:
            router.authorize()
            return router
        except Exception:
            pass

        for client in [TPLinkVRClient, TPLinkXDRClient]:
            router = client(host, password, username, None, verify_ssl, timeout)
            try:
                router.authorize()
                message = ('Your router might be supported by {}. Please open the issue here '
                           'https://github.com/AlexandrErohin/TP-Link-Archer-C6U').format(router.__class__)
                break
            except Exception:
                pass

        raise ClientException(message)
