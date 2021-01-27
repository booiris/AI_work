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

bool check_end(int chess_list[], int len, int &now_turn)
{
    for (int i = 0; i < len; i++)
    {
        if (chess_list[i] == 0)
            continue;
        int cnt = 0;
        while (i + cnt < len && chess_list[i + cnt] == now_turn)
            cnt++;
        if (cnt == 5)
            return 1;
    }
    return 0;
}
bool is_end(int chessboard[][15], int now_turn)
{
    bool flag = 0;
    for (int i = 0; i < 15; i++)
    {
        flag = max(flag, check_end(chessboard[i], 15, now_turn));
        for (int j = 0; j < 15; j++)
            temp_list[j] = chessboard[j][i];
        flag = max(flag, check_end(temp_list, 15, now_turn));
    }
    for (int i = 0; i < 15; i++)
    {
        int j;
        if (i != 14)
        {
            for (j = 0; j < 15; j++)
            {
                if (i - j < 0)
                    break;
                temp_list[j] = chessboard[j][i - j];
            }
            flag = max(flag, check_end(temp_list, j, now_turn));
        }
        if (i != 0)
        {
            for (j = 0; j < 15; j++)
            {
                if (i + j >= 15)
                    break;
                temp_list[j] = chessboard[j][i + j];
            }
            flag = max(flag, check_end(temp_list, j, now_turn));
        }
    }
    for (int i = 0; i < 15; i++)
    {
        int j;
        for (j = 0; j < 15; j++)
        {
            if (i - j < 0)
                break;
            temp_list[j] = chessboard[14 - j][i - j];
        }
        flag = max(flag, check_end(temp_list, j, now_turn));
        for (j = 0; j < 15; j++)
        {
            if (i + j >= 15)
                break;
            temp_list[j] = chessboard[14 - j][i + j];
        }
        flag = max(flag, check_end(temp_list, j, now_turn));
    }
    return flag;
}
int px, py, maxd = 2, turn;
int ab_search(int maxdepth, int alpha, int beta, int now_turn, int chessboard[][15], int &who_win)
{
    if (who_win != 0 || is_end(chessboard, -turn))
        who_win = -turn;
    int cnt = 0;
    point list[75];
    get_position(chessboard, list, cnt, now_turn);
    if (maxdepth < 0 || cnt == 0)
        return evaluation(chessboard, now_turn) - evaluation(chessboard, -now_turn) / 2;

    for (int i = 0; i < cnt; i++)
    {
        point &temp = list[i];
        chessboard[temp.x][temp.y] = now_turn;
        int v = -ab_search(maxdepth - 1, -beta, -alpha, -now_turn, chessboard, who_win);
        chessboard[temp.x][temp.y] = 0;
        if (who_win == -turn && now_turn == turn)
        {
            who_win = 0;
            continue;
        }
        if (v >= beta)
            return beta;
        if (v > alpha)
        {
            if (maxdepth == maxd)
            {
                px = temp.x, py = temp.y;
            }
            alpha = v;
        }
    }
    return alpha;
}

extern "C" void begin_search(int chessboard[][15], int now_turn)
{
    turn = now_turn;
    int who_win = 0;
    px = -1, py = -1;
    int v = ab_search(maxd, -INF, INF, now_turn, chessboard, who_win);
    if (px == -1)
    {
        for (int i = 0; i < 15 && px == -1; i++)
        {
            for (int j = 0; j < 15 && px == -1; j++)
            {
                if (chessboard[i][j] == 0)
                {
                    px = i, py = j;
                    chessboard[i][j] = now_turn;
                    break;
                }
            }
        }
    }
    chessboard[px][py] = now_turn;
    return;
}

int main()
{
    int chessboard[15][15];
    memset(chessboard, 0, sizeof chessboard);
    int a, b;
    int now_turn = -1;
    for (int i = 0; i < 15; i++)
    {
        for (int j = 0; j < 15; j++)
        {
            chessboard[i][j] = 0;
        }
    }
    chessboard[7][7] = 1;
    while (!is_end(chessboard, -now_turn))
    {
        begin_search(chessboard, now_turn);
        now_turn = -now_turn;
        for (int i = 0; i < 15; i++)
        {
            for (int j = 0; j < 15; j++)
            {
                if (chessboard[i][j] == 1)
                    printf("O ");
                else if (chessboard[i][j] == -1)
                    printf("X ");
                else
                    printf(". ");
            }
            printf("\n");
        }
        printf("\n");
    }
    // while (cin >> a >> b)
    // {
    //     if (a == -1)
    //         break;
    //     chessboard[a][b] = 1;
    //     for (int i = 0; i < 15; i++)
    //     {
    //         for (int j = 0; j < 15; j++)
    //         {
    //             if (chessboard[i][j] == 1)
    //                 printf("O ");
    //             else if (chessboard[i][j] == -1)
    //                 printf("X ");
    //             else
    //                 printf(". ");
    //         }
    //         printf("\n");
    //     }
    //     printf("\n");
    //     begin_search(chessboard, -1);
    //     for (int i = 0; i < 15; i++)
    //     {
    //         for (int j = 0; j < 15; j++)
    //         {
    //             if (chessboard[i][j] == 1)
    //                 printf("O ");
    //             else if (chessboard[i][j] == -1)
    //                 printf("X ");
    //             else
    //                 printf(". ");
    //         }
    //         printf("\n");
    //     }
    //     printf("\n");
    // }
}
