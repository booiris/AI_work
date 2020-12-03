#include <vector>
#include <cstring>
#include <cstdio>
#include <stdlib.h>
#include "../head_file/evaluation.h"
#include "../head_file/AB_serach.h"
#include "../head_file/Get_position.h"
#define INF 0x3f3f3f3f
int t = INF >> 1;
using namespace std;
int dir8[8][2] = {0, -1, 0, 1, 1, 0, -1, 0, 1, 1, 1, -1, -1, 1, -1, -1};
int ab_search(int maxdepth, int alpha, int beta, int now_turn, int chessboard[][15])
{
    int cnt = 0;
    point list[25];
    get_position(chessboard, list, cnt);
    if (maxdepth == 0 || cnt == 0)
        return evaluation(chessboard, now_turn);
    for (int i = 0; i < cnt; i++)
    {
        point &temp = list[i];
        chessboard[temp.x][temp.y] = now_turn;
        int v = -ab_search(maxdepth - 1, -beta, -alpha, -now_turn, chessboard);
        chessboard[temp.x][temp.y] = 0;
        if (v >= beta)
            return beta;
        if (v > alpha)
            alpha = v;
    }
    return alpha;
}
bool chess_vis[15][15];
void begin_search(int chessboard[][15], int now_turn)
{
    int best = -INF;
    int px = 0, py = 0;
    memset(chess_vis, 0, sizeof chess_vis);
    for (int i = 0; i < 15; i++)
    {
        for (int j = 0; j < 15; j++)
        {
            if (chessboard[i][j] != 0)
            {
                for (int k = 0; k < 8; k++)
                {
                    int nx = i + dir8[k][0], ny = j + dir8[k][1];
                    if (nx < 0 || nx >= 15 || ny < 0 || ny >= 15)
                        continue;
                    if (!chess_vis[nx][ny] && chessboard[nx][ny] == 0)
                    {
                        chess_vis[nx][ny] = 1;
                        int v = ab_search(2, -INF, INF, -1, chessboard);
                        if (best < v)
                        {
                            best = v;
                            px = nx, py = ny;
                        }
                    }
                }
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
