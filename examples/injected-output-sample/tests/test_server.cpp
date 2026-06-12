#include "server.h"

#include <cstdlib>

int main() {
    Server server(8080);
    if (server.port() != 8080) {
        return EXIT_FAILURE;
    }
    if (server.Describe() != "sample-server:8080") {
        return EXIT_FAILURE;
    }
    return EXIT_SUCCESS;
}
