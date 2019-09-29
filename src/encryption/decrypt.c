#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <stdint.h>

// Enable ECB, CTR and CBC mode. Note this can be done before including aes.h or at compile-time.
// E.g. with GCC by using the -D flag: gcc -c aes.c -DCBC=0 -DCTR=1 -DECB=1

#include "aes.h"

uint8_t* decrypt (const uint8_t* str_to_decrypt){

    uint8_t* u_decrypted = (uint8_t*) malloc (64*sizeof(uint8_t));
    
    memcpy(u_decrypted, str_to_decrypt, 64);

    //Should import key from somewhere, but here it will be hard coded.
    uint8_t key[] = { 0x45, 0xa2, 0x78, 0x22, 0x3e, 0xaf, 0xe4, 0xc2, 0xac, 0x8f, 0x15, 0xf4, 0xee, 0xa8, 0x5b, 0x2a };
    //iv is the initialization vector, a random vector that initializes the chain (check CBC page on Wikipedia)
    uint8_t iv[]  = { 0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f };
    
    struct AES_ctx ctx_d;
    
    AES_init_ctx_iv(&ctx_d, key, iv);

    AES_CBC_decrypt_buffer(&ctx_d, u_decrypted, 64);

    return u_decrypted;
}
