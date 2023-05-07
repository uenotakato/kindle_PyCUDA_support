#include <stdio.h>
#include <math.h>

void basic_calculation(float num1, float num2) {
	// 四則演算 + - x /
	printf("a + b = %f\n", num1 + num2);
	printf("a - b = %f\n", num1 - num2);
	printf("a x b = %f\n", num1 * num2);
	printf("a / b = %f\n", num1 / num2);
	// べき乗・平方根の計算
	printf("a ** 2 = %f\n", powf(num1, 2.0));
	printf("a ** 0.5 = %f\n", sqrtf(num1));
}

/*
- 冪乗演算子がないため，powf()関数を用いている。（doubleの場合はpow）この関数はmath.hに定義されている.powf()関数は，第一引数を第二引数で累乗した値を返す.
- 平方根の計算はsqrtf()関数を用いている.この関数はmath.hに定義されている.sqrtf()関数は，引数の平方根を返す.
- printfは，第一引数に出力する文字列を指定し，第二引数以降に出力する変数を指定する.変数の指定は，%fのように%に続けて指定する.この場合，第二引数以降の変数は，第一引数の文字列に順番に代入される.
	- %fは，float型の変数を出力するための指定子である.
	- %dは，int型の変数を出力するための指定子である.
*/
