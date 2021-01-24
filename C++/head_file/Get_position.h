#include <vector>
using namespace std;

#ifndef _GET_POSISION_H
#define _GET_POSISION_H

struct point
{
    int x, y, v;
};

void get_position(int chessboard[][15], point position[], int &cnt, int &now_turn);

#endif