#pragma once

#include <string>

class Server {
public:
    explicit Server(int port);

    int port() const noexcept;
    std::string Describe() const;

private:
    int port_;
};
