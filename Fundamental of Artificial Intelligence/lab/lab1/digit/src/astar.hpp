#ifndef ASTAR_HPP_
#define ASTAR_HPP_

#include <vector>

using namespace std;

namespace astar
{
    class State
    {
    private:
        vector<vector<int> > digits;
        unsigned x;
        unsigned y;
        unsigned g;
        unsigned h;
        unsigned f;
        vector<vector<int> >* p_target;
        State* parent;
        char action;

    public:
        State();
        State(vector<vector<int> > digits, unsigned g, unsigned h, State* parent, char action);
        State(vector<vector<int> > digits, unsigned g, unsigned h, vector<vector<int> >* p_target, State* parent, char action);
        ~State();
        vector<vector<int> > get_digits() const;
        unsigned get_f() const;
        State* get_parent() const;
        char get_action() const;
        void set_h(unsigned h);

        bool operator== (const State& s) const;
        bool operator> (const State& s) const;
        bool operator>= (const State& s) const;
        bool operator< (const State& s) const;

        State* up() const;
        State* down() const;
        State* left() const;
        State* right() const;
    };
}

#endif