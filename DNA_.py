def complement(s):
    # 返回字符串 s 的互补串，即 A<->T, C<->G
    comp = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    answer = ""
    for ch in s:
        answer = comp[ch] + answer
    return answer


def compute_dp(query, ref):
    # 计算 dp 数组，得到从query的i下标开头和ref的j下标开头的最长公共前缀长度表格"""
    n, m = len(query), len(ref)
    dp = [[0] * (m + 1) for _ in range(n + 1)]  
    # 从后向前填表
    for i in range(n - 1, -1, -1):
        for j in range(m - 1, -1, -1):
            if query[i] == ref[j]:
                dp[i][j] = dp[i+1][j+1] + 1
            else:
                dp[i][j] = 0
    return dp

def build_lcp_dp(query, m):
    # 构造 dp 数组，其中 dp[i][j] 表示 query[i:] 与 query[j:] 的最长公共前缀长度。

    n = len(query)
    dp = [[0] * (n + 1) for _ in range(n + 1)]
    
    maxEnd = 0

    for i in range(n - 1, -1, -1):
        if (i + m) > (n - 1):
            maxEnd = n - 1
        else:
            maxEnd = i + m
        for j in range(maxEnd, i, -1):  
            if query[i] == query[j]:
                dp[i][j] = dp[i + 1][j + 1] + 1
            else:
                dp[i][j] = 0
    return dp

def find_repeated_segments(query, m):
    global dp1, dp2
    Q = query
    R_comp = complement(R)
    n = len(query)

    dp = build_lcp_dp(query, m) 
    segments = []            
    i = 0                     
    
    while i < n:
        best_total = 0      
        best_candidate = None  
        index = -1
        state = ""

        maxEnd = 0
        # 保证每个尝试长度在dp1或dp2中能有匹配
        for j in range(m + 1):
            if dp1[i][j] > dp2[i][j]:
                if dp1[i][j] > maxEnd:
                    maxEnd = dp1[i][j]
            else:
                if dp2[i][j] > maxEnd:
                    maxEnd = dp2[i][j]


        for L in range(1, maxEnd + 1):
            unit = query[i:i+L]  
            count = 1  
            
            # 利用 dp 表判断后续每个单位是否与 unit 相同
            # 当 dp[x][y] >= L 时，表示从 x 和 y 开始的 L 个字符相同
            while i + count * L + L <= n and dp[i + (count - 1) * L][i + count * L] >= L:
                count += 1
            
            # 若连续重复出现至少 2 次，则只取覆盖范围最长的
            if count >= 2:
                total = count * L 
                if total >= best_total:
                    best_total = total
                    best_candidate = (i, i + total, unit, count)
        
        if best_candidate:
            segments.append(best_candidate)
            i = best_candidate[1]
        else:
            i += 1
    
    return segments

