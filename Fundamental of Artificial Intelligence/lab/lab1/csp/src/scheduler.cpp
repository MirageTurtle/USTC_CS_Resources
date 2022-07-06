#include "scheduler.hpp"
#include "worker.hpp"

using namespace std;
using namespace csp;

Scheduler::Scheduler()
{
    return;
}

Scheduler::Scheduler(int worker_num, int min_workers_num, int min_rest_days, int max_continual_rest_days, vector<Worker> workers) : worker_num(worker_num), min_workers_num(min_workers_num), min_rest_days(min_rest_days), max_continual_rest_days(max_continual_rest_days)
{
    this->workers = workers;
    this->scheduler = vector<vector<int> >(7, vector<int>(worker_num, -1));
    return;
}

Scheduler::Scheduler(int worker_num, int min_workers_num, int min_rest_days, int max_continual_rest_days, vector<int> workers, vector<vector<int> > exclusions) : worker_num(worker_num), min_workers_num(min_workers_num), min_rest_days(min_rest_days), max_continual_rest_days(max_continual_rest_days)
{
    this->workers = vector<Worker>();
    for(int i = 0; i < worker_num; i++)
    {
        this->workers.push_back(Worker(i + 1, (bool)workers.at(i), exclusions.at(i)));
    }
    this->scheduler = vector<vector<int> >(7, vector<int>(worker_num, -1));
    return;
}

Scheduler::~Scheduler()
{
    return;
}

Worker Scheduler::get_worker(int n) const
{
    return this->workers.at(n - 1);
}

vector<vector<int> > Scheduler::get_scheduler() const
{
    return this->scheduler;
}

void Scheduler::set(int day, Worker worker, int assign)
{
    set(day, worker.get_id() - 1, assign);
    return;
}

void Scheduler::set(int day, int worker_idx, int assign)
{
    this->scheduler.at(day).at(worker_idx) = assign;
    return;
}

bool Scheduler::rest_days()
{
    vector<int> rest_days(this->worker_num);
    for(int i = 0; i < 7; i++)
    {
        for(int j = 0; j < this->worker_num; j++)
        {
            if(this->scheduler.at(i).at(j) != 1)
            {
                rest_days.at(j)++;
            }
        }
    }
    for(int i = 0; i < this->worker_num; i++)
    {
        if(rest_days.at(i) < min_rest_days)
        {
            return false;
        }
    }
    return true;
}

bool Scheduler::continual_rest()
{
    vector<int> continual_rest_days(this->worker_num);
    for(int i = 0; i < 7; i++)
    {
        for(int j = 0; j < this->worker_num; j++)
        {
            if(this->scheduler.at(i).at(j) == 0)
            {
                continual_rest_days.at(j)++;
                if(continual_rest_days.at(j) > max_continual_rest_days)
                {
                    return false;
                }
            }
            else
            {
                continual_rest_days.at(j) = 0;
            }
        }
    }
    return true;
}

bool Scheduler::workers_num()
{
    // vector<int> workers_num(7);
    for(int i = 0; i < 7; i++)
    {
        int workers_num = 0;
        for(int j = 0; j < this->worker_num; j++)
        {
            // workers_num += this->scheduler.at(i).at(j);
            // if(this->scheduler.at(i).at(j) == 1)
            if(this->scheduler.at(i).at(j) != 0)
            {
                workers_num += 1;
            }
        }
        if(workers_num < this->min_workers_num)
        {
            return false;
        }
    }
    return true;
}

bool Scheduler::have_senior()
{
    for(int i = 0; i < 7; i++)
    {
        int j;
        for(j = 0; j < this->worker_num; j++)
        {
            if(this->workers.at(j).is_senior() && this->scheduler.at(i).at(j) != 0)
            {
                break;
            }
        }
        if(j >= this->worker_num)
        {
            return false;
        }
    }
    return true;
}

bool Scheduler::no_exclusion()
{
    for(int i = 0; i < 7; i++)
    {
        for(int j = 0; j < this->worker_num; j++)
        {
            if(this->scheduler.at(i).at(j) == 1 && !no_exclusion(this->workers.at(j), i))
            {
                return false;
            }
        }
    }
    return true;
}

bool Scheduler::no_exclusion(Worker worker, int day)
{
    vector<int> exclusion = worker.get_exclusion();
    for(auto it = exclusion.begin(); it != exclusion.end(); it++)
    {
        // if(this->scheduler.at(day).at(*it) != 0)
        if(this->scheduler.at(day).at((*it) - 1) == 1)
        {
            return false;
        }
    }
    return true;
}

bool Scheduler::is_consistent()
{
    bool is_consistent = true;
    is_consistent = is_consistent && rest_days();
    is_consistent = is_consistent && continual_rest();
    is_consistent = is_consistent && workers_num();
    is_consistent = is_consistent && have_senior();
    is_consistent = is_consistent && no_exclusion();
    return is_consistent;
}

bool Scheduler::is_complete()
{
    for(int i = 0; i < 7; i++)
    {
        for(int j = 0; j < this->worker_num; j++)
        {
            if(this->scheduler.at(i).at(j) == -1)
            {
                return false;
            }
        }
    }
    return true;
}

pair<int, Worker> Scheduler::select_unassigned_day_worker()
{
    for(int i = 0; i < 7; i++)
    {
        for(int j = 0; j < this->worker_num; j++)
        {
            if(this->scheduler.at(i).at(j) == -1)
            {
                return {i, this->workers.at(j)};
            }
        }
    }
    return {-1, Worker()};
}

vector<pair<pair<int, Worker>, int> > Scheduler::inferences()
{
    vector<pair<pair<int, Worker>, int> > inferenced;
    // have exclusion
    for(int i = 0; i < 7; i++)
    {
        for(int j = 0; j < this->worker_num; j++)
        {
            if(this->scheduler.at(i).at(j) == -1)
            {
                auto exclusion = this->workers.at(j).get_exclusion();
                for(auto it = exclusion.begin(); it != exclusion.end(); it++)
                {
                    if(this->scheduler.at(i).at((*it) - 1) == 1)
                    {
                        inferenced.push_back({{i, this->workers.at(j)}, 0});
                    }
                }
            }
        }
    }
    // continual rest
    for(int j = 0; j < this->worker_num; j++)
    {
        for(int i = 0; i < 7; i++)
        {
            if(this->scheduler.at(i).at(j) == -1)
            {
                int continual_rest_days = 0;
                for(int k = i - 1; k >= 0; k--)
                {
                    if(this->scheduler.at(k).at(j) == 0)
                    {
                        continual_rest_days++;
                    }
                    else
                    {
                        break;
                    }
                }
                for(int k = i + 1; k < 7; k++)
                {
                    if(this->scheduler.at(k).at(j) == 0)
                    {
                        continual_rest_days++;
                    }
                    else
                    {
                        break;
                    }
                }
                if(continual_rest_days >= max_continual_rest_days)
                {
                    inferenced.push_back({{i, this->workers.at(j)}, 1});
                }
            }
        }
    }
    // vector<int> senior_idx;
    // for(int j = 0; j < this->worker_num; j++)
    // {
    //     if(this->workers.at(j).is_senior())
    //     {
    //         senior_idx.push_back(j);
    //     }
    // }
    // for(int i = 0; i < 7; i++)
    // {

    // }

    return inferenced;
}