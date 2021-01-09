#include <vector>
#include <cstring>
#include <iostream>
#include <cstdio>
#include <stdlib.h>
#include "../head_file/evaluation.h"
#include "../head_file/AB_serach.h"
#include "../head_file/Get_position.h"
#define INF 0x3f3f3f3f
using namespace std;
int dir8[8][2] = {0, -1, 0, 1, 1, 0, -1, 0, 1, 1, 1, -1, -1, 1, -1, -1};
int temp_list[15];

bool check(int chess_list[], int len, int now_turn)
{
    for (int i = 0; i < len; i++)
    {
        int cnt = 0;
        while (i + cnt < len && chess_list[i + cnt] == now_turn)
            cnt++;
        if (cnt == 5)
            return 1;
    }
    return 0;
}
bool is_win(int now_turn, int chessboard[][15])
{
    bool flag = 0;
    for (int i = 0; i < 15; i++)
    {
        flag = max(flag, check(chessboard[i], 15, now_turn));
        if (i != 0 && i != 14)
        {
            for (int j = 0; j < 15 - i; j++)
                temp_list[j] = chessboard[i + j][j];
            flag = max(flag, check(temp_list, 15 - i, now_turn));
            for (int j = 0; j <= i; j++)
                temp_list[j] = chessboard[i - j][j];
            flag = max(flag, check(temp_list, i + 1, now_turn));
        }
    }
    for (int i = 0; i < 15; i++)
    {
        for (int j = 0; j < 15; j++)
            temp_list[j] = chessboard[j][i];
        flag = max(flag, check(temp_list, 15, now_turn));
        for (int j = 0; j < 15 - i; j++)
            temp_list[j] = chessboard[j][i + j];
        flag = max(flag, check(temp_list, 15 - i, now_turn));
        for (int j = 0; j <= i; j++)
            temp_list[j] = chessboard[j][i - j];
        flag = max(flag, check(temp_list, i + 1, now_turn));
    }
    return flag;
}
int px, py, maxd = 5;
int ab_search(int maxdepth, int alpha, int beta, int now_turn, int chessboard[][15])
{
    int cnt = 0;
    point list[25];
    get_position(chessboard, list, cnt);
    if (maxdepth == 0 || cnt == 0 || is_win(now_turn, chessboard))
    {
        if (now_turn == 1)
            return evaluation(chessboard, now_turn) - evaluation(chessboard, -now_turn) / 3 * 2;
        else
            return evaluation(chessboard, now_turn) / 3 * 2 - evaluation(chessboard, -now_turn);
    }

    for (int i = 0; i < cnt; i++)
    {
        point &temp = list[i];
        chessboard[temp.x][temp.y] = now_turn;
        int v = -ab_search(maxdepth - 1, -beta, -alpha, -now_turn, chessboard);
        chessboard[temp.x][temp.y] = 0;
        if (v >= beta)
            return beta;
        if (v > alpha)
        {
            if (maxdepth == maxd)
                px = temp.x, py = temp.y;
            alpha = v;
        }
    }
    return alpha;
}
bool chess_vis[15][15];
extern "C" void begin_search(int chessboard[][15], int now_turn)
{
    memset(chess_vis, 0, sizeof chess_vis);
    printf("best==%d px==%d py==%d\n", ab_search(maxd, -INF, INF, -1, chessboard), px, py);
    chessboard[px][py] = now_turn;
    return;
}

int main()
{
    int chessboard[15][15];
    memset(chessboard, 0, sizeof chessboard);
    int a, b;
    while (cin >> a >> b)
    {
        if (a == -1)
            break;
        chessboard[a][b] = 1;
        begin_search(chessboard, -1);
        for (int i = 0; i < 15; i++)
        {
            for (int j = 0; j < 15; j++)
            {
                if (chessboard[i][j] == 1)
                    printf("O ");
                else if (chessboard[i][j] == -1)
                    printf("X ");
                else
                    printf("? ");
            }
            printf("\n");
        }
        printf("\n");
    }
}
