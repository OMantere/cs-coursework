# Round 3 Part B 

In this assignment we had a C program with a buffer overflow vulnerability. The vulnerability is on the line 35, ```sprintf(msg, "%s%s", command_rec, username);```, where the length of ```command_rec``` is left unchecked, allowing us to overwrite ```key```. 

Compiling the given source with GDB and observing the stack we notice ```key``` is at ESP+64 on the stack. ```msg``` is at ESP+48. Putting 32 A's into the message field overwrites all bytes of the 16-bit key with 0x41.

I then added a line just before the MAC check to print out the MAC encoded with our key. Putting this in the "HMAC"-field and 32 A's in the "Command"-field gives us access. 

*Modifications I made to the code during the assignment:*

~~~~
#include <string.h>
#include <openssl/evp.h>
#include <openssl/hmac.h>

#define MSG_LEN 9 
#define KEY_LEN 16 
#define HMAC_LEN 20 
#define USERNAME_LEN 6 

void process(char *command_rec, char *username, char *hmac_rec) { 
    /* key used to compute message authentication code (MAC) below value in hexadecimal. 
     * NOTE: THIS IS NOT THE REAL KEY THE SERVER USES! 
     */ 
    unsigned char key[KEY_LEN] = 
    {0xff, 0xff, 0xff, 0xff, 
        0x00, 0x00, 0x00, 0x00, 
        0xff, 0xff, 0xff, 0xff, 
        0x00, 0x00, 0x00, 0x00}; 

    char msg[MSG_LEN] = {0}; 
    int i; 
    unsigned char *hmac; 
    char hex_hmac[HMAC_LEN*2]; 

    // check if length of hex HMAC is 20*2 
    if (strlen(hmac_rec) != HMAC_LEN*2) { 
        printf("%s\n", "HMAC_INVALID"); 
    } 

    if (strlen(username) != USERNAME_LEN) { 
        printf("%s\n", "USERNAME_INVALID"); 
    } 

    /* concatenate command and username */ 
    sprintf(msg, "%s%s", command_rec, username); 

    printf("%s\n", key);

    hmac = HMAC(EVP_sha1(), key, KEY_LEN, (const unsigned char *) msg, (int) strlen(msg), NULL, NULL); 


    /* Hexadecimal representation of HMAC computed above */ 
    for (i=0; i<HMAC_LEN; i++) { 
        sprintf(hex_hmac+i*2, "%02x", hmac[i]); 
    } 

    printf("HMAC: %s\n", hex_hmac);

    /* check if MAC is correct */ 
    if (!memcmp(hex_hmac, hmac_rec, HMAC_LEN*2)) { 
        printf("%s\n", "A");
    } else { 
        printf("%s\n", "U");
    } 
} 

int main(int argc, char* argv[]) {
    process(argv[1], argv[2], argv[3]);
    return 0;
}
~~~~ 
