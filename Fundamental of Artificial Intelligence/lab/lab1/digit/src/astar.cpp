#include <vector>
#include "astar.hpp"

using namespace std;
using namespace astar;

State::State()
{
    return;
}

State::State(vector<vector<int> > digits, unsigned g, unsigned h, State* parent, char action) : digits(digits), g(g), h(h), f(g + h), parent(parent), action(action)
{
    for(auto it1 = digits.begin(); it1 != digits.end(); it1++)
    {
        for(auto it2 = it1->begin(); it2 != it1->end(); it2++)
        {
            if((*it2) == 0)
            {
                this->x = it1 - digits.begin();
                this->y = it2 - it1->begin();
                return;
            }
        }
    }
}

State::State(vector<vector<int> > digits, unsigned g, unsigned h, vector<vector<int> >* p_target, State* parent, char action) : digits(digits), g(g), h(h), f(g + h), p_target(p_target), parent(parent), action(action)
{
    for(auto it1 = digits.begin(); it1 != digits.end(); it1++)
    {
        for(auto it2 = it1->begin(); it2 != it1->end(); it2++)
        {
            if((*it2) == 0)
            {
                this->x = it1 - digits.begin();
                this->y = it2 - it1->begin();
                return;
            }
        }
    }
}

State::~State()
{
    return;
}

vector<vector<int> > State::get_digits() const
{
    return this->digits;
}

unsigned State::get_f() const
{
    return this->f;
}

State* State::get_parent() const
{
    return this->parent;
}

char State::get_action() const
{
    return this->action;
}

void State::set_h(unsigned h)
{
    this->h = h;
    this->f = this->g + h;
    return;
}

bool State::operator== (const State& s) const
{
    return this->digits == s.get_digits();
}

bool State::operator> (const State& s) const
{
    return this->f > s.get_f();
}

bool State::operator>= (const State& s) const
{
    return this->f >= s.get_f();
}

bool State::operator< (const State& s) const
{
    return this->f < s.get_f();
}

State* State::up() const
{
    if(this->x == 0 && this->y != 2)
    {
        return nullptr;
    }
    unsigned next_x = this->x - 1, next_y = this->y;
    if(next_x > 4)
    {
        next_x = 4;
    }
    if(this->digits.at(next_x).at(next_y) < 0)
    {
        return nullptr;
    }
    vector<vector<int> > new_digits = this->digits;
    new_digits.at(x).at(y) = this->digits.at(next_x).at(next_y);
    new_digits.at(next_x).at(next_y) = 0;
    State* p_new_state = new State(new_digits, this->g + 1, 0, (State*)this, 'U');
    return p_new_state;
}

State* State::down() const
{
    if(this->x == 4 && this->y != 2)
    {
        return nullptr;
    }
    unsigned next_x = this->x + 1, next_y = this->y;
    if(next_x > 4)
    {
        next_x = 0;
    }
    if(this->digits.at(next_x).at(next_y) < 0)
    {
        return nullptr;
    }
    vector<vector<int> > new_digits = this->digits;
    new_digits.at(x).at(y) = this->digits.at(next_x).at(next_y);
    new_digits.at(next_x).at(next_y) = 0;
    State* p_new_state = new State(new_digits, this->g + 1, 0, (State*)this, 'D');
    return p_new_state;
}

State* State::left() const
{
    if(this->x != 2 && this->y == 0)
    {
        return nullptr;
    }
    unsigned next_x = this->x, next_y = this->y - 1;
    if(next_y > 4)
    {
        next_y = 4;
    }
    if(this->digits.at(next_x).at(next_y) < 0)
    {
        return nullptr;
    }
    vector<vector<int> > new_digits = this->digits;
    new_digits.at(x).at(y) = this->digits.at(next_x).at(next_y);
    new_digits.at(next_x).at(next_y) = 0;
    State* p_new_state = new State(new_digits, this->g + 1, 0, (State*)this, 'L');
    return p_new_state;
}

State* State::right() const
{
    if(this->x != 2 && this->y == 4)
    {
        return nullptr;
    }
    unsigned next_x = this->x, next_y = this->y + 1;
    if(next_y > 4)
    {
        next_y = 0;
    }
    if(this->digits.at(next_x).at(next_y) < 0)
    {
        return nullptr;
    }
    vector<vector<int> > new_digits = this->digits;
    new_digits.at(x).at(y) = this->digits.at(next_x).at(next_y);
    new_digits.at(next_x).at(next_y) = 0;
    State* p_new_state = new State(new_digits, this->g + 1, 0, (State*)this, 'R');
    return p_new_state;
}
