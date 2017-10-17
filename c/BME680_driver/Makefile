all: main

lib:
	gcc -c -fpic bme680.c              
	ar rcs libbme680.a bme680.o
	gcc -shared -o libbme680.so bme680.o

main: lib
	gcc main.c -L. -static -lbme680 -o main
