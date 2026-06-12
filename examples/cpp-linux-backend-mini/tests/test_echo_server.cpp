#include "echo_server.h"

#include <cstdlib>

int main() {
    EchoServer server(9000);
    if (server.port() != 9000) {
        return EXIT_FAILURE;
    }
    if (server.BuildBanner() != "echo-server listening on :9000") {
        return EXIT_FAILURE;
    }
    return EXIT_SUCCESS;
}
