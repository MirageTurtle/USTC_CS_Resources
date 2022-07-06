#ifndef WORKER_HPP_
#define WORKER_HPP_

#include <vector>

using namespace std;

namespace csp
{
    class Worker
    {
    private:
        int id;
        bool senior;
        vector<int> exclusion;
    public:
        Worker();
        Worker(int id, bool senior, vector<int> exclusion);
        ~Worker();
        int get_id() const;
        bool is_senior() const;
        vector<int> get_exclusion() const;

        bool operator == (const Worker& worker);
    };
}

#endif