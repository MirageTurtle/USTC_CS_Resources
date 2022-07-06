#include "worker.hpp"

using namespace std;
using namespace csp;

Worker::Worker()
{
    return;
}

Worker::Worker(int id, bool senior, vector<int> exclusion) : id(id), senior(senior), exclusion(exclusion)
{
    return;
}

Worker::~Worker()
{
    return;
}

int Worker::get_id() const
{
    return this->id;
}

bool Worker::is_senior() const
{
    return this->senior;
}

vector<int> Worker::get_exclusion() const
{
    return this->exclusion;
}

bool Worker::operator == (const Worker& worker)
{
    return this->id == worker.get_id();
}
