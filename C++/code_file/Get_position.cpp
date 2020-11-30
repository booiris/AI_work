#include <vector>
#include <algorithm>
#include <cstdio>
#include "../head_file/Get_position.h"
#include "../head_file/evaluation.h"
using namespace std;
struct node
{
    int x, y, v;
    bool operator<(const node &a) const
    {
        return v > a.v;
    }
};
void get_position(int chessboard[][15], chess_pos position[], int &cnt, int now_turn)
{
    for (int i = 0; i < 15; i++)
    {
        for (int j = 0; j < 15; j++)
        {
            if (chessboard[i][j] == -now_turn)
            {
                cnt++;
                if (cnt >= 50)
                    break;
                
            }
        }
    }
}
// int main()
// {
//     vector<int> asda;
// }