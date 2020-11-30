#include <vector>
#include <cstring>
#include <cstdio>
#include <stdlib.h>
#include "../head_file/evaluation.h"
#include "../head_file/AB_serach.h"
#include "../head_file/Get_position.h"
#define INF 0x3f3f3f3f
using namespace std;

int dir[4][2] = {0, 1, 0, -1, 1, 0, -1, 0};

int ab_search(int maxdepth, int alpha, int beta, int now_turn, int chessboard[][15])
{
    int cnt;
    chess_pos list[50];
    if (maxdepth == 0)
        return evaluation(chessboard, now_turn) - evaluation(chessboard, -now_turn) * 2;
    for (int i = 0; i < 15; i++)
    {
        for (int j = 0; j < 15; j++)
        {
            if (chessboard[i][j] != 0)
                continue;
            chessboard[i][j] = now_turn;
            int v = -ab_search(maxdepth - 1, -beta, -alpha, -now_turn, chessboard);
            chessboard[i][j] = 0;
            if (v >= beta)
                return beta;
            if (v > alpha)
                alpha = v;
        }
    }
    return alpha;
}

void begin_search(int chessboard[][15], int now_turn)
{
    int best = -INF;
    int px = 0, py = 0;
    for (int i = 0; i < 15; i++)
    {
        for (int j = 0; j < 15; j++)
        {
            if (chessboard[i][j] != 0)
                continue;
            if ((rand() % 10) == 1)
            {
                chessboard[i][j] = now_turn;
                int v = ab_search(2, -INF, INF, now_turn, chessboard);
                if (best < v)
                {
                    best = v;
                    px = i, py = j;
                }
                chessboard[i][j] = 0;
            }
        }
    }
    printf("best==%d\n", best);
    chessboard[px][py] = now_turn;
    return;
}

int main()
{
    int chessboard[15][15];
    memset(chessboard, 0, sizeof chessboard);
    int a, b;
    while (~scanf("%d%d", &a, &b))
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
                    printf(".");
                else if (chessboard[i][j] == -1)
                    printf("#");
                else
                    printf("?");
            }
            printf("\n");
        }
        printf("\n");
    }
}
