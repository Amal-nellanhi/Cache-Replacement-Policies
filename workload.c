#include <stdio.h>
#include <stdlib.h>

// Array size: 128KB (Assuming we simulate a 32KB Cache, this guarantees conflict misses)
#define ARRAY_SIZE (32 * 1024) 
#define NUM_LOOPS 100

int main() {
    printf("Starting Cache Stress Test...\n");
    
    // Allocate memory
    int *arr = (int*)malloc(ARRAY_SIZE * sizeof(int));
    if (arr == NULL) return 1;

    // Initialize (Cold Misses)
    for (int i = 0; i < ARRAY_SIZE; i++) {
        arr[i] = i;
    }

    // Access Pattern Loop
    // We stride by 16 (64 bytes) to hit a new cache line every access
    volatile int sink; 
    for (int k = 0; k < NUM_LOOPS; k++) {
        for (int i = 0; i < ARRAY_SIZE; i += 16) {
            sink = arr[i]; // Read access
        }
    }

    printf("Done.\n");
    return 0;
}