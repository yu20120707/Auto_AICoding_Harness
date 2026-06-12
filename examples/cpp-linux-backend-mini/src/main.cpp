#include "echo_server.h"

#include <iostream>

int main() {
    EchoServer server(9000);
    std::cout << server.BuildBanner() << '\n';
    return 0;
}
