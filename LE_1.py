import langextract as lx
import textwrap
import os

if("GEMINI_API_KEY" in os.environ):
    del os.environ["GEMINI_API_KEY"]

os.environ["LANGEXTRACT_API_KEY"] = ""


class lang_ex:
    def __init__(self,prompt,data,examples,model="gemini-2.5-flash"):
        self.prompt=prompt
        self.data=data
        self.examples=examples
        self.model=model
        
    def extraction(self):
        res=lx.extract(
            text_or_documents=self.data,
            prompt_description=self.prompt,
            examples=self.examples,
            model_id=self.model
        )
        return res

class is_ai_code:
    def __init__(self,code1):
        self.code=code1
    
    def validation(self):
        #Analyze the code snippet to determine if it was likely written by an AI or a Human.
        #    Extract specific syntax or comments as evidence and classify the author.
        prompt=textwrap.dedent("""\
            Analyze the code snippet to determine if it is written by an AI/LLM.
            
            Criteria for AI Code:
            - Uses standard headers (<iostream>, <vector>).
            - Uses full type names (long long instead of ll).
            - Has comments explaining steps.
            - Uses standard for-loops, not macros like f1(i,0,n).
            
            Criteria for Human/CP Code:
            - Uses <bits/stdc++.h>.
            - Uses macros (#define ll long long, #define f1...).
            - Short variable names (v, p, n, m).
            
            OUTPUT:
            Extract evidence. In attributes, set 'is_ai' to "Yes" or "No".
            """)
        
        data=self.code
        examples=[
            lx.data.ExampleData(
                text="""\
                    #include <iostream>
                    #include <vector>
                    #include <algorithm>
                    #include <numeric>
                    #include <utility>

                    // AI models typically use standard namespaces but avoid heavy macros
                    using namespace std;

                    // AI typically defines types clearly rather than using short macros like 'll' or 'vll'
                    using long_long = long long;

                    void solve() {
                    int n;
                    long_long m;

                    if (!(cin >> n >> m)) return;

                    vector<long_long> values(n);
                    vector<pair<long_long, int>> pairs_with_index(n);

                    // Reading input
                    for (int i = 0; i < n; ++i) {
                    cin >> values[i];
                    // Storing value and 1-based index
                    pairs_with_index[i] = {values[i], i + 1};
                    }

                    // Calculating validation metrics
                    long_long max_val = *max_element(values.begin(), values.end());
                    long_long sum_val = accumulate(values.begin(), values.end(), 0LL);

                    // Condition Check
                    if (m > n / 2 || (m == 0 && sum_val < 2 * max_val)) {
                    cout << -1 << endl;
                    return;
                    }

                    vector<pair<int, int>> result_edges;
                    sort(pairs_with_index.begin(), pairs_with_index.end());

                    if (m == 0) {
                    // Handling the case where m is 0
                    int left_ptr = n - 2;
                    long_long current_sum = 0;
                    long_long target = pairs_with_index[n - 1].first;

                    while (left_ptr >= 0) {
                    current_sum += pairs_with_index[left_ptr].first;
                    if (current_sum >= target) {
                        break;
                    }
                    left_ptr--;
                    }

                    // Constructing edges based on the split point
                    for (int i = 0; i < left_ptr; ++i) {
                    result_edges.push_back({pairs_with_index[i].second, pairs_with_index[i + 1].second});
                    }
                    for (int i = left_ptr; i < n - 1; ++i) {
                    result_edges.push_back({pairs_with_index[i].second, pairs_with_index[n - 1].second});
                    }

                    } else {
                    // Handling the case where m > 0
                    // Linear connection for the first segment
                    for (int i = 0; i < n - 2 * m; ++i) {
                    result_edges.push_back({pairs_with_index[i].second, pairs_with_index[i + 1].second});
                    }

                    // Pairing remaining elements from ends
                    int left = n - 2 * m;
                    int right = n - 1;
                    while (left < right) {
                    result_edges.push_back({pairs_with_index[right].second, pairs_with_index[left].second});
                    left++;
                    right--;
                    }
                    }

                    // Outputting results
                    cout << result_edges.size() << endl;
                    for (const auto& edge : result_edges) {
                    cout << edge.first << " " << edge.second << endl;
                    }
                    }

                    int main() {
                    // Fast I/O is standard in competitive programming solutions generated by AI
                    ios_base::sync_with_stdio(false);
                    cin.tie(NULL);

                    int test_cases;
                    if (cin >> test_cases) {
                    while (test_cases--) {
                    solve();
                    }
                    }
                    return 0;
                    }
                    """,
                extractions=[
                    lx.data.Extraction(
                        extraction_class="Code_Analysis",
                        extraction_text="#include <iostream>",
                        attributes={"is_ai": "Yes"}
                    )
                ] 
            ),lx.data.ExampleData(
                text="""\
                        
                    #include <bits/stdc++.h>
                    #define ll long long
                    using namespace std;

                    int main() {
                        ios::sync_with_stdio(false);
                        cin.tie(NULL);

                        string s;
                        cin >> s;
                        int n = s.size();

                        vector<int> z(n);
                        int l = 0, r = 0;

                        for (int i = 1; i < n; i++) {
                            if (i <= r)
                                z[i] = min(r - i + 1, z[i - l]);

                            while (i + z[i] < n && s[z[i]] == s[i + z[i]])
                                z[i]++;

                            if (i + z[i] - 1 > r) {
                                l = i;
                                r = i + z[i] - 1;
                            }
                        }

                        unordered_map<int, int> cnt;
                        for (int i = 1; i < n; i++) {
                            if (z[i] > 0)
                                cnt[z[i]]++;
                        }

                        for (auto &p : cnt) {
                            cout << p.first << " " << p.second << "\n";
                        }

                        return 0;
                    }
                    """,
                extractions=[
                    lx.data.Extraction(
                        extraction_class="Code_Analysis",
                        extraction_text="#include <bits/stdc++.h>",
                        attributes={"is_ai": "Yes"}
                    )
                ]
            ),
            lx.data.ExampleData(
                text="""\
                    #include<bits/stdc++.h>
                    #include <ext/pb_ds/assoc_container.hpp>
                    #include <ext/pb_ds/tree_policy.hpp>
                    using namespace std;
                    using namespace __gnu_pbds;

                    template<typename T> using ordered_set = tree<T, null_type, less<T>, rb_tree_tag, tree_order_statistics_node_update>;
                    #define ll long long
                    #define vll vector<ll>
                    #define pll pair<ll,ll>
                    #define vvll vector<vector<ll>>
                    #define maxhp priority_queue<ll>
                    #define minhp priority_queue<ll,vector<ll>,greater<ll>>
                    #define vpll vector<pair<ll, ll>>
                    #define umpll unordered_map<ll, ll>
                    #define umpcl unordered_map<char, ll>

                    #define all(v) v.begin(), v.end()
                    #define maxi(v) *max_element(all(v))
                    #define mini(v) *min_element(all(v))
                    #define rsort(v) sort(all(v),greater<ll>());
                    #define rall(v) reverse(all(v));

                    #define oo ios_base::sync_with_stdio(false); cin.tie(NULL);
                    #define mod 1000000007
                    #define f1(i, j, n) for (ll i = j; i < n; i++)
                    #define f2(i, j, n) for (ll i = j; i >= n; i--)
                    #define print1(a) cout << a << endl;
                    #define print2(a, b) cout << a << " " << b << endl;
                    #define print3(a,b,c) cout << a << " " << b << " " << c << endl;
                    #define yes cout<<"YES"<<endl;
                    #define no cout << "NO" <<endl;
                    #define line cout << endl;

                    #define pvpl(v) f1(i,0,v.size()){cout<<v[i].first<<" "<<v[i].second<<endl;}
                    #define pvl(v) f1(i,0,v.size()){cout<<v[i]<<" ";} line

                    int main() {
                        oo

                        ll size;
                        cin >> size;
                        while(size--){
                            ll n,m;
                            cin>>n>>m;

                            vll v(n);
                            vector<pair<ll,ll>> p(n);
                            f1(i,0,n){
                                cin>>v[i];  
                                p[i]={v[i],i+1};
                            }

                            if(m>n/2 || (m==0 && accumulate(all(v),0ll)<2*maxi(v))){
                                print1(-1)
                                continue;
                            }

                            vpll ans;
                            sort(all(p));
                            if(m==0){
                                ll l=n-2,r=p[n-1].first;
                                ll sum=0;
                                while(l>=0){
                                    sum+=p[l].first;
                                    if(sum>=r){
                                        break;
                                    }
                                    l--;
                                }
                                f1(i,0,l) ans.push_back({p[i].second,p[i+1].second});
                                f1(i,l,n-1) ans.push_back({p[i].second,p[n-1].second});

                            } else {

                                f1(i,0,n-2*m){
                                    ans.push_back({p[i].second,p[i+1].second});
                                }
                                ll l=n-2*m,r=n-1;
                                while(l<r){
                                    ans.push_back({p[r].second,p[l].second});
                                    l++,r--;
                                }
                            }

                            print1(ans.size())
                            pvpl(ans)
                        }
                    }
                    """,
                extractions=[
                    lx.data.Extraction(
                        extraction_class="Code_Analysis",
                        extraction_text="#define ll long long",
                        attributes={"is_ai": "No"}
                    )
                ]
            ),
        ]
        
        res=lang_ex(prompt,data,examples)
        return res.extraction()        
        
