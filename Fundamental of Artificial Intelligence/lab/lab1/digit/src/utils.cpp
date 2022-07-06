#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <queue>
#include <limits>
#include <set>
#include "utils.hpp"
#include "astar.hpp"

using namespace std;
using namespace astar;


void load_data(vector<vector<int> >& data_vec, string file_path)
{
    data_vec.clear();
    ifstream input_file;
    input_file.open(file_path, ios::in);
    int tmp;
    while(!input_file.eof())
    {
        vector<int> tmp_vec;
        for(int i = 0; i < 5; i++)
        {
            input_file >> tmp;
            tmp_vec.push_back(tmp);
        }
        if(input_file.fail())
        {
            break;
        }
        data_vec.push_back(tmp_vec);
    }    
    input_file.close();
    return;
}

void output_data(string path, double time_in_second, string file_path)
{
    ofstream output_file;
    output_file.open(file_path, ios::app);
    output_file << path << "," << time_in_second << endl;
    output_file.close();
    return;
}

struct cmp
{
    bool operator()(const State* s1, const State* s2)
    {
        // return (*s1) > (*s2);
        return (*s1) >= (*s2);
    }
};

string a_star_search(const vector<vector<int> > &start, const vector<vector<int> > &target, unsigned int (*h_function)(const vector<vector<int> > &, const vector<vector<int> > &))
{
    // vector<State*> open;
    priority_queue<State*, vector<State*>, cmp> open;
    // vector<vector<vector<int> > > close;
    set<vector<vector<int> > > close;
    unsigned h = h_function(start, target);
    State* p_state = new State(start, 0, h, nullptr, 'O');
    // open.push_back(p_state);
    open.push(p_state);
    

    while(true)
    {
        if(open.empty())
        {
            return string("Failure");
        }
        p_state = open.top();
        open.pop();
        if(p_state->get_digits() == target)
        {
            // return string("Success");
            string solution = get_path(p_state);
            return solution;
        }
        // close.push_back(p_state->get_digits());
        close.insert(p_state->get_digits());
        for(int i = 0; i < 4; i++)
        {
            State* p_new_state = nullptr;
            switch (i)
            {
            case 0:
                p_new_state = p_state->up();
                break;
            case 1:
                p_new_state = p_state->down();
                break;
            case 2:
                p_new_state = p_state->left();
                break;
            case 3:
                p_new_state = p_state->right();
                break;
            
            default:
                cerr << "?" << endl;
                break;
            }
            if(p_new_state == nullptr)
            {
                continue;
            }
            // if(find(close.begin(), close.end(), p_new_state->get_digits()) != close.end())
            if(close.find(p_new_state->get_digits()) != close.end())
            {
                delete p_new_state;
                continue;
            }
            h = h_function(p_new_state->get_digits(), target);
            p_new_state->set_h(h);
            open.push(p_new_state);
        }
    }
}

string ida_star_search(const vector<vector<int> > &start, const vector<vector<int> > &target, unsigned int (*h_function)(const vector<vector<int> > &, const vector<vector<int> > &))
{
    const unsigned infinite = numeric_limits<unsigned>::max();
    unsigned h = h_function(start, target);
    State* p_start = new State(start, 0, h, nullptr, 'O');
    unsigned limit = p_start->get_f();
    while(limit < infinite)
    {
        unsigned next_limit = infinite;
        // vector<State*> list;
        // list.push_back(p_start);
        priority_queue<State*, vector<State*>, cmp> list;
        set<vector<vector<int> > > close;
        list.push(p_start);
        State* p_state;
        while(!list.empty())
        {
            // p_state = list.at(0);
            // list.erase(list.begin());
            p_state = list.top();
            list.pop();
            if(p_state->get_f() > limit)
            {
                next_limit = next_limit < p_state->get_f() ? next_limit : p_state->get_f();
            }
            else
            {
                if(p_state->get_digits() == target)
                {
                    // return "Success!";
                    return get_path(p_state);
                }
                close.insert(p_state->get_digits());
                for(int i = 0; i < 4; i++)
                {
                    State* p_new_state = nullptr;
                    switch (i)
                    {
                    case 0:
                        p_new_state = p_state->up();
                        break;
                    case 1:
                        p_new_state = p_state->down();
                        break;
                    case 2:
                        p_new_state = p_state->left();
                        break;
                    case 3:
                        p_new_state = p_state->right();
                        break;
                    
                    default:
                        cerr << "?" << endl;
                        break;
                    }
                    if(p_new_state == nullptr)
                    {
                        continue;
                    }
                    if(close.find(p_new_state->get_digits()) != close.end())
                    {
                        delete p_new_state;
                        continue;
                    }
                    h = h_function(p_new_state->get_digits(), target);
                    p_new_state->set_h(h);
                    // list.insert(list.begin(), p_new_state);
                    list.push(p_new_state);
                }
            }
        } // end while
        limit = next_limit;
    }
    return "Failure";
}

