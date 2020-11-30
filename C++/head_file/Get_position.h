#include <vector>
using namespace std;

#ifndef _GET_POSISION_H
#define _GET_POSISION_H


struct chess_pos
{
    int x, y;
};

void get_position(int chessboard[][15], vector<chess_pos> &position, int now_turn);

#endif