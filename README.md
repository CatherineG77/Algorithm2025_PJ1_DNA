
23307130412
2025/3/4
解题思路：
   题目要求寻找query中最长(较长的覆盖较短的)重复片段，找到query和reference不一样之处，返回重复片段多余重复次数，片段在reference中首次结束下标。
    解题过程中，通过多次试错发现能得到正确答案的方法是：现在query中寻找最长重复片段，然后再在reference中尝试对应，把多出的部分作为结果输出。

算法描述：
    （以下实现算法思路描述均为伪代码）
    首先，由于题目要求可能在reference的互补链中找到重复片段，定义一个获得符合要求的reference_comp字符串的函数complement(s)：
def complement(s):
    # 建立字典使得 A <-> T, C <-> G，其中{'原字符':'匹配的字符'}
    comp <- {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    # 对 s 中的每个字符 ch，从字典 comp 中取出其对应的倒序互补字符
    answer <- ""
    for ch in s:
        answer <- comp[ch] + answer
    return answer

然后通过建立dp数组方法分别建立 
(1) query和reference每个对应字符开头的最长匹配字符串长度的二维表格 compute_dp(query, ref); 
(2)query自身不同字符开头最长匹配字符串长度二维表格 build_lcp_dp(query, m)，注意由于m中重复子串最长长度不会超过m，所以在填表时候j变量的上限取(n - 1)和(i + m)中更小的一个，使得最终函数的复杂度保持O(mn)

得到的dp表填表过程时间复杂度O(xy)
get_dp(x, y):
    dp[y + 1][x + 1] 初始化全0 
    # 保证dp[i+1][j+1]不违法,并进行表格初始化

    # 从后向前填表，保证前一层得到的结果可以用到下一层
    i from y - 1 downto 0:
        j from x - 1 downto 0:
            if string1[i] = string2[j]:
                dp[i][j] <- dp[i+1][j+1] + 1
            else:
                dp[i][j] <- 0
    return dp

    然后先找出query中所有最长重复片段find_repeated_segments(query),返回一个列表，每个元素为元组 (start, end, unit,count);
    其中：
      - start: 该重复片段在 query 中的起始位置（0-indexed）
      - end: 重复片段的结束位置（不包括该下标），即 start + count * len(unit)
      - unit: 重复单位字符串
      - count: 连续重复的次数（至少 >= 2）
    过程中利用 dp 表寻找 query 中所有连续重复出现的片段。如果有候选片段在位置上重合，则取覆盖该区间最长的一个。
    该部分时间复杂度为O(mn)。

def find_repeated_segments(query, m):
    # 基础变量赋值准备
    Q <- query
    n <- len(query)
    R <- reference
    R_comp <- complement(reference)

    # 预处理 dp 表
    dp  <- build_lcp_dp(query, m)  # 预处理 LCP 动态规划表
    segments <- []             # 存放最终结果
    i <- 0                     # 从 query 的第 0 个字符开始扫描
    
    while i < n:
        best_total <- 0      # 记录以 i 为起点时，候选重复区间的最大总长度
        best_candidate <- None  
# 初始化为None，保存最佳候选，格式为 (start, end, unit, count)
        

        # 注意：重复区间最多不超过当下i下标处的dp1[i]和dp2[i]这两行中的最大值，否则就算query中有重复在reference里也找不到对应的片段，所以:
        maxEnd = 0;
        j from 0 to (m - 1):
            maxEnd <- max{max{dp1[i][j], dp2[i][j]}, maxEnd}

        # 对于n中的每一个i，遍历从自身1开始到最长可能片段长度的L，然后利用 dp 表，用while循环判断后续每个单位是否与 unit 相同，是则count自增并继续，直到不一样
        L from 1 to maxEnd:
            unit <- query[i:i+L]  # 候选重复单位
            count <- 1  # 表示至少出现一次（就是当前位置的那个 unit）
            
            # 循环的前提是比较的最大i + count * L + L下标不超过n的范围(否则必然不成立)，条件是dp[tempIndex][tempIndex + L] >= L
            while i + count * L + L <= n and dp[i + (count - 1) * L][i + count * L] >= L:
                count += 1
            
            # 若连续重复出现至少 2 次，才更新候选（只取覆盖范围最长的）
            if count >= 2:
                total <- count * L  # total为重复区间的总长度
                if total > best_total:
                    best_total <- total     # 覆盖最长长度更新
                    best_candidate = (i, i + total, unit, count)   
 # 对应的最长候选参数组也更新
        
        if best_candidate:

            # 成功找到一个有效重复片段，则加入结果
            segments.append(best_candidate)

            # 跳过整个重复区域，从上一个best_candidate中的end处下标作为i开始下一轮，以避免与后续可能重叠的候选冲突
            i <- best_candidate[1]
        else:
            # 若当前位置未找到有效重复，则向右移动一个字符
            i += 1
    
    return segments # 返回答案元组的列表

    现在已有所有query中最长重复片段的结果集合，但打印出会发现很多是原来reference串中本身存在的片段重复，所以最后在main函数中把这些不符合答案要求的结果排除掉。
    判断方式: 每一个segment中 (end - 1) 如果超出Q和R当下已匹配(或已处理)长度，说明这一重复部分存在reference中不匹配的部分

    # 初始情况，reference(R)和query(Q)都从下标0开始比对
    indexR <- 0         # 当下开始比对到的reference中字符下标
    indexQ <- 0         # 当下开始比对到的query中字符下标

    # segments规模最差情况为O(K), (K <= n)
    for seg in segments:
        start, end, unit, count <- seg
        # 重复片段的结尾下标，比query中当下与reference中能成功匹配到的位置更后
        if end > indexQ + dp1[indexQ][indexR]:  
            temp <- end         # temp是当下剩余重复片段结束的后一位
            stop <- indexQ + dp1[indexQ][indexR]    # stop是停下标识位
            cnt = 0             # 代表不在query中匹配的片段个数，也就是重复次数

            # 当下位置小于等于重复片段开始位置start或匹配片段结束后一位stop时停止循环
            # 最坏情况复杂度O(n/K)，叠加for的循环复杂度控制在O(n)
            while temp > stop and temp > start: 
                cnt += 1
                temp -= len(unit)
            
            # 寻找R或R_comp中和片段匹配的位置结尾下标, 规模O(m)
            irange <- len(reference) - len(unit)
            index <- -1
            state <- ""
            i from 0 to (irange - 1):
                if dp1[start][i] >= len(unit):
                    state <- "no"
                    index <- i + len(unit)
                    break
                elif dp2[start][i] >= len(unit):
                    state <- "yes"
                    index <- len(reference) - i
                    break

            # 更新R中比较开始下标的条件：temp停下的位置在start之后，既有片段被包括在匹配部分，也就是stop在start之后
            if stop > start:    
                # 更新长度：现在位置减初始位置, temp - indexQ
                indexR += (temp - indexQ)

            indexQ <- end   # Q中开始匹配位置一定是匹配完的end所在

        else:   
# 虽有重复片段但全部囊括在reference里面, 直接看下一个, indexQ和indexR都不更新
            continue

在以上基础上添加符合要求的输出print语句，并用python语法改写，就得到最终的程序，详细代码可见DNA_.py文件
	算法总时间复杂度是O(mn)，空间复杂度是O(mn + n^2)

运行结果截图：
 
综上，实验结果顺利得到。
