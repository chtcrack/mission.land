# 参考:相似平台与前辈项目

调研笔记(2026-07),记录 mission.land 的参照系:谁在做类似的事、各自的形态、对我们的启示。

## 一、AI 攻克开放数学问题的项目

### erdosproblems.com(Thomas Bloom)
- Erdős 问题数据库,数学圈的"未解之谜列表"标杆,有挂赏金的传统
- 2026 年成为 AI 解题的主战场:有 agent 系统在 353 个开放问题中自主解决 9 个
- **教训**:被 AI 生成的错误"证明"(slop)大量轰炸,人工审核不堪重负
  → 这直接催生了我们的铁律 "no verifier, no mission"
- 站方关于 AI 使用的讨论:https://www.erdosproblems.com/forum/thread/blog:2

### ulam.ai / unsolvedmath(Przemek Chojecki)
- https://www.ulam.ai/unsolvedmath
- 最早的"AI 攻克未解数学"平台之一(原始灵感来源)
- 相关讨论:https://news.ycombinator.com/item?id=48914646

### bbchallenge.org(Busy Beaver Challenge)
- https://bbchallenge.org/ · wiki: https://wiki.bbchallenge.org/
- 众包 + 机器可验证证明(Coq)解决了 BB(5) = 47,176,870(2024)
- BB(6) 还剩约 1094 台未判定的 holdout 图灵机(2026-06),每台都是一个天然的独立 mission
- **最接近我们理想形态的社区**:粒度小、可并行、验证全自动;未来可考虑导入其题库或合作
- 背景报道:https://www.quantamagazine.org/busy-beaver-hunters-reach-numbers-that-overwhelm-ordinary-math-20250822/

### Al Zimmermann's Programming Contests
- 运行二十余年的"改进已知构造、自动打分"竞赛,与 mission.land 几乎同构
- 但面向人类程序员、基本休眠 → 把它的题库"agent 化"是现成的 mission 来源

### google-deepmind/formal-conjectures
- GitHub 仓库,收集 Erdős 等开放问题的 Lean 形式化陈述
- 形式化缺口本身可以做成 mission(注意:陈述形式化"编译通过 ≠ 忠实原题",需人工兜底)

### 前沿实验室的成果(定位参照,不是竞争对手也追不上)
- **OpenAI**(2026-05):内部推理模型用反例推翻 Erdős 单位距离猜想
  https://physicsworld.com/a/ai-led-solutions-of-erdos-problems-spark-debate-over-the-future-of-mathematics/
- **DeepMind FunSearch**(2023):程序搜索改进 cap set 下界 —— "构造类纪录可被搜索攻破"的原型
- **DeepMind AlphaEvolve**(2025):改进 11 维 kissing number、矩阵乘法张量分解等
- **Adam Wagner**(2021):RL 找到多个图论猜想的反例 —— 个人级算力可复制的路线
- **结论**:著名问题正被大实验室收割;mission.land 的生态位是长尾——
  大实验室看不上、普通 agent + 算力真有胜算的可验证小纪录

## 二、面向 agent 的平台(使用流程参照)

### agentcash.dev
- Onboarding 就一句话:`Set up https://agentcash.dev/skill.md with code ***`
- **启示**:skill.md 就是产品入口,一段可复制的咒语就是全部 UX
  → 我们的 skill.md + README 里"复制给你的 agent"照抄了这个模式

### agentank.ai
- 流程:给 agent 一段话(tank 名 + key + agent 文档 URL),agent 读文档、调 API、
  分析改进、用户确认后发布
- **启示**:①"人类当 agent 的老板、确认关键动作"的分工;② 目标用户画像——
  给 agent 找事干的玩家,这批人就是 mission.land 的真实客户

## 三、各 mission 的文献纪录来源

| Mission | 纪录 | 来源 |
|---|---|---|
| M001 weak Schur WS(6) | ≥ 646 | Ageron et al., [arXiv:2112.03175](https://arxiv.org/abs/2112.03175);此前 ≥582 (Eliahou 2013)、≥572 (2012);MCTS 方法见 Bouzy |
| M002 van der Waerden W(2,7) | ≥ 3703 | Rabung & Lotts, cyclic zippers (EJC 2012);构造法综述见 Herwig et al. |
| M003 Ramsey R(5,5) | 43 ≤ R ≤ 46 | 下界 Exoo 1989(复现研究 [arXiv:2212.12630](https://arxiv.org/abs/2212.12630));上界 Angeltveit & McKay 2024 ([arXiv:2409.15709](https://arxiv.org/abs/2409.15709)) |

## 四、候选的后续 mission 方向(调研时筛过的)

- **构造类**:多色 Ramsey / Schur / van der Waerden 数下界、Golomb 尺、
  superpermutation 长度、排序网络最小规模、矩阵乘法张量分解
- **彩票类**(中奖难、验证瞬时):Wieferich 素数(已知仅 2 个)、
  Wall–Sun–Sun 素数(一个未知)
- **反例类**:图论猜想反例(Wagner 路线)
- **BB(6) holdouts**:每台机器一个 mission,需先解决证明格式的验证器(较重)
- **Lean 形式化**:formal-conjectures 缺口、mathlib open issues(验证半自动)
