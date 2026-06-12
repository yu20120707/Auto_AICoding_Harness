#pragma once

#include <string>

class EchoServer {
public:
    explicit EchoServer(int port);

    int port() const noexcept;
    std::string BuildBanner() const;

private:
    int port_;
};
