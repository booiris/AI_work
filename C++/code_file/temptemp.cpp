#include <iostream>  
#include <algorithm>  
#include<cstdio>  
#include<cmath>  
#include<cstring>  
#include<vector>
using namespace std;  
int map[20], cnt;//cnt 走了几条边  
const int INF = 1e8;  
void addline(int x, int y)  
{  
    if ((x == 1 && y == 2) || (x == 2 && y == 1))map[0] = 1;  
    if ((x == 2 && y == 3) || (x == 3 && y == 2))map[1] = 1;  
    if ((x == 1 && y == 3) || (x == 3 && y == 1))map[2] = 1;  
    if ((x == 2 && y == 4) || (x == 4 && y == 2))map[3] = 1;  
    if ((x == 2 && y == 5) || (x == 5 && y == 2))map[4] = 1;  
    if ((x == 4 && y == 5) || (x == 5 && y == 4))map[5] = 1;  
    if ((x == 3 && y == 5) || (x == 5 && y == 3))map[6] = 1;  
    if ((x == 3 && y == 6) || (x == 6 && y == 3))map[7] = 1;  
    if ((x == 5 && y == 6) || (x == 6 && y == 5))map[8] = 1;  
    if ((x == 4 && y == 7) || (x == 7 && y == 4))map[9] = 1;  
    if ((x == 4 && y == 8) || (x == 8 && y == 4))map[10] = 1;  
    if ((x == 7 && y == 8) || (x == 8 && y == 7))map[11] = 1;  
    if ((x == 5 && y == 9) || (x == 9 && y == 5))map[12] = 1;  
    if ((x == 5 && y == 8) || (x == 8 && y == 5))map[13] = 1;  
    if ((x == 8 && y == 9) || (x == 9 && y == 8))map[14] = 1;  
    if ((x == 6 && y == 9) || (x == 9 && y == 6))map[15] = 1;  
    if ((x == 9 && y == 10) || (x == 10 && y == 9))map[16] = 1;  
    if ((x == 6 && y == 10) || (x == 10 && y == 6))map[17] = 1;  
}  
int check()  
{  
    int num=0;  
    if (map[0] && map[1] && map[2])num++;  
    if (map[3] && map[4] && map[5])num++;  
    if (map[6] && map[7] && map[8])num++;  
    if (map[9] && map[10] && map[11])num++;  
    if (map[12] && map[13] && map[14])num++;  
    if (map[15] && map[16] && map[17])num++;  
    if (map[1] && map[4] && map[6])num++;  
    if (map[5] && map[10] && map[13])num++;  
    if (map[8] && map[12] && map[15])num++;  
    return num;  
}  
int alphabeta(int depth, int alpha, int beta, int player, int num,int A,int B)  
{  
    int val;  
    if (cnt == 18)  
        return player == 1 ? B - A : A - B;  
    if (A >= 5)  
        return player == 1 ? -1 : 1;  
    if (B >= 5)  
        return player == 1 ? 1 : -1;  
    for (int i = 0; i < 18; i++)  
    {  
        if (map[i] == 1)continue;  
        map[i] = 1;  
        cnt++;  
        int temp = check() - num;  
        if (temp > 0)  
        {  
            if (player == 0)  
            {  
                val = alphabeta( depth+1,alpha, beta, player, num + temp,A+temp,B);  
            }  
            else  
            {  
                val = alphabeta( depth+1,alpha, beta, player, num + temp,A,B+temp);  
            }  
        }  
        else  
        {  
            val = -alphabeta(depth+1,-beta, -alpha,1- player, num,A,B);  
        }  
        cnt--;  
        map[i] = 0;  
        if (val >= beta)  
        {  
            return beta;  
        }  
        if (val > alpha)  
        {  
            alpha = val;  
        }  
    }  
    return alpha;  
}  
int main()  
{

    int t;  
    scanf("%d", &t);  
    int Case = 0;  
    while (t--)  
    {  
        int n;  
        Case++;  
        scanf("%d", &n);  
        memset(map, 0, sizeof map);  
        cnt = n;  
        int player = 0;  
        int num = 0;  
        int A =0, B = 0;  
        while (n--)  
        {     
            int x, y;  
            scanf("%d%d", &x, &y);  
            addline(x, y);  
            int temp = check();  
            if (temp > num)  
            {  
                if (player == 0)A += (temp - num);  
                else B += (temp - num);  
                num = temp;  
            }  
            else player = 1 - player;  
        }  
        int ans=alphabeta(0,-INF, INF, player, num,A,B);  
        if (player == 1 && ans < 0 || player == 0 && ans>0)  
            printf("Game %d: A wins.\n", Case);  
        else  
            printf("Game %d: B wins.\n", Case);  
    }  
}  