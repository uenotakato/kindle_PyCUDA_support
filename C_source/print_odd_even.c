#include <stdio.h>

void print_odd_even(int num){
    for (int i = 0; i < num; i++){
        if (i % 2 == 0){
            printf("%d is an even number.\n", i);
        } else if (!(i % 2 == 0)){
	        printf("%d is an odd number.\n", i);
        } else {
            printf("Something wrong...\n");
        }
    }
}

/*
- for文の書き方は，Pythonと同じである.
- if文の書き方は，Pythonと同じである.
- else if文は，Pythonではelif文である.
- for (カウンタ変数の初期化; 継続条件; カウンタ変数の更新) {
    繰り返し実行する文;
}
*/
