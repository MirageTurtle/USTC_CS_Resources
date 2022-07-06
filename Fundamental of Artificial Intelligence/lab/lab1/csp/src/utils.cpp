#include "scheduler.hpp"

using namespace std;
using namespace csp;


bool backtrack(Scheduler& scheduler)
{
    if(scheduler.is_complete())
    {
        return true;
    }
    pair<int, Worker> day_worker = scheduler.select_unassigned_day_worker();
    // for each value
    for(int assign = 1; assign >= 0; assign--)
    {
        if(assign && !scheduler.no_exclusion(day_worker.second, day_worker.first))
        {
            continue;
        }
        Scheduler new_scheduler(scheduler);
        new_scheduler.set(day_worker.first, day_worker.second, assign);
        vector<pair<pair<int, Worker>, int> >  inferenced;
        bool contradictory = false;
        if(new_scheduler.is_consistent())
        {
            scheduler.set(day_worker.first, day_worker.second, assign);
            inferenced = scheduler.inferences();
            for(auto it = inferenced.begin(); it != inferenced.end(); it++)
            {
                int now_statuse = scheduler.get_scheduler().at(it->first.first).at(it->first.second.get_id() - 1);
                if(now_statuse == -1)
                {
                    scheduler.set(it->first.first, it->first.second, it->second);
                }
                else if(now_statuse != it->second)
                {
                    contradictory = true;
                    break;
                }
            }
            if(!contradictory)
            {
                bool result = backtrack(scheduler);
                if(result)
                {
                    return true;
                }
            }
        }
        // remove
        scheduler.set(day_worker.first, day_worker.second, -1);
        for(auto it = inferenced.begin(); it != inferenced.end(); it++)
        {
            scheduler.set(it->first.first, it->first.second, -1);
        }
    }
    return false;
}

// bool order_domain_values(pair<int, int> day_worker, const Scheduler& scheduler)
// {

// }