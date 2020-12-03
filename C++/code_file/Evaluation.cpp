#include <stdlib.h>
#include <cstdio>
#include "../head_file/evaluation.h"

enum chess_score
{
    alive_5 = 1000000,
    alive_4 = 100000,
    alive_3 = 10000,
    alive_2 = 1000,
    alive_1 = 10,
    die_4 = 1000,
    die_3 = 100,
    die_2 = 10,
    die_1 = 1,
}; 

int now; // 当前下棋的人
int temp[15];
int check_cnt(int part[], int len)
{
    if (part[0] != 0 && part[len - 1] != 0)
        return 0;
    for (int i = 1; i < len - 1; i++)
    {
        if (part[i] != now)
            return 0;
    }
    if (part[0] == 0 && part[len - 1] == 0)
        return 1;
    else
        return 2;
}
int check(int chess_list[], int len)
{
    int res = 0;
    for (int i = 0; i < len; i++)
    {
        if (i + 5 >= len)
            break;
        bool flag = 1;
        for (int j = 0; j < 5; j++)
        {
            if (chess_list[i + j] != now)
            {
                flag = 0;
                break;
            }
        }
        if (flag)
            res += alive_5;
    }
    for (int i = 0; i < len; i++)
    {
        if (i + 6 >= len)
            break;
        int flag = check_cnt(&chess_list[i], 6);
        if (flag == 1)
            res += alive_4;
        if (flag == 2)
            res += die_4;
    }
    for (int i = 0; i < len; i++)
    {
        if (i + 5 >= len)
            break;
        int flag = check_cnt(&chess_list[i], 5);
        if (flag == 1)
            res += alive_3;
        if (flag == 2)
            res += die_3;
    }
    for (int i = 0; i < len; i++)
    {
        if (i + 4 >= len)
            break;
        int flag = check_cnt(&chess_list[i], 4);
        if (flag == 1)
            res += alive_2;
        if (flag == 2)
            res += die_2;
    }
    for (int i = 1; i < len - 1; i++)
    {
        if (i + 3 >= len)
            break;
        int flag = check_cnt(&chess_list[i], 3);
        if (flag == 1)
            res += alive_1;
        if (flag == 2)
            res += die_1;
    }
    for (int i = 0; i < 4; i++)
    {
        if (i + 1 >= len || i >= len || chess_list[i] != now)
            break;
        if (chess_list[i] == now && chess_list[i + 1] == 0)
        {
            switch (i)
            {
            case 0:
                res += die_1;
                break;
            case 1:
                res += die_2;
                break;
            case 2:
                res += die_3;
                break;
            case 3:
                res += die_4;
            }
            break;
        }
    }
    for (int i = 0; i < 4; i++)
    {
        if (len - i - 1 < 0 || len - i - 2 < 0 || chess_list[len - i - 1] != now)
            break;
        if (chess_list[len - i - 1] == now && chess_list[len - i - 2] == 0)
        {
            switch (i)
            {
            case 0:
                res += die_1;
                break;
            case 1:
                res += die_2;
                break;
            case 2:
                res += die_3;
                break;
            case 3:
                res += die_4;
            }
            break;
        }
    }
    return res;
}

int evaluation(int chessboard[][15], int now_turn)
{
    now = now_turn;
    int res = 0;
    for (int i = 0; i < 15; i++)
    {
        res += check(chessboard[i], 15);
        if (i != 0 && i != 14)
        {
            for (int j = 0; j < 15 - i; j++)
                temp[j] = chessboard[i + j][j];
            res += check(temp, 15 - i);
            for (int j = 0; j <= i; j++)
                temp[j] = chessboard[i - j][j];
            res += check(temp, i + 1);
        }
    }
    for (int i = 0; i < 15; i++)
    {
        for (int j = 0; j < 15; j++)
            temp[j] = chessboard[j][i];
        res += check(temp, 15);
        for (int j = 0; j < 15 - i; j++)
            temp[j] = chessboard[j][i + j];
        res += check(temp, 15 - i);
        for (int j = 0; j <= i; j++)
            temp[j] = chessboard[j][i - j];
        res += check(temp, i + 1);
    }
    return res;
}
// int map[15][15];
// int main()
// {
//     map[7][7] = 1;
//     printf("%d\n", evaluation(map, 1));
// }