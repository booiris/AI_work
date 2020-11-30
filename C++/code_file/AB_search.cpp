#include <vector>
#include <cstring>
#include "../head_file/evaluation.h"
#include "../head_file/AB_serach.h"
#include "../head_file/Get_position.h"
using namespace std;

int dir[4][2] = {0, 1, 0, -1, 1, 0, -1, 0};
vector<chess_pos> pos_list;
int chessboard[15][15];

int ab_search(int maxdepth, int nowdepth, int alpha, int beta, int now_turn)
{
    pos_list.clear();
    get_position(chessboard, pos_list, now_turn);
    int res = 0;
    for (auto i = pos_list.begin(); i != pos_list.end(); i++)
    {
        chess_pos &temp = *i;
        chessboard[temp.x][temp.y] = now_turn;
        int v = evaluation(chessboard, now_turn);
        chessboard[temp.x][temp.y] = 0;
    }
    return res;
}

int begin_search(int chess_board[][15], int now_turn)
{
    memcpy(chessboard, chess_board, sizeof(int));
    return ab_search(4, 0, 0, 0, 1);
}

// int main()
// {
// }
