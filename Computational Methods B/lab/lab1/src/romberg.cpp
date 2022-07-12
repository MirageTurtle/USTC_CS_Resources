#include<iostream>
#include<iomanip>
// #include<cmath>

using namespace std;

double func(double x)
{
    return log(x);
}

int coordinate2idx(int x, int y)
{
    // x >= y
    return x * (x + 1) / 2 + y;
}

double Romberg(double a, double b, double e, int M, double (*func)(double), double* &R, int &idx)
{
    // double R[M * (M + 1) / 2] = {0};
    // double* R = new double[M * (M + 1) / 2]();
    R = new double[M * (M + 1) / 2]();
    // int n = 1;
    double result = 0;
    // double h = b - a;
    // double h[M] = {0};
    double* h = new double[M]();
    h[0] = b - a;
    R[coordinate2idx(0, 0)] = ((*func)(a) + (*func)(b)) * h[0] / 2;
    int i;
    for(i = 1; i < M; i++)
    {
        h[i] = h[i - 1] / 2;
        double sum = 0;
        // int end = int(pow(2, i - 1));
        int end = 1 << (i - 1);
        for(int j = 1; j <= end; j++)
        {
            sum += func(a + (2 * j - 1) * h[i]);
        }
        R[coordinate2idx(i, 0)] = (R[coordinate2idx(i-1, 0)] + h[i - 1] * sum) / 2;
        for(int j = 1; j <= i; j++)
        {
            // R[coordinate2idx(i, j)] = R[coordinate2idx(i, j - 1)] + (R[coordinate2idx(i, j - 1)] - R[coordinate2idx(i - 1, j - 1)]) / (int(pow(4, j)) - 1);
            R[coordinate2idx(i, j)] = R[coordinate2idx(i, j - 1)] + (R[coordinate2idx(i, j - 1)] - R[coordinate2idx(i - 1, j - 1)]) / ((1 << (2 * j)) - 1);
        }
        if(abs(R[coordinate2idx(i, i)] - R[coordinate2idx(i - 1, i - 1)]) < e)
        {
            break;
        }
    }
    // return R[coordinate2idx(i , i)];
    result = R[coordinate2idx(i , i)];
    idx = i;
    // delete[] R;
    delete[] h;
    return result;
}


int main()
{
    double* R;
    int idx;
    double result;
    result = Romberg(1, 2, 1.0e-4, 100, func, R, idx);
    // cout << setiosflags(ios::fixed) << setprecision(8) << result << endl;
    double true_value = 2 * log(2) - 1;
    cout << "积分准确结果（小数点后12位）:" << setprecision(12) << true_value << endl;
    cout << "Romberg积分表：" << endl;
    for(int i = 0; i <= idx; i++)
    {
        for(int j = 0; j <= i; j++)
        {
            cout << setprecision(8) << R[coordinate2idx(i, j)] << ' ';
        }
        cout << endl;
    }
    cout << "Romberg积分结果（小数点后12位）:";
    cout << setprecision(12) << result << endl;
    int k = 0;
    cout << "复化梯形积分结果及误差：" << endl;
    for(int i = k; i <= idx; i++)
    {
        cout << setprecision(8) << R[coordinate2idx(i, k)] << ' ';
    }
    cout << endl;
    for(int i = k; i <= idx; i++)
    {
        cout << setprecision(8) << abs(true_value - R[coordinate2idx(i, k)]) << ' ';
    }
    cout << endl;
    k = 1;
    cout << "复化Simpson积分结果及误差：" << endl;
    for(int i = k; i <= idx; i++)
    {
        cout << setprecision(8) << R[coordinate2idx(i, k)] << '\t';
    }
    cout << endl;
    for(int i = k; i <= idx; i++)
    {
        cout << setprecision(8) << abs(true_value - R[coordinate2idx(i, k)]) << '\t';
    }
    cout << endl;
    
    return 0;
}