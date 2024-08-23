def topological_sort(n, dependencies):
    # 构建图的邻接表和入度表  
    graph = {i: [] for i in range(1, n + 1)}
    in_degree = {i: 0 for i in range(1, n + 1)}
    for u, v in dependencies:
        graph[v].append(u)
        in_degree[u] += 1

        # 找到所有入度为0的节点
    queue = [i for i in range(1, n + 1) if in_degree[i] == 0]
    result = []

    # Kahn算法进行拓扑排序  
    while queue:
        u = queue.pop(0)
        result.append(u)
        for v in graph[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)

                # 检查是否所有节点都被访问（即图是否是有向无环图）
    if len(result) != n:
        return "存在环，无法进行拓扑排序"

    return result


# 读取输入
n = int(input().strip())
dependencies = []
for _ in range(n):
    u, v = map(int, input().strip().split())
    dependencies.append((u, v))

# 执行拓扑排序并输出结果  
result = topological_sort(n, dependencies)
print(' '.join(map(str, result)))

# 测试样例  
# 假设输入为：  
# 2  
# 1 2  
# 2 3  
# 输出应为：  
# 3 2 1