string get_path(State* p_state)
{
    vector<char> path;
    while(p_state->get_parent() != nullptr)
    {
        path.insert(path.begin(), p_state->get_action());
        p_state = p_state->get_parent();
    }
    return string(path.begin(), path.end());
}

unsigned int A_h1(const vector<vector<int> > &start, const vector<vector<int> > &target)
{
    // return 0;
    unsigned misplaced_num = 0;
    const unsigned size = start.size();
    for(int i = 0; i < size; i++)
    {
        for(int j = 0; j < size; j++)
        {
            if(start.at(i).at(j) == 0)
            {
                continue;
            }
            if(start.at(i).at(j) != target.at(i).at(j))
            {
                misplaced_num++;
            }
        }
    }
    return misplaced_num;
}

unsigned manhattan_distance(const unsigned& x1, const unsigned& y1, const unsigned& x2, const unsigned& y2)
{
    unsigned x_distance = (x1 > x2 ? x1 - x2 : x2 - x1);
    unsigned y_distance = (y1 > y2 ? y1 - y2 : y2 - y1);
    return x_distance + y_distance;
}

unsigned int A_h2(const vector<vector<int> > &start, const vector<vector<int> >&target)
{
    unsigned distance_sum = 0;
    const unsigned size = start.size();
    pair<unsigned, unsigned> start_coordinates[24] = {};
    pair<unsigned, unsigned> target_coordinates[24] = {};
    for(int i = 0; i < size; i++)
    {
        for(int j = 0; j < size; j++)
        {
            if(start.at(i).at(j) != 0)
            {
                start_coordinates[start.at(i).at(j) - 1] = pair<unsigned, unsigned>(i, j);
            }
            if(target.at(i).at(j) != 0)
            {
                target_coordinates[target.at(i).at(j) - 1] = pair<unsigned, unsigned>(i, j);
            }
        }
    }
    for(int i = 0; i < 24; i++)
    {
        // 9 cases
        unsigned x1 = start_coordinates[i].first;
        unsigned y1 = start_coordinates[i].second;
        unsigned x2 = target_coordinates[i].first;
        unsigned y2 = target_coordinates[i].second;
        unsigned distance = manhattan_distance(x1, y1, x2, y2);
        unsigned d = 100;
        if(x1 != 2 && y1 != 2)
        {
            unsigned d1, d2;
            if(x1 < 2 && y1 < 2)
            {
                d1 = manhattan_distance(x1, y1, 0, 2) + manhattan_distance(4, 2, x2, y2) + 1;
                d2 = manhattan_distance(x1, y1, 2, 0) + manhattan_distance(2, 4, x2, y2) + 1;
            }
            else if(x1 < 2 && y1 > 2)
            {
                d1 = manhattan_distance(x1, y1, 0, 2) + manhattan_distance(4, 2, x2, y2) + 1;
                d2 = manhattan_distance(x1, y1, 2, 4) + manhattan_distance(2, 0, x2, y2) + 1;
            }
            else if(x1 > 2 && y1 < 2)
            {
                d1 = manhattan_distance(x1, y1, 4, 2) + manhattan_distance(0, 2, x2, y2) + 1;
                d2 = manhattan_distance(x1, y1, 2, 0) + manhattan_distance(2, 4, x2, y2) + 1;
            }
            else
            {
                d1 = manhattan_distance(x1, y1, 4, 2) + manhattan_distance(0, 2, x2, y2) + 1;
                d2 = manhattan_distance(x1, y1, 2, 4) + manhattan_distance(2, 0, x2, y2) + 1;
            }
            d = d1 < d2 ? d1 : d2;
        }
        else if(x1 < 2 && y1 == 2)
        {
            d = manhattan_distance(x1, y1, 0, 2) + manhattan_distance(4, 2, x2, y2) + 1;
        }
        else if(x1 > 2 && y1 == 2)
        {
            d = manhattan_distance(x1, y1, 4, 2) + manhattan_distance(0, 2, x2, y2) + 1;
        }
        else if(x1 == 2 && y1 < 2)
        {
            d = manhattan_distance(x1, y1, 2, 0) + manhattan_distance(2, 4, x2, y2) + 1;
        }
        else if(x1 == 2 && y1 > 2)
        {
            d = manhattan_distance(x1, y1, 2, 4) + manhattan_distance(2, 0, x2, y2) + 1;
        }
        distance_sum += distance < d ? distance : d;
    }
    return distance_sum;
}