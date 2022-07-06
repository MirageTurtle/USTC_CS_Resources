#include <iostream>
#include <vector>
#include <string>
#include <chrono>
#include "utils.hpp"
#include "astar.hpp"

using namespace std;
using namespace chrono;
using namespace astar;

const vector<string> function_types {"A_h1", "A_h2", "IDA_h1", "IDA_h2"};

int main(int argc, char* argv[])
{
    if(argc != 4)
    {
        cerr << "Except 3 arguments but got " << argc - 1<< endl;
        return 1;
    }
    string function_type(argv[1]);
    int func_idx = find(function_types.begin(), function_types.end(), function_type) - function_types.begin();
    if(func_idx >= 4)
    {
        cerr << "Function Type Error!" << endl;
        return 2;
    }
    // input data
    vector<vector<int> > start;
    vector<vector<int> > target;
    string file_path = string("./data/") + string(argv[2]);
    load_data(start, file_path);
    file_path = string("./data/") + string(argv[3]);
    load_data(target, file_path);
    string result;
    auto clock_start = system_clock::now();
    auto clock_end = system_clock::now();
    switch (func_idx)
    {
    case 0:
        clock_start = system_clock::now();
        result = a_star_search(start, target, A_h1);
        clock_end = system_clock::now();
        break;
    case 1:
        clock_start = system_clock::now();
        result = a_star_search(start, target, A_h2);
        clock_end = system_clock::now();
        break;
    case 2:
        clock_start = system_clock::now();
        result = ida_star_search(start, target, A_h1);
        clock_end = system_clock::now();
        break;
    case 3:
        clock_start = system_clock::now();
        result = ida_star_search(start, target, A_h2);
        clock_end = system_clock::now();
        break;
    
    default:
        break;
    }
    cout << result << endl;
    auto duration = duration_cast<nanoseconds>(clock_end - clock_start);
    output_data(result, double(duration.count()) / 1000000000, string("./output/output_") + string(function_types.at(func_idx)) + string(".txt"));

    return 0;
}