sample_code1="""\
    #include<bits/stdc++.h>
#include <ext/pb_ds/assoc_container.hpp>
#include <ext/pb_ds/tree_policy.hpp>
using namespace std;
using namespace __gnu_pbds;

template<typename T> using ordered_set = tree<T, null_type, less<T>, rb_tree_tag, tree_order_statistics_node_update>;
#define ll long long
#define vll vector<ll>
#define pll pair<ll,ll>
#define vvll vector<vector<ll>>
#define maxhp priority_queue<ll>
#define minhp priority_queue<ll,vector<ll>,greater<ll>>
#define vpll vector<pair<ll, ll>>
#define umpll unordered_map<ll, ll>
#define umpcl unordered_map<char, ll>

#define all(v) v.begin(), v.end()
#define maxi(v) *max_element(all(v))
#define mini(v) *min_element(all(v))
#define rsort(v) sort(all(v),greater<ll>());
#define rall(v) reverse(all(v));

#define oo ios_base::sync_with_stdio(false); cin.tie(NULL);
#define mod 1000000007
#define f1(i, j, n) for (ll i = j; i < n; i++)
#define f2(i, j, n) for (ll i = j; i >= n; i--)
#define print1(a) cout << a << endl;
#define print2(a, b) cout << a << " " << b << endl;
#define print3(a,b,c) cout << a << " " << b << " " << c << endl;
#define yes cout<<"YES"<<endl;
#define no cout << "NO" <<endl;
#define line cout << endl;

#define pvpl(v) f1(i,0,v.size()){cout<<v[i].first<<" "<<v[i].second<<endl;}
#define pvl(v) f1(i,0,v.size()){cout<<v[i]<<" ";} line

int main() {
    oo

    ll size;
    cin >> size;
    while(size--){
        ll n;
        cin>>n;


        vll v(n);
        f1(i,0,n) cin>>v[i];

        vll suf(n),pre(n);
        suf[n-1]=v[n-1];
        f2(i,n-2,0){
            suf[i]=suf[i+1]+v[i];
        }

        pre[0]=v[0];
        f1(i,1,n) pre[i]=pre[i-1]+abs(v[i]);
        ll ans=0;

        f1(i,0,n){
            if()
        }

        print1(ans)
        
    }
}

    """
sample_code2="""\
    
    #include <bits/stdc++.h>
    #define ll long long
    using namespace std;

    int main() {
        ios::sync_with_stdio(false);
        cin.tie(NULL);

        string s;
        cin >> s;
        int n = s.size();

        vector<int> z(n);
        int l = 0, r = 0;

        for (int i = 1; i < n; i++) {
            if (i <= r)
                z[i] = min(r - i + 1, z[i - l]);

            while (i + z[i] < n && s[z[i]] == s[i + z[i]])
                z[i]++;

            if (i + z[i] - 1 > r) {
                l = i;
                r = i + z[i] - 1;
            }
        }

        unordered_map<int, int> cnt;
        for (int i = 1; i < n; i++) {
            if (z[i] > 0)
                cnt[z[i]]++;
        }

        for (auto &p : cnt) {
            cout << p.first << " " << p.second << "\n";
        }

        return 0;
    }

    """

test1=is_ai_code(sample_code2)
result=test1.validation()

print("Test 1 Results:",result.extractions[0].attributes.get("is_ai", "Unknown"))