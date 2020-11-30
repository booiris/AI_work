#include <vector>
#include <algorithm>
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
void get_position(int chessboard[][15], vector<chess_pos> &position, int now_turn)
{
    vector<node> key;
    key.clear();
    for (int i = 0; i < 15; i++)
    {
        for (int j = 0; j < 15; j++)
        {
            if (chessboard[i][j] == 0)
            {
                chessboard[i][j] = now_turn;
                int v = evaluation(chessboard, now_turn);
                key.push_back(node{i, j, v});
                chessboard[i][j] = 0;
            }
        }
    }
    sort(key.begin(), key.end());
    for (int i = 0; i < min(50, (int)key.size()); i++)
        position.push_back(chess_pos{key[i].x, key[i].y});
}
// int main()
// {
//     vector<int> asda;
// }