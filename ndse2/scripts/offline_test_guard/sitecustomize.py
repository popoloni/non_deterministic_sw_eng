"""Test-only network guard, inherited by child Python interpreters; not an OS sandbox."""
import socket
def blocked(*args, **kwargs):
    raise RuntimeError("NETWORK_DISABLED_FOR_V10_TESTS")
socket.create_connection = blocked
class OfflineSocket(socket.socket):
    connect = blocked
    connect_ex = blocked
    sendto = blocked
socket.socket = OfflineSocket
