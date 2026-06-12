#include "server.h"

#include <sstream>

Server::Server(int port) : port_(port) {}

int Server::port() const noexcept {
    return port_;
}

std::string Server::Describe() const {
    std::ostringstream buffer;
    buffer << "sample-server:" << port_;
    return buffer.str();
}
