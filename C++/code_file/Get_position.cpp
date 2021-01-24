#include <algorithm>
#include "../head_file/Get_position.h"
#include "../head_file/evaluation.h"
using namespace std;

int dir_8[8][2] = {0, -1, 0, 1, 1, 0, -1, 0, 1, 1, 1, -1, -1, 1, -1, -1};
// point temp_pos[225];
// int pos_list[15];

bool cmp(const point &a, const point &b)
{
    return a.v > b.v;
}
void get_position(int chessboard[][15], point position[], int &cnt, int &now_turn)
{
    for (int i = 0; i < 15 && cnt < 75; i++)
    {
        for (int j = 0; j < 15 && cnt <75; j++)
        {
            if (chessboard[i][j] == 0)
            {
                for (int k = 0; k < 8; k++)
                {
                    int nx = i + dir_8[k][0], ny = j + dir_8[k][1];
                    if (nx < 0 || nx >= 15 || ny < 0 || ny >= 15)
                        continue;
                    if (chessboard[nx][ny] != 0)
                    {
                        position[cnt].x = i, position[cnt].y = j;
                        cnt++;
                        break;
                    }
                }
            }
        }
    }
}