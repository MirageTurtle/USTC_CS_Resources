#ifndef UTILS_HPP_
#define UTILS_HPP_

#include <vector>
#include <string>
#include "astar.hpp"

using namespace std;
using namespace astar;


void load_data(vector<vector<int> >& data_vec, string file_path);
void output_data(string path, double time_in_second, string file_path);
string a_star_search(const vector<vector<int> > &start, const vector<vector<int> > &target, unsigned int (*h_function)(const vector<vector<int> > &, const vector<vector<int> > &));
string ida_star_search(const vector<vector<int> > &start, const vector<vector<int> > &target, unsigned int (*h_function)(const vector<vector<int> > &, const vector<vector<int> > &));
string get_path(State* p_state);
unsigned int A_h1(const vector<vector<int> > &start, const vector<vector<int> > &target);
unsigned int A_h2(const vector<vector<int> > &start, const vector<vector<int> >&target);
unsigned int IDA_h1(const vector<vector<int> > &start, const vector<vector<int> >&target);
unsigned int IDA_h2(const vector<vector<int> > &start, const vector<vector<int> > &target);

#endif