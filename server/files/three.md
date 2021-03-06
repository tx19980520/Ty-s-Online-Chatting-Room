# 三个算法的简介——SPFA，SCC，匈牙利算法

所有的代码均可用，放在了本人的github中，链接放在下方：

https://github.com/tx19980520/Implement-the-algorithm-with-c--

## SPFA

在我们的有向图单源最短路径的问题中，我们基础的是可以使用dijstra算法得到答案，但是dijkstra算法不能解决负权环问题和，甚至连拥有负权都不能保证得到正确答案（部分不影响选择的绝对值相对很小的负权是没有问题的）。这个时候我们会想到替代的方法，我们首先会想到Floyd算法，能包容负权，在一定程度上的改造还能判断负权环的存在（对角线上的值可以改变，对角线表示自己到自己的距离，结果发现有一个负数，则肯定有负环。），但这时间的代价是输入的三次方，这是非常大的，因而我们在这里讲SPFA算法并加上了SLF的优化。

SPFA分为DFS和BFS，从判断负权环的角度，DFS在判断负环上是不稳定的，我们这个地方讲的方法是BFS。

在这个地方我们需要的数据结构有：

1.一个队列（SLF优化需要双向队列deque）

2.一个邻接矩阵或者一个邻接表来表示图的基本信息（源代码中我单独还写了一个final来储存源点到各点的距离）

3.一个now_in[]，记录现在是否在队列中，在入队出队的时候记得记录

放入队列是什么，是我们图中的点的序号，什么样的点能够进入队列呢：

1.能使得源点到某个某个其他的点的距离减少

2.你本来就不在队列里面（使用now_in判断）

满足这两点即可入队。

我们的在数据预处理之后，我们的主要部分为一个不断出队入队，最后整个程序只有两个出口，第一，我们的队列里面没有元素了，整个图处理完毕，输出答案就可以结束了。第二，其中存在负权环。

负权环怎么判断，只要有一个点入队n次，那就一定有负权环。这个道理我们简单的理解下，如果有一个环，你在里面跑了一圈，最后你的路径大小变小了，那从贪心的角度来讲，那我肯定愿意在这个环里面无穷的走下去，那肯定其中环内的各个点会被遍历无穷次，实际上我们说限制为入队n次，你只要找一个比n大的数都可以，只是时间上并不是最优的。

## scc

SCC(strongly connected component)强连通子图，基本的意思是在于遍历一个图，得到各个强连通分量，我们先解释一下什么叫强连通分量，即一个子图（树），在这个子图（树）当中，任意找两个点，他们都可以找到一条路，使两者连通。我们这个地方只讲tarjan算法和kosaraju算法。

###tarjan算法

该算法要求的数据结构：

1.stack一个，作为一个全局变量

2.一个邻接表或者邻接矩阵，用于储存图的基本信息

3.step[]储存遍历到某点的步数

4.deep[]储存你和你子树中能找到的最小的deep，如果没有，则deep[i] = step[i]（这是明显的递归定义）

这个地方强调一下，我们的step是遍历顺序定的，不会被更改，只有deep会被改变。

第四点已经非常明显的告诉我们这个算法是递归实现的，他的基础是DFS，我们的在每一个层次上要做的事情为

1.确立好你的step[i]，初始化deep[i] = step[i]，将该点入栈。

2.开始遍历你的子树，并通过他们的deep的改变来改变自己的deep，deep为子树和你自己本身最小的。

3.如果在2之后还是发现deep[i] == step[i]，进行栈的pop

PS：这个地方要注意到一个问题，可能图中有点没有被访问到（甚至有森林的可能），这一定要注意保证每个点都被visit到，当一次dfs退出之后，一定要记得检查visit数组里面还有没有值为0，如果有就以之开始下一次dfs，知道全图被完全遍历。

我们来具体说一下这个出栈的问题，这里贴一段代码：

```cpp
  if(deep[index] == step[index])//根据画图的得到的经验是，pop到该元素出栈为止
  {
    cout<< "a strongly connected component:" << endl;
    while(s.top() != index)
    {
        int tmp = s.top();
        cout << tmp << "  ";
        s.pop();
        had_in[tmp] = 1;
        now_in[tmp] = 0;
    }
    int tmp = s.top();
    cout << tmp << "  ";
    s.pop();
    had_in[tmp] = 1;
    now_in[tmp] = 0;
  }
```

我们退栈只会在```deep[index] == step[index]```被调用，入栈只会在递归最开始的时候，退栈退到什么程度呢，退到栈顶是该元素，然后再退一次栈（pop该index），则你前面pop的一切的点，就组成了一个强连通分量。

###kosaraju算法

该算法据说栈可能炸，我们的栈空间需求稳定的需要n，但我们的tarjan中间可以看到，我们中途可以弹栈，所以栈的最坏情况（整个图是强联通的）才是n，但这个方法的理解很简单。

该算法需要的数据结构：

1.一个全局栈，所有点都需要进栈，栈底的元素最先被遍历，该图的遍历是后序遍历（子树优先）。

2.一个visit数组，这个数组需要用到两次，记录是否被遍历，两次中间需要重新初始化。

3.deep[]，用于记录dfs的次序。

首先随机找一个点开始进行dfs（我的算法里面提供的是对visit数组顺序遍历，如果没有被visit，就开始对其dfs，dfs过程中会改变visit数组中的值）

说有点都进栈之后，我再一次初始化了我的visit数组，为了接下来的dfs做准备。

所有点都进栈之后，从栈顶的点开始DFS，同样的，DFS过程将改变visit数组的值，被遍历过的点i,visit[i] = 1，当一个点DFS进行完毕或者其visit数组中对应的值在遍历前已经为一，则弹栈。这一小部分的代码如下：

```c++
vector<int>scc //用于记录每一个强连通子图，方便在后期输出
while(!s.empty())//栈空则退出该循环
  {
    if(visit[top] ==1)//如果该点已经被遍历过，则直接弹栈，回到循环头
    {
      s.pop();
      top = s.top();
      continue;
    }
    redfs(top);
    cout<< "There is an scc:" << endl;
    for(int i=0;i<scc.size();++i)
    {
      cout<< scc[i]<<" ";
    }
    cout << endl;
    scc.clear();
    s.pop();
    top = s.top();
  }
```

## 匈牙利算法

匈牙利算法是一个匹配问题，基本的问题阐述为，有AB两个集合，A中的元素和B中的部分（可能是全部）元素之间有联系，问最多能匹配出多少组有联系。

这个问题主要是得到最后的匹配个数，因为可能匹配的最终具体结果可能有变化，想要得出所有解的话一定是一个n！复杂度的东西（在找到最大答案之后得回溯）。

这个算法的实现的本质是‘“以后为重，先满足后面元素”。是一个不断扩展和改变子解的过程。我们以A集合的元素来看这个问题，则问题①A中n个元素匹配B中n个元素的最大匹配度求解 的子问题是 问题②A中n-1个元素匹配B中n个元素的最大匹配度求解。

如何理解先满足后面的元素，即如果A中的后面元素a想与B中元素b配对，如果元素b之前没有进行过配对，则直接配对，进行下一个问题；如果元素b之前已经是和a'配对了，则a'取消与b配对，另寻其他元素，这个过程一直重复，最后该问题解决。我们对父问题继续求解。