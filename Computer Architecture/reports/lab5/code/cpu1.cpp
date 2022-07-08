#include <iostream>
#include <string>
#include <cstdlib>
#include <ctime>

using namespace std;

int idxs2idx(int i, int j, int N);
void gemm_baseline(float *A, float *B, float *C, int N);
void print_matrix(float *M, int N);

int main(int argc, char **argv)
{
    int n = 0;
    n = atoi(argv[1]);
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
    // cout << n << " " << N << endl;
    clock_t timer = clock();
    gemm_baseline(A, B, C, N);
    timer = clock() - timer;
    float dur = (float)timer / CLOCKS_PER_SEC;
    cout << dur << "s" << endl;
    // print_matrix(C, N);
    delete[] A;
    delete[] B;
    delete[] C;
    return 0;
}

int idxs2idx(int i, int j, int N)
{
    return i * N + j;
}

void gemm_baseline(float *A, float *B, float *C, int N)
{
    for(int i = 0; i < N; i ++)
    {
        for(int j = 0; j < N; j++)
        {
            // C[i][j]
            int idx = idxs2idx(i, j, N);
            C[idx] = 0.0f;
            for(int k = 0; k < N; k++)
            {
                C[idx] += A[idxs2idx(i, k, N)] * B[idxs2idx(k, j, N)];
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