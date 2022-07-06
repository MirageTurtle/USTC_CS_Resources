#include <iostream>
#include <vector>
#include <chrono>
#include <fstream>
#include "scheduler.hpp"
#include "worker.hpp"
#include "utils.hpp"

using namespace std;
using namespace chrono;
using namespace csp;

int main()
{
    // case 1
    int worker_num = 7;
    int min_workers_num = 4;
    const int min_rest_days = 2;
    const int max_continual_rest_days = 2;
    vector<int> seniors = {1, 1, 0, 0, 0, 0, 0};
    // const vector<int> seniors = {1, 1, 0, 0, 0, 0, 0, 1, 0, 1};
    vector<pair<int, int> > exclusion = {{1, 4}, {2, 3}, {3, 6}};
    // const vector<pair<int, int> > exclusion = {{1, 5}, {2, 6}, {8, 10}};

    vector<Worker> workers;
    for(int i = 0; i < worker_num; i++)
    {
        vector<int> worker_exclusion;
        for(auto it = exclusion.begin(); it != exclusion.end(); it++)
        {
            if(it->second == i + 1)
            {
                worker_exclusion.push_back(it->first);
            }
        }
        for(auto it = exclusion.begin(); it != exclusion.end(); it++)
        {
            if(it->first == i + 1)
            {
                worker_exclusion.push_back(it->second);
            }
        }
        Worker worker(i + 1, (bool)seniors.at(i), worker_exclusion);
        workers.push_back(worker);
    }
    Scheduler scheduler(worker_num, min_workers_num, min_rest_days, max_continual_rest_days, workers);
    auto clock_start = system_clock::now();
    bool result = backtrack(scheduler);
    auto clock_end = system_clock::now();
    auto duration = duration_cast<nanoseconds>(clock_end - clock_start);
    auto s_table = scheduler.get_scheduler();
    cout << "Case 1:" << endl;
    if(result)
    {
        for(int j = 0; j < worker_num; j++)
        {
            for(int i = 0; i < 7; i++)
            {
                cout << s_table.at(i).at(j) << " ";
            }
            cout << endl;
        }
    }
    else
    {
        cout << "wuwuwu" << endl;
    }
    cout << "time: " << double(duration.count()) / 1000000000 << "s" << endl;
    ofstream output_file;
    output_file.open("./output/output1.txt", ios::out);
    for(int i = 0; i < 7; i++)
    {
        for(int j = 0; j < worker_num; j++)
        {
            if(s_table.at(i).at(j))
            {
                output_file << (j + 1) << " ";
            }
        }
        output_file << endl;
    }
    output_file.close();

    // case 2
    worker_num = 10;
    min_workers_num = 5;
    seniors = {1, 1, 0, 0, 0, 0, 0, 1, 0, 1};
    exclusion = {{1, 4}, {2, 3}, {3, 6}};
    workers.clear();
    for(int i = 0; i < worker_num; i++)
    {
        vector<int> worker_exclusion;
        for(auto it = exclusion.begin(); it != exclusion.end(); it++)
        {
            if(it->second == i + 1)
            {
                worker_exclusion.push_back(it->first);
            }
        }
        for(auto it = exclusion.begin(); it != exclusion.end(); it++)
        {
            if(it->first == i + 1)
            {
                worker_exclusion.push_back(it->second);
            }
        }
        Worker worker(i + 1, (bool)seniors.at(i), worker_exclusion);
        workers.push_back(worker);
    }
    Scheduler scheduler2(worker_num, min_workers_num, min_rest_days, max_continual_rest_days, workers);
    clock_start = system_clock::now();
    result = backtrack(scheduler2);
    clock_end = system_clock::now();
    duration = duration_cast<nanoseconds>(clock_end - clock_start);
    s_table = scheduler2.get_scheduler();
    cout << "Case 2:" << endl;
    if(result)
    {
        for(int j = 0; j < worker_num; j++)
        {
            for(int i = 0; i < 7; i++)
            {
                cout << s_table.at(i).at(j) << " ";
            }
            cout << endl;
        }
    }
    else
    {
        cout << "wuwuwu" << endl;
    }
    cout << "time: " << double(duration.count()) / 1000000000 << "s" << endl;

    output_file.open("./output/output2.txt", ios::out);
    for(int i = 0; i < 7; i++)
    {
        for(int j = 0; j < worker_num; j++)
        {
            if(s_table.at(i).at(j))
            {
                output_file << (j + 1) << " ";
            }
        }
        output_file << endl;
    }
    output_file.close();

    return 0;
}