all: cpu1 cpu2 cpu3 gpu1 gpu2

cpu1: cpu1.cpp
	g++ cpu1.cpp -o cpu1.out
cpu2: cpu2.cpp
	g++ cpu2.cpp -o cpu2.out -mavx -mfma -O3
cpu3: cpu3.cpp
	g++ cpu3.cpp -o cpu3.out -mavx -mfma -O3

gpu1: gpu1.cu
	nvcc gpu1.cu -o gpu1.out -O3
gpu2: gpu2.cu
	nvcc gpu2.cu -o gpu2.out -O3

clean:
	rm *.out