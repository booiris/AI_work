#include <stdlib.h>
#include <cstdio>
#include "../head_file/evaluation.h"

int temp[15];
int check_cnt(int part[], int len, int &now)
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
    else if (part[0] == now || part[len - 1] == now)
        return 0;
    else
        return 2;
}
int check(int chess_list[], int len, int &now)
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
        int flag = check_cnt(&chess_list[i], 6, now);
        if (flag == 1)
            res += alive_4;
        if (flag == 2)
            res += die_4;
    }
    for (int i = 0; i < len; i++)
    {
        if (i + 5 >= len)
            break;
        int flag = check_cnt(&chess_list[i], 5, now);
        if (flag == 1)
            res += alive_3;
        if (flag == 2)
            res += die_3;
    }
    for (int i = 0; i < len; i++)
    {
        if (i + 4 >= len)
            break;
        int flag = check_cnt(&chess_list[i], 4, now);
        if (flag == 1)
            res += alive_2;
        if (flag == 2)
            res += die_2;
    }
    for (int i = 1; i < len - 1; i++)
    {
        if (i + 3 >= len)
            break;
        int flag = check_cnt(&chess_list[i], 3, now);
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
    int res = 0;
    for (int i = 0; i < 15; i++)
    {
        res += check(chessboard[i], 15, now_turn);
        for (int j = 0; j < 15; j++)
            temp[j] = chessboard[j][i];
        res += check(temp, 15, now_turn);
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
                temp[j] = chessboard[j][i - j];
            }
            res += check(temp, j, now_turn);
        }
        if (i != 0)
        {
            for (j = 0; j < 15; j++)
            {
                if (i + j >= 15)
                    break;
                temp[j] = chessboard[j][i + j];
            }
            res += check(temp, j, now_turn);
        }
    }
    for (int i = 0; i < 15; i++)
    {
        int j;
        for (j = 0; j < 15; j++)
        {
            if (i - j < 0)
                break;
            temp[j] = chessboard[14 - j][i - j];
        }
        res += check(temp, j, now_turn);
        for (j = 0; j < 15; j++)
        {
            if (i + j >= 15)
                break;
            temp[j] = chessboard[14 - j][i + j];
        }
        res += check(temp, j, now_turn);
    }
    return res;
}
// int map[15][15];
// int main()
// {
//     map[7][7] = 1;
//     map[7][8] = -1;
//     map[7][9] = -1;
//     map[7][10] = -1;
//     map[7][11] = -1;
//     map[7][12] = -1;
//     printf("%d\n", evaluation(map, -1));
// }