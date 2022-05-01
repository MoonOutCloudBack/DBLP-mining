# 使用 FP-growth 挖掘 DBLP 学者关系

## 基本思路

- 解析 DBLP 的 xml 文件，以 attention 和 transformer 为关键词（python 的 str in 来筛选），只取 2017 年以后的文章。
- 把人名编码成数字。
- 一年一年来处理，认为有效的学者关系满足两点：
  - 一年内发表论文数量大于 5【支持率】。
  - 关系内任意一人记为 a，除他之外其他人记为 A，要满足 A → A+a 的【置信率】大于 0.5；注意是任意一人。
- 定义 人数=2 的关系为【合著者】，人数＞2 的关系为【团队】。
- 定义学者关系的【活跃程度】：α \* 这一堆人发表文章数量 + β / 人数 \* 求和{一堆人发表文章数量 / 每个人发表文章数量}。取 α=1，β=10。注意发表数量都是一年内的。

## 主要结论

- 研究 attention transformer 的人越来越多。
- 貌似没人能一直研究 attention transformer 超过一年，大家的研究方向变得很快。
- 好多活跃的人都是重复的，比如出现 “一个固定导师+一个可变学生” “两个固定导师+一个可变学生” “AB BC AC 都活跃” 这种 pattern，三五好友 / 整个实验室一起研究 transformer。
- 合著者发文数量上，2018年有一个激增；团队发文数量上，2019年和2021年都有激增。

## 文件列表

- py：
  - `getAuthors.py`：从 DBLP 的 xml 文件，解析得到 `authors.txt`。
  - `encodeAuthors.py`：把 `authors.txt` 编码成 `authors_encode.txt` + `author_index.txt`。
  - `fpgrowth.py`：调用 `mlxtend` 的关联规则挖掘，以及学者关系分析。
- txt：
  - `authors.txt`：年份 + title + 学者名字。
  - `authors_encode.txt`：年份 + title + 学者编码（数字）。
  - `author_index.txt`：学者编码 + 学者名字 + 这个人（一年内）总共发表数量。
- csv：
  - `result_co_authors_5_0.5.csv`：合著者的分析结果，年份 + 学者名字（tuple）+ 学者一年内发文数量 + 活跃程度。
  - `result_teams_5_0.5.csv`：团队的分析结果，格式同上。
- pdf：
  - 课程报告。


## 鸣谢

感谢这些带给我帮助的 repo：

- https://github.com/findmyway/DBLP-Coauthor
- https://github.com/sherryxiata/DBLP-CoAuthor
- https://github.com/liyi-david/dblpmining
- https://github.com/wsjfc/dblp_data_mining/
- https://github.com/LinusDietz/DBLPGraphs