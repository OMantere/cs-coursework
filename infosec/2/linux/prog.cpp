#include <stdlib.h>
#include <pwd.h>
#include <stdio.h>
#include <stdarg.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <string.h>

void exec_child(const char *path, ...) {
	pid_t parent = getpid();
	pid_t pid = fork();

	if (pid == -1)
	{
		// error, failed to fork()
	} 
	else if (pid > 0)
	{
		wait(NULL);
	}

	else 
	{
		// we are the child
        va_list ap;
		va_start(ap, path);
		char* argv[5];
		char* arg;
		for(int i = 0; i < 5; i++) {
			argv[i] = NULL;
		}

		int i = 0;
		while(arg = va_arg(ap, char*))
		{
			printf("%s \n", arg);
			argv[i] = arg;
			i++;
		}
		va_end(ap);
		execv(path, argv);
		_exit(EXIT_FAILURE);   // exec never returns
	}
}

int main(int argc, char* argv[]) {
    struct passwd *p = getpwuid(geteuid());
    char *user = getenv("USER");
    if(strcmp(p->pw_name, "root")) {
        printf("This file needs to be suid root. \n");
        return 1;
    }
    exec_child("/bin/mkdir", "mkdir", "assignment", NULL);
    exec_child("/bin/mkdir", "mkdir", "assignment/confidential", NULL);
    exec_child("/usr/sbin/lgroupadd", "lgroupadd", "project2016", NULL);
    exec_child("/usr/sbin/lgroupmod", "lgroupadd", "-M", user, "project2016", NULL);
    exec_child("/bin/chown", "chown", "-R", user, "assignment", NULL);
    exec_child("/bin/chgrp", "chgrp", "-R", "project2016", "assignment", NULL);
    exec_child("/bin/chmod", "chmod", "770", "assignment", NULL);
    exec_child("/bin/chmod", "chmod", "700", "assignment/confidential", NULL);
    return 0;
}
