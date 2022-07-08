#include <iostream>
#include <ctime>
#include <string>
#include <cstdlib>
#include <immintrin.h>

#define UNROLL (4)

using namespace std;

int idxs2idx(int i, int j, int N);
bool gemm_verify(float *A, float *B, float *C, int N);
void gemm_avx_block(float *A, float *B, float *C, int N, int block_size);
void print_matrix(float *M, int N);
void transpose(float *matrix, float *transposed, int N);
void block(float *A, float *B, float *C, int N, int si, int sj, int sk, int block_size);

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
    clock_t timer = clock();
    // block(A, B, C, N, 0, 0, 0, N);
    gemm_avx_block(A, B, C, N, (1 << 8));
    timer = clock() - timer;
    // print_matrix(A, N);
    // print_matrix(B, N);
    // print_matrix(C, N);
    // bool result = gemm_verify(A, B, C, N);
    // cout << boolalpha << result << endl;
    float dur = (float)timer / CLOCKS_PER_SEC;
    cout << dur << "s" << endl;
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

void gemm_avx_block(float *A, float *B, float *C, int N, int block_size)
{
    for(int sj = 0; sj < N; sj += block_size)
    {
        for(int si = 0; si < N; si += block_size)
        {
            for(int sk = 0; sk < N; sk += block_size)
            {
                block(A, B, C, N, si, sj, sk, block_size);
            }
        }
    }
    return;
}

void transpose(float *matrix, float *transposed, int N)
{
    for(int i = 0; i < N; i++)
    {
        for(int j = 0; j < N; j++)
        {
            transposed[idxs2idx(i, j, N)] = matrix[idxs2idx(j, i, N)];
        }
    }
    return;
}

void block(
    float *A, float *B, float *C,
    int N, int si, int sj, int sk,
    int block_size
)
{
    for(int i = si; i < si + block_size && i < N; i += UNROLL)
    {
        for(int j = sj; j < sj + block_size && j < N; j++)
        {
            // unroll a
            __m256 a[UNROLL];
            for(int x = 0; x < UNROLL; x++)
            {
                // A 的一列元素各自对应的向量
                a[x] = _mm256_set1_ps(A[idxs2idx(i + x, j, N)]);
            }
            for(int k = sk; k < sk + block_size && k < N; k += 8)
            {
                __m256 b;
                // b = [ B[j][k] ... B[j][k+7] ]
                b = _mm256_loadu_ps(B + idxs2idx(j, k, N));
                // unroll c
                __m256 c[UNROLL];
                for(int x = 0; x < UNROLL; x++)
                {
                    c[x] = _mm256_loadu_ps(C + idxs2idx(i + x, k, N));
                    c[x] = _mm256_fmadd_ps(a[x], b, c[x]);
                    _mm256_storeu_ps(C + idxs2idx(i + x, k, N), c[x]);
                }
            }
        }
    }
    return;
}