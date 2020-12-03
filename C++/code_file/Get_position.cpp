#include <vector>
#include <algorithm>
#include <cstdio>
#include "../head_file/Get_position.h"
#include "../head_file/evaluation.h"
using namespace std;
bool pos_vis[125][125];
int dir_8[8][2] = {0, -1, 0, 1, 1, 0, -1, 0, 1, 1, 1, -1, -1, 1, -1, -1};
void get_position(int chessboard[][15], point position[], int &cnt)
{
    for (int i = 0; i < 15; i++)
    {
        for (int j = 0; j < 15; j++)
        {
            if (chessboard[i][j] != 0)
            {
                for (int k = 0; k < 8; k++)
                {
                    int nx = i + dir_8[k][0], ny = j + dir_8[k][1];
                    if (nx < 0 || nx >= 15 || ny < 0 || ny >= 15)
                        continue;
                    if (!pos_vis[nx][ny] && chessboard[nx][ny] == 0)
                    {
                        pos_vis[nx][ny] = 1;
                        position[cnt].x = nx;
                        position[cnt].y = ny;
                        cnt++;
                        if (cnt >= 25)
                        {
                            for (int l = 0; l < cnt; l++)
                                pos_vis[position[l].x][position[l].y] = 0;
                            return;
                        }
                    }
                }
            }
        }
    }
    for (int l = 0; l < cnt; l++)
        pos_vis[position[l].x][position[l].y] = 0;
}