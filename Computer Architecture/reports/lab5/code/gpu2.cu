#include <iostream>
#include <string>
#include <cstdlib>
#include <ctime>

// #define VERIFY

using namespace std;

__global__ void blocked_gemm_baseline(float *A, float *B, float *C, int N);
int idxs2idx(int i, int j, int N);
bool gemm_verify(float *A, float *B, float *C, int N);
void print_matrix(float *M, int N);

const int size = (1 << 4);

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
        // A[i] = i / 10.0f;
        // B[i] = i / 10.0f;
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
    // int size = 8;
    dim3 block_size(size, size);
    dim3 grid_size((N + size - 1) / size, (N + size - 1) / size);
    blocked_gemm_baseline<<<grid_size, block_size>>>(dA, dB, dC, N);
    cudaMemcpy((void *)C, (void *)dC, nBytes, cudaMemcpyDeviceToHost);
#ifdef VERIFY
    cout << boolalpha << gemm_verify(A, B, C, N) << endl;
#endif
    // print_matrix(A, N);
    // print_matrix(B, N);
    // print_matrix(C, N);
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

__global__ void blocked_gemm_baseline(float *A, float *B, float *C, int N)
{
    int x = threadIdx.x + blockIdx.x * blockDim.x;
    int y = threadIdx.y + blockIdx.y * blockDim.y;
    if(x >= N || y >= N)
    {
        return;
    }
    
    int tmp_x = threadIdx.x;
    int tmp_y = threadIdx.y;
    int block_num = (N + blockDim.x - 1) / blockDim.x;

    // const int block_size = (1 << 3);
    const int block_size = size;

    __shared__ float blockA[block_size][block_size];
    __shared__ float blockB[block_size][block_size];
    int A_start = blockIdx.x * block_size * N;
    int B_start = blockIdx.y * block_size;
    int A_step = block_size;
    int B_step = block_size * N;

    // 使用tmp减少与数组的交互，提升速度
    // 矩阵规模为 2^13 时，可以从2s+提升到1s+
    float tmp = 0.0f;
    for(int i = 0; i < block_num; i++)
    {
        blockA[tmp_x][tmp_y] = A[A_start + i * A_step + tmp_x * N + tmp_y];
        blockB[tmp_x][tmp_y] = B[B_start + i * B_step + tmp_x * N + tmp_y];
        __syncthreads();
        for(int j = 0; j < blockDim.x; j++)
        {
            // C[x * N + y] += blockA[tmp_x][j] * blockB[j][tmp_y];
            tmp += blockA[tmp_x][j] * blockB[j][tmp_y];
        }
        __syncthreads();
    }
    C[x * N + y] = tmp;
}

void print_matrix(float *M, int N)
{
    for(int i = 0; i < N; i++)
    {
        for(int j = 0; j < N; j++)
        {
            cout << M[idxs2idx(i, j, N)] << " ";
        }
        cout << endl;
    }
    return;
}