if __name__ == '__main__':
    # 示例 query 字符串
    reference = "CTGCAACGTTCGTGGTTCATGTTTGAGCGATAGGCCGAAACTAACCGTGCATGCAACGTTAGTGGATCATTGTGGAACTATAGACTCAAACTAAGCGAGCTTGCAACGTTAGTGGACCCTTTTTGAGCTATAGACGAAAACGGACCGAGGCTGCAAGGTTAGTGGATCATTTTTCAGTTTTAGACACAAACAAACCGAGCCATCAACGTTAGTCGATCATTTTTGTGCTATTGACCATATCTCAGCGAGCCTGCAACGTGAGTGGATCATTCTTGAGCTCTGGACCAAATCTAACCGTGCCAGCAACGCTAGTGGATAATTTTGTTGCTATAGACCAACACTAATCGAGACTGCCTCGTTAGTGCATCATTTTTGCGCCATAGACCATAGCTAAGCGAGCCTTACCATCGGACCTCCACGAATCTGAAAAGTTTTAATTTCCGAGCGATACTTACGACCGGACCTCCACGAATCAGAAAGGGTTCACTATCCGCTCGATACATACGATCGGACCTCCACGACTCTGTAAGGTTTCAAAATCCGCACGATAGTTACGACCGTACCTCTACGAATCTATAAGGTTTCAATTTCCGCTGGATCCTTACGATCGGACCTCCTCGAATCTGCAAGGTTTCAATATCCGCTCAATGGTTACGGACGGACCTCCACGCATCTTAAAGGTTAAAATAGGCGCTCGGTACTTACGATCGGACCTCTCCGAATCTCAAAGGTTTCAATATCCGCTTGATACTTACGATCGCAACACCACGGATCTGAAAGGTTTCAATATCCACTCTATA"

    
    query = "CTGCAACGTTCGTGGTTCATGTTTGAGCGATAGGCCGAAACTAACCGTGCATGCAACGTTAGTGGATCATTGTGGAACTATAGACTCAAACTAAGCGAGCTTGCAACGTTAGTGGACCCTTTTTGAGCTATAGACGAAAACGGACCGAGGCTGCAAGGTTAGTGGATCATTTTTCAGTTTTAGACACAAACAAACCGAGCCATCAACGTTAGTCGATCATTTTTGTGCTATTGACCATATCTCAGCGAGCCTGCAACGTGAGTGGATCATTCTTGAGCTCTGGACCAAATCTAACCGTGCCAGCAACGCTAGTGGATAATTTTGTTGCTATAGACCAACACTAATCGAGACTGCCTCGTTAGTGCATCATTTTTGCGCCATAGACCATAGCTAAGCGAGCCTGCCTCGTTAGTGCATCATTTTTGCGCCATAGACCATAGCTAAGCGAGCCTGCCTCGTTAGTGCATCATTTTTGCGCCATAGACCATAGCTAAGCGAGCCTGCCTCGTTAGTGCATCATTTTTGCGCCATAGACCATAGCTAAGCGAGCCTGCCTCGTTAGTGCATCATTTTTGCGCCATAGACCATAGCTAAGCGAGCTAGACCAACACTAATCGAGACTGCCTCGTTAGTGCATCATTTTTGCGCCATAGACCATAGCTAAGCGAGCTAGACCAACACTAATCGAGACTGCCTCGTTAGTGCATCATTTTTGCGCCATAGACCATAGCTAAGCGAGCTAGACCAACACTAATCGAGACTGCCTCGTTAGTGCATCATTTTTGCGCCATAGACCATAGCTAAGCGAGCGCTCGCTTAGCTATGGTCTATGGCGCAAAAATGATGCACTAACGAGGCAGTCTCGATTAGTGTTGGTCTATAGCAACAAAATTATCCACTAGCGTTGCTGGCTCGCTTAGCTATGGTCTATGGCGCAAAAATGATGCACTAACGAGGCAGTCTCGATTAGTGTTGGTCTATAGCAACAAAATTATCCACTAGCGTTGCTGCTTACCATCGGACCTCCACGAATCTGAAAAGTTTTAATTTCCGAGCGATACTTACGACCGGACCTCCACGAATCAGAAAGGGTTCACTATCCGCTCGATACATACGATCGGACCTCCACGACTCTGTAAGGTTTCAAAATCCGCACGATAGTTACGACCGTACCTCTACGAATCTATAAGGTTTCAATTTCCGCTGGATCCTTACGATCGGACCTCCTCGAATCTGCAAGGTTTCAATATCCGCTCAATGGTTACGGACGGACCTCCACGCATCTTAAAGGTTAAAATAGGCGCTCGGTACTTACGATCGGACCTCTCCGAATCTCAAAGGTTTCAATATCCGCTTGATACTTACGATCGCAACACCACGGATCTGAAAGGTTTCAATATCCACTCTATA"

    R = reference
    m = len(R)
    Q = query
    n = len(Q)
    R_comp = complement(R)
    dp1 = compute_dp(Q, R)      
    dp2 = compute_dp(Q, R_comp) 
    
    segments = find_repeated_segments(query, m)
    
    # 输出结果，每个候选片段的起始位置、结束位置、重复单位、重复次数
    print("重复片段结果:")
    indexR = 0
    indexQ = 0
    indexAnswer = 0
    print(f"Index\t\tPoS in REF\tRepeat Size\tRepeat Count\tInverse")
    for seg in segments:
        start, end,  unit, count = seg
        if end > indexQ + dp1[indexQ][indexR]:
            temp = end
            stop = indexQ + dp1[indexQ][indexR]
            cnt = 0
            while temp > stop and temp > start:
                cnt += 1
                temp -= len(unit)
            
            irange = len(reference) - len(unit)
            index = -1
            state = ""
            for i in range (irange):
                if dp1[start][i] >= len(unit):
                    state = "no"
                    index = i + len(unit)
                    break
                elif dp2[start][i] >= len(unit):
                    state = "yes"
                    index = len(reference) - i
                    break
            indexAnswer += 1
            print(f"{indexAnswer}\t\t{index}\t\t{len(unit)}\t\t{cnt}\t\t{state}")
            if stop > start:
                indexR += (temp - indexQ)
            indexQ = end
        else:
            continue