from hypercorn.config import Config as OriginalConfig
from hypercorn.config import format_date_time, List, Tuple, time, Dict


class Config(OriginalConfig):
    def __init__(self, custom_headers: Dict[str, str], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__custom_headers = custom_headers

    def response_headers(self, protocol: str) -> List[Tuple[bytes, bytes]]:
        """ This function is patched to include custom headers, which will
         be sent in every response. For example to send a custom "server"
         header or CORS headers all the time. """

        headers = [(b"date", format_date_time(time()).encode("ascii"))]
        if self.include_server_header:
            headers.append((b"server", f"hypercorn-{protocol}".encode("ascii")))

        for alt_svc_header in self.alt_svc_headers:
            headers.append((b"alt-svc", alt_svc_header.encode()))
        if len(self.alt_svc_headers) == 0 and self._quic_bind:
            from aioquic.h3.connection import H3_ALPN

            for version in H3_ALPN:
                for bind in self._quic_bind:
                    port = int(bind.split(":")[-1])
                    headers.append((b"alt-svc", b'%s=":%d"; ma=3600' % (version.encode(), port)))

        for header, value in self.__custom_headers.items():
            headers.append((header.encode("ascii"), value.encode("ascii")))

        return headers
