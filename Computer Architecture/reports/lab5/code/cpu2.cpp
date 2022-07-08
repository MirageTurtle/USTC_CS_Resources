#include <iostream>
#include <ctime>
#include <string>
#include <cstdlib>
#include <immintrin.h>

using namespace std;

int idxs2idx(int i, int j, int N);
bool gemm_verify(float *A, float *B, float *C, int N);
void gemm_avx(float *A, float *B, float *C, int N);
void print_matrix(float *M, int N);

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
    gemm_avx(A, B, C, N);
    timer = clock() - timer;
    // print_matrix(A, N);
    // print_matrix(B, N);
    // print_matrix(C, N);
    // bool result = gemm_verify(A, B, C, N);
    // cout << boolalpha << result << endl;
    float dur = (float)timer / CLOCKS_PER_SEC;
    // if(result)
    // {
    //     cout << dur << "s" << endl;
    // }
    // else
    // {
    //     cout << "false." << endl;
    // }
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
            if(abs(tmp - C[idxs2idx(i, j, N)]) >= 1e-3)
            {
                cout << "[NOT EQUAL] true: " << tmp << " result: " << C[idxs2idx(i, j, N)] << endl;
                cout << "[DIFF]: " << abs(tmp - C[idxs2idx(i, j, N)]) << endl;
                return false;
            }
        }
    }
    return true;
}

void gemm_avx(float *A, float *B, float *C, int N)
{
    __m256 vecA, vecB, vecC;
    // 先假设 n >= 3 即 N >= 8，向量不需要补0
    // 对于 n < 3的情况，因为会向量会初始化为0，所以不需要额外处理
    for(int i = 0; i < N; i++)
    {
        // init Matrix C
        for(int j = 0; j < N; j++)
        {
            // cout << idxs2idx(i, j, N) << endl;
            C[idxs2idx(i, j, N)] = 0.0f;
        }
        for(int j = 0; j < N; j++)
        {
            vecA = _mm256_set1_ps(A[idxs2idx(i, j, N)]);
            // 8 = 256 / 32
            for(int k = 0; k < N; k += 8)
            {
                vecB = _mm256_loadu_ps(B + idxs2idx(j, k, N));
                vecC = _mm256_loadu_ps(C + idxs2idx(i, k, N));
                vecC = _mm256_fmadd_ps(vecA, vecB, vecC);
                _mm256_storeu_ps(C + idxs2idx(i, k, N), vecC);
            }
        }
    }
    return;
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