#include <iostream>
#include <string>
#include <cstdlib>
#include <ctime>

// #define VERIFY

using namespace std;

__global__ void gemm_baseline(float *A, float *B, float *C, int N);
int idxs2idx(int i, int j, int N);
bool gemm_verify(float *A, float *B, float *C, int N);

int main(int argc, char ** argv)
{
    int n = atoi(argv[1]);
    int N = (1 << n);
    // init
    float *A = new float[N * N];
    float *B = new float[N * N];
    float *C = new float[N * N];
    srand48 (static_cast <unsigned> (time(0)));
    for(int i = 0; i < N * N; i++)
    {
        A[i] = static_cast <float> (drand48());
        B[i] = static_cast <float> (drand48());
    }
    float *dA, *dB, *dC;
    int nBytes = N * N * sizeof(float);
    cudaMalloc((void **)&dA, nBytes);
    cudaMalloc((void **)&dB, nBytes);
    cudaMalloc((void **)&dC, nBytes);
    cudaMemcpy((void *)dA, (void *)A, nBytes, cudaMemcpyHostToDevice);
    cudaMemcpy((void *)dB, (void *)B, nBytes, cudaMemcpyHostToDevice);
    int size = 8;
    dim3 block_size(size, size);
    dim3 grid_size((N + size - 1) / size, (N + size - 1) / size);
    gemm_baseline<<<grid_size, block_size>>>(dA, dB, dC, N);
    cudaMemcpy((void *)C, (void *)dC, nBytes, cudaMemcpyDeviceToHost);
#ifdef VERIFY
    cout << boolalpha << gemm_verify(A, B, C, N) << endl;
#endif
    return 0;
}

int idxs2idx(int i, int j, int N)
{
    return i * N + j;
}

bool gemm_verify(float *A, float *B, float *C, int N)
{
    for(int i = 0; i < N; i++)
    {
        for(int j = 0; j < N; j++)
        {
            float tmp = 0.0f;
            for(int k = 0; k < N; k++)
            {
                tmp += A[idxs2idx(i, k, N)] * B[idxs2idx(k, j, N)];
            }
            // float equal: difference less than 1e-4
            if(abs(tmp - C[idxs2idx(i, j, N)]) >= 1e-4)
            {
                cout << "[WRONG]" << "i: " << i << " j: " << j << " true: " << tmp << " result: " << C[idxs2idx(i, j, N)] << endl;
                cout << "[DIFF]: " << abs(tmp - C[idxs2idx(i, j, N)]) << endl;
                return false;
            }
        }
    }
    return true;
}

__global__ void gemm_baseline(float *A, float *B, float *C, int N)
{
    int x = threadIdx.x + blockIdx.x * blockDim.x;
    int y = threadIdx.y + blockIdx.y * blockDim.y;
    if(x >= N || y >= N)
    {
        return;
    }
    C[x * N + y] = 0.0f;
    float *pa = A + x * N;
    float *pb = B + y;
    for(int i = 0; i < N; i++, pa++, pb += N)
    {
        C[x * N + y] += (*pa) * (*pb);
    }
    return;
}