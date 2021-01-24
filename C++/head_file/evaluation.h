#ifndef _EVALUATION_H
#define _EVALUATION_H
enum chess_score
{
    alive_5 = 5000000,
    alive_4 = 40000,
    alive_3 = 3000,
    alive_2 = 200,
    alive_1 = 10,
    die_4 = 1000,
    die_3 = 10,
    die_2 = 1,
    die_1 = 0,
};
int evaluation(int chessboard[][15], int now_turn);
int check(int chess_list[], int len, int &now);

#endif