#
# MIT License
#
# Copyright (c) 2026 Sonardyne International Limited
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
from abc import ABC, abstractmethod
import socket
import serial
import select
from typing import Optional

class CommunicationInterface(ABC):
    """Abstract Base Class defining the unified communication interface."""

    @abstractmethod
    def open(self) -> None:
        """Establish the connection or initialize the socket/port."""
        pass

    @abstractmethod
    def close(self) -> None:
        """Terminate the connection and free up system resources."""
        pass

    @abstractmethod
    def send(self, data: bytes) -> None:
        """Transmit binary data over the connection."""
        pass

    @abstractmethod
    def receive(self, buffer_size: int, timeout: Optional[float] = None) -> bytes:
        """Receive binary data up to the specified buffer size with an optional timeout in seconds."""
        pass

class TcpClient(CommunicationInterface):
    """TCP Client for point-to-point stream connections."""
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self._socket = None

    def open(self) -> None:
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((self.host, self.port))

    def close(self) -> None:
        if self._socket:
            self._socket.close()
            self._socket = None

    def send(self, data: bytes) -> None:
        if not self._socket:
            raise RuntimeError("Connection is not open.")
        self._socket.sendall(data)

    def receive(self, buffer_size: int, timeout: Optional[float] = None) -> bytes:
        if not self._socket:
            raise RuntimeError("Connection is not open.")

        # Temporarily alter socket timeout if provided
        try:
            ready = select.select([self._socket], [], [], timeout)
            if ready[0]:
                return self._socket.recv(buffer_size)
            else:
                raise TimeoutError("TCP receive operation timed out.")
        except socket.timeout:
            raise TimeoutError("TCP receive operation timed out.")


class TcpServer(CommunicationInterface):
    """TCP Server that handles a single client connection at a time."""
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self._server_socket = None
        self._client_socket = None

    def open(self) -> None:
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server_socket.bind((self.host, self.port))
        self._server_socket.listen(1)
        self._client_socket, _ = self._server_socket.accept()

    def close(self) -> None:
        if self._client_socket:
            self._client_socket.close()
            self._client_socket = None
        if self._server_socket:
            self._server_socket.close()
            self._server_socket = None

    def send(self, data: bytes) -> None:
        if not self._client_socket:
            raise RuntimeError("No client connected.")
        self._client_socket.sendall(data)

    def receive(self, buffer_size: int, timeout: Optional[float] = None) -> bytes:
        if not self._client_socket:
            raise RuntimeError("No client connected.")

        original_timeout = self._client_socket.gettimeout()
        try:
            if timeout is not None:
                self._client_socket.settimeout(timeout)
            return self._client_socket.recv(buffer_size)
        except socket.timeout:
            raise TimeoutError("TCP server receive operation timed out.")
        finally:
            if timeout is not None:
                self._client_socket.settimeout(original_timeout)


class UdpSocket(CommunicationInterface):
    """UDP Socket handling connectionless datagram communication."""
    def __init__(self, local_port: int, remote_host: str = None, remote_port: int = None):
        self.local_port = local_port
        self.remote_host = remote_host
        self.remote_port = remote_port
        self._socket = None

    def open(self) -> None:
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket.bind(("", self.local_port))

    def close(self) -> None:
        if self._socket:
            self._socket.close()
            self._socket = None

    def send(self, data: bytes) -> None:
        if not self._socket:
            raise RuntimeError("Socket is not open.")
        if not self.remote_host or not self.remote_port:
            raise ValueError("Remote host and port must be specified to send data.")
        self._socket.sendto(data, (self.remote_host, self.remote_port))

    def receive(self, buffer_size: int, timeout: Optional[float] = None) -> bytes:
        if not self._socket:
            raise RuntimeError("Socket is not open.")

        original_timeout = self._socket.gettimeout()
        try:
            if timeout is not None:
                self._socket.settimeout(timeout)
            data, _ = self._socket.recvfrom(buffer_size)
            return data
        except socket.timeout:
            raise TimeoutError("UDP receive operation timed out.")
        finally:
            if timeout is not None:
                self._socket.settimeout(original_timeout)


class SerialPort(CommunicationInterface):
    """Serial Port wrapper targeting hardware devices via PySerial."""
    def __init__(self, port: str, baudrate: int = 9600, timeout: float = None):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout  # Default fallback timeout
        self._serial = None

    def open(self) -> None:
        self._serial = serial.Serial(port=self.port, baudrate=self.baudrate, timeout=self.timeout)

    def close(self) -> None:
        if self._serial and self._serial.is_open:
            self._serial.close()
            self._serial = None

    def send(self, data: bytes) -> None:
        if not self._serial or not self._serial.is_open:
            raise RuntimeError("Serial port is not open.")
        self._serial.write(data)

    def receive(self, buffer_size: int, timeout: Optional[float] = None) -> bytes:
        if not self._serial or not self._serial.is_open:
            raise RuntimeError("Serial port is not open.")

        # Only change the timeout when it differs, as on Windows every change
        # reconfigures the port, which disrupts the link when called in a loop
        if timeout is not None and timeout != self._serial.timeout:
            self._serial.timeout = timeout

        data = self._serial.read(buffer_size)

        # PySerial returns less/no data on timeout instead of throwing an exception
        if len(data) == 0 and buffer_size > 0:
            raise TimeoutError("Serial read operation timed out.")
        return data