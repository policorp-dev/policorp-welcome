#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <crypt.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

void change_root_password(const char* password) {
    char command[256];
    snprintf(command, sizeof(command), "sudo /usr/sbin/usermod -p $(mkpasswd -m sha-512 '%s') root", password);
    if (system(command) == 0) {
        int fd = open("/opt/.setted-pass", O_CREAT | O_WRONLY, 0644);
        if (fd != -1) {
            close(fd);
        } else {
            perror("Erro criando /opt/.setted-pass");
        }
    } else {
        fprintf(stderr, "Falha em mudar senha root \n");
    }
}

void change_user_password(const char* user, const char* password) {
    char command[256];
    snprintf(command, sizeof(command), "sudo passwd -d %s", user);
    if (system(command) == 0) {
        snprintf(command, sizeof(command), "echo '%s:%s' | sudo chpasswd", user, password);
        if (system(command) != 0) {
            fprintf(stderr, "Falha para mudar password do usuario %s\n", user);
        }
    } else {
        fprintf(stderr, "Falha em deletar a senha usuario atual  %s\n", user);
    }
}

int main(int argc, char *argv[]) {
    if (argc < 3) {
        fprintf(stderr, "Usage: %s <password> <user> [change_user_password]\n", argv[0]);
        return 1;
    }

    const char* password = argv[1];
    const char* user = argv[2];
    int change_user_pass = (argc > 3 && strcmp(argv[3], "True") == 0);

    change_root_password(password);

    if (change_user_pass) {
        change_user_password(user, password);
    }

    return 0;
}
