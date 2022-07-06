#ifndef SCHEDULER_HPP_
#define SCHEDULER_HPP_

#include <vector>
#include "worker.hpp"

using namespace std;

namespace csp
{
    class Scheduler
    {
    private:
        int worker_num;
        int min_workers_num;
        int min_rest_days;
        int max_continual_rest_days;
        vector<Worker> workers;
        vector<vector<int> > scheduler;
    public:
        Scheduler();
        Scheduler(int worker_num, int min_workers_num, int min_rest_days, int max_continual_rest_days, vector<Worker> workers);
        Scheduler(int worker_num, int min_workers_num, int min_rest_days, int max_continual_rest_days, vector<int> workers, vector<vector<int> > exclusions);
        ~Scheduler();

        Worker get_worker(int n) const;
        vector<vector<int> > get_scheduler() const;
        void set(int day, Worker worker, int assign);
        void set(int day, int worker_idx, int assign);

        bool rest_days();
        bool continual_rest();
        bool workers_num();
        bool have_senior();
        bool no_exclusion();
        bool no_exclusion(Worker worker, int day);
        bool is_consistent();
        bool is_complete();

        pair<int, Worker> select_unassigned_day_worker();
        vector<pair<pair<int, Worker>, int> > inferences();
    };
}

#endif