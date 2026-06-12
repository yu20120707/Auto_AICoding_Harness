#include "echo_server.h"

#include <sstream>

EchoServer::EchoServer(int port) : port_(port) {}

int EchoServer::port() const noexcept {
    return port_;
}

std::string EchoServer::BuildBanner() const {
    std::ostringstream buffer;
    buffer << "echo-server listening on :" << port_;
    return buffer.str();
}
