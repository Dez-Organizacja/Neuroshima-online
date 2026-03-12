#include<bits/stdc++.h>
#define ll long long

using namespace std;

template<int base, typename Node, auto _merge>
class przpkt{
    private:
    Node pusty;
    Node tree[base << 1];

    public:

    Node& idx(int x){
        return tree[x+base];
    }

    void build(){
        for(int i = base-1 ; i > 0 ; i--){
            tree[i] = _merge(tree[i<<1], tree[(i<<1)^1]); 
        }
    }

    przpkt(auto val){
        pusty = val;
        for(int i = base ; i < (base <<1); i++){
            tree[i] = val;
        }
        build();
    }

    przpkt(auto val, auto Pusty){
        pusty = Pusty;
        for(int i = base ; i < (base << 1); i++){
            tree[i] = val;
        }
        build();
    }

    void add(int x, Node val){
        x += base;
        tree[x] = val;
        x >>= 1;
        while(x){
            tree[x] = _merge(tree[x<<1], tree[(x<<1)^1]); 
            x >>= 1;
        }
    }
    
    Node query(int l, int r){
        l += base;
        r += base+1;
        Node lans = pusty;
        Node rans = pusty;
        while(l < r){
            if(l&1){
                lans = _merge(lans, tree[l++]);
            }
            if(r&1){
                rans = _merge(rans, tree[--r]);
            }
            l >>= 1;
            r >>= 1;
        }
        return _merge(lans, rans);
    }
};

const int MAXN = 2e0 + 7;
int tab[MAXN];

int32_t main(){
    ios_base::sync_with_stdio(false);
    cin.tie(0);

    int T = 1;
    // cin >> T;
    while(T--){
        
    }

    return 0;
}
