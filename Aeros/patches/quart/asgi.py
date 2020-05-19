from quart.asgi import *
from quart.asgi import ASGIHTTPConnection as Original


class ASGIHTTPConnection(Original):

    async def handle_request(self, request: Request, send: Callable) -> None:
        try:
            response = await self.app.handle_request(request)
        except Exception:
            response = await traceback_response()

        timeout = self.app.config["RESPONSE_TIMEOUT"]
        try:
            await asyncio.wait_for(self._send_response(send, response), timeout=timeout)
        except asyncio.TimeoutError:
            pass
