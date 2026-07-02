import os, re

src = r"E:\BaiduNetdiskDownload\老梅面试\【07】老梅公考面试理论课【梅矛盾2.5版】\md笔记"
out = r"E:\BaiduNetdiskDownload\老梅面试\面试知识库\07_梅矛盾2.5"

section_types = ['核心主题','关键概念','核心观点','核心原理','常见误区','关联知识','行动工具箱','课后练习','答题示范']
remove_sections = ['操作实录','关键话术','案例素材']

# Step 1: Re-clean from source
files = sorted(os.listdir(src))
for f in files:
    if not f.endswith('.md'): continue
    src_path = os.path.join(src, f)
    content = open(src_path, encoding='utf-8').read()

    raw_sections = []
    cur_title = ''
    cur_body = []
    for line in content.split('\n'):
        if re.match(r'^##\s+', line):
            if cur_body:
                raw_sections.append((cur_title.strip(), '\n'.join(cur_body).strip()))
            cur_title = line.strip()
            cur_body = []
        else:
            cur_body.append(line)
    if cur_body:
        raw_sections.append((cur_title.strip(), '\n'.join(cur_body).strip()))

    kept = {}
    for title, body in raw_sections:
        if any(s in title for s in remove_sections):
            continue
        matched = None
        for t in section_types:
            if t in title:
                matched = t
                break
        if matched:
            kept[matched] = (title, body)
        elif title:
            kept[title] = (title, body)

    fname = f.replace('.md', '').strip()
    out_lines = [f"# {fname}\n", f"> 来源：【07】老梅公考面试理论课（梅矛盾2.5版）\n"]

    for stype in section_types:
        if stype in kept:
            title, body = kept[stype]
            new_title = '### ' + title.replace('## ', '')
            out_lines.append(f"\n{new_title}\n")
            body = re.sub(r'^#### ', '##### ', body, flags=re.MULTILINE)
            body = re.sub(r'^### ', '#### ', body, flags=re.MULTILINE)
            body = re.sub(r'^## ', '### ', body, flags=re.MULTILINE)
            out_lines.append(body)

    for stype, (title, body) in kept.items():
        if stype not in section_types:
            new_title = '### ' + title.replace('## ', '')
            out_lines.append(f"\n{new_title}\n")
            out_lines.append(body)

    with open(os.path.join(out, f), 'w', encoding='utf-8') as fout:
        fout.write('\n'.join(out_lines))

print("Step 1: Re-cleaned 8 files.")

# Step 2: Safe answer replacement
answers = {}

# 1-总纲
answers["1-梅矛盾2.5总纲     -"] = """各位考官，社区微菜场这件事，我想从三个角度来谈。

第一，它是一个很有价值的尝试。从农民的菜地到居民的餐桌，中间要经过批发商、运输商、零售商，每个环节都加价。无人售菜柜的本质是"去中间化"——用技术手段把流通链条缩短了。价格更低了，农民收入反而可能更高了。

第二，但它也制造了新的矛盾。一个无人售菜柜立起来，周边的菜场摊贩怎么办？社区超市的生鲜区怎么办？技术赋能在带来便利的同时，也在重新分配利益。如果我们只看"便民"这一面，忽视了被冲击的那一面，政策的落地就会遇到阻力。

第三，所以评判这个政策好不好，关键不在于技术本身，而在于它有没有兼顾多元利益。比如能不能让周边摊贩也参与进来——他们负责补货和日常维护？能不能和社区超市形成互补——菜柜卖"基础款"蔬菜，超市做"品质款"？把零和博弈变成正和博弈，才是好政策。

答题完毕。"""

# 2-社会现象
answers["2-社会现象     -"] = """各位考官，青年人在网上做MBTI测试这件事，表面是个人行为，背后是结构性问题。我有三点思考。

第一，MBTI热潮折射出的是就业结构的深层矛盾。很多年轻人找到的工作并不是自己擅长的——人岗匹配度低，个人价值有限，企业效益也打折扣。从这个角度看，做MBTI虽然不一定精准，但它反映了年轻人自我认知意识的觉醒，也是一种低成本、可普及的探索方式。它的流行恰恰说明——正规的职业指导渠道没有满足需求。

第二，学校教育在这方面是有缺位的。学校虽然开设了职业指导课程，但大多流于形式——大班教学没有个性化，课程内容脱离真实职场。正因为学校不行，年轻人才转向网上测试来弥补。这提醒我们：职业指导不是"有没有"的问题，是"好不好"的问题。

第三，MBTI本身也存在不容忽视的问题。比如诱导性消费——测试免费、看结果要钱；测试的科学性在心理学界也有争议，把复杂的人简单归类为16种类型，某种程度上是在"标签化"地简化人的丰富性。这就涉及到"桥分析"——做MBTI能不能真正帮人分析优势？这座桥如果不够牢，年轻人花了钱和时间，得到的结果可能反而限制了自己的可能性。

但说到底，这道题最深层的问题是——我们的教育评价体系和社会资源分配，还没有充分向每一个个体倾斜。如果一个社会能给每个人提供多元化的成长路径和充分的职业探索空间，大家就不必依赖一个网络测试来决定自己的人生方向。

答题完毕。"""

# 3-态度观点
answers["3-态度观点     -"] = """各位考官，"奋斗是青春最亮丽的底色"这句话，我想结合现实来理解它。

第一，这句话放在今天说，有很强的现实针对性。当下有一种声音叫"躺平"——不是真的不想努力，而是很多年轻人觉得努力了也没用。房价高、就业难、内卷严重，奋斗的"性价比"好像越来越低。在这个背景下，强调"奋斗是青春的底色"，不是在喊口号，而是在回应一种社会情绪。

第二，但"奋斗"这个词需要被具体化。不是996加班就叫奋斗，不是透支身体就叫奋斗。真正的奋斗是——找到一件你觉得值得做的事，然后持续地投入进去。可能是考一个证书，可能是学一门技术，可能是把一个项目做到极致。奋斗不一定要惊天动地，它更多时候是日复一日的坚持。

第三，从矛盾分析的角度看，青春有一个内在矛盾：它既是精力最旺盛的时期，也是方向最迷茫的时期。你没有经验、没有人脉、没有资本，你唯一有的是时间和体力。奋斗的意义就在于，它把"青春"这个不确定的阶段，转化成了"积累"——你今天做的每一件事，都会在未来某个时刻产生回响。也许不是明天，但一定会有那一天。

所以我对这句话的理解是：奋斗不是"假装努力"的自我感动，也不是"躺平认命"的反面，而是——在你还有时间、还有精力、还有犯错机会的年纪，去真正投入地做一件事。这个底色，别人抹不掉。

答题完毕。"""

# 4-体制内必修课
answers["4-体制内必修课     -"] = """各位考官，领导交给我不熟悉的任务，我想先做三件事。

第一，先确认边界。不熟悉的任务，首先要搞清楚——领导要我交付的到底是什么？是一个方案、一份报告、还是一次协调？什么时候要？有没有可以参考的先例？这些基本信息不搞清楚，盲目行动反而是浪费时间。在机关里，"问清楚"本身就是一种能力。

第二，用对资源。体制内做事不是单打独斗——有业务骨干、有老同志、有上级部门、有兄弟单位。我的策略是：先自己快速消化现有材料，列出不懂的问题清单，然后带着具体问题去请教，而不是笼统地问"这个怎么做"。被请教的人时间也是有限的，你把功课做在前面，别人才愿意帮你。

第三，及时反馈。机关工作最忌讳的是"闷头干到底，最后交上来完全不对"。我会在做了三分之一的时候，拿初步方案给领导看一眼——不是让领导替我做，而是确认方向没错。这叫"过程管理"，是体制内最被低估的能力。

最后我想说一句，不熟悉的任务其实是最好的学习机会。你熟悉的事情做一百遍，能力不会涨。但不熟悉的事情每做一件，能力边界就扩大一寸。

答题完毕。"""

# 5-组织类
answers["5.组织类     -"] = """各位考官，乡村旅游调研和其他调研不一样——它最怕的是"走马观花看一圈，回来写个报告交差"。我的思路是围绕三个关键问题展开。

第一，搞清楚"有没有"——这个村到底有没有旅游资源？不只是看有没有山有水，更要看有没有故事。很多村子自然风光一般，但有一段鲜为人知的历史或者一个独特的民俗。这种"软资源"往往比山水本身更有价值。所以我会专门走访村里的老人，翻翻村志县志，因为真正的旅游IP往往藏在细节里。

第二，评估"行不行"——有资源和"能开发"是两回事。交通方便吗？有停车场吗？村里有闲置房屋可以改造成民宿吗？村民愿意参与吗？这些问题不问清楚，调研报告写得再漂亮，落不了地就是废纸。我会用"游客视角"走一遍——假设我是一个自驾游客，从进城到停车到玩到吃住，每个环节有没有障碍？

第三，算清楚"值不值"——投入和产出大概是什么量级？周边的村子有没有成功的案例可以参考？失败的案例更要看——为什么他们没做起来？是因为产品不行还是市场不行？从别人的失败中学到的，往往比从成功中学到的更值钱。

这三个问题搞清楚之后，我才开始写调研报告。报告的结论只有一个——能做还是不能做。如果能做，重点在哪；如果不能做，为什么。

答题完毕。"""

# 6-矛盾类
answers["6.矛盾类     -"] = """各位考官，小王和小李都是业务骨干，两人不说话说明矛盾已经比较深了。处理这种问题，我的原则是：不站队、不拖延、不激化。具体三步走。

第一步，先稳住工作。矛盾归矛盾，活不能停。我会临时调整分工——把需要两人密切配合的工作先拆开，各做各的，保证科室整体运转不受影响。但这不是长久之计，只是给解决问题争取时间。

第二步，分别谈。我不会一开始就把两人叫到一起——那容易变成各说各话甚至当面争吵。我会先单独找小王谈，再找小李谈。谈话的时候不问"谁对谁错"，而是问"你觉得问题出在哪"和"你觉得怎么解决比较好"。让对方自己说出来——当他需要为自己的建议负责时，情绪会退一步，理性能进一步。

第三步，在合适的时机促成和解。等双方都冷静下来之后，找一个工作任务作为契机——"这个项目需要你们俩一起做，之前的矛盾先放一放，把这个活干完再说。"在共同完成一件事的过程中，隔阂往往能自然消解——因为你们有了一个新的共同目标，而不是纠结于过去的谁对谁错。

最后我想说，科室里有人闹矛盾，说明这些人在乎工作——如果不在乎，就不会争。作为负责人，我的责任不是消灭矛盾（也消灭不了），而是让矛盾成为推动工作前进的摩擦力，而不是阻碍工作前进的死结。

答题完毕。"""

# 7-模拟题
answers["7.模拟题     -"] = """大爷，您先坐，喝口水，别气坏了身子。

您说的情况我记着呢——上个月您来过两次，我都登记了。我知道每天晚上睡不好觉有多难受，换了我我也急。

但是大爷，您刚才说"自己解决"，这可千万使不得。我为什么这么紧张？因为我之前碰到过一个类似的——也是楼上楼下因为噪音闹矛盾，楼下那位一冲动上门跟人吵了一架，结果两家从邻居变成了仇人，最后闹到派出所。本来是个小事情，这么一搞就大了。我不希望您也走这个弯路。

楼上那户的情况我核实过了——是个做直播带货的小伙子，每天晚上开工。我前两天去找过他，他态度确实不太好，说"我在自己家工作碍着谁了"。但我跟他说了一句话——"你可以不把大爷当回事，但我代表社区，这事我们有责任管。"他听完态度就软了。

这样大爷，我今天再去找他一次——这次不是跟他商量，是跟他说明利害。第一，晚上十点以后产生噪音属于扰民，有规定的。第二，他做直播的，社区要是给他开个扰民的证明，对他的生意也是影响。这两条摆出来，他不可能不配合。

但我也跟您交个底——彻底没声音是不可能的，毕竟人家靠这个吃饭。可能的结果是——晚上十点以后他注意控音量，十点以前您多担待。大家各退一步。

大爷您放心，这事我肯定管到底。您就在家等我消息，三天之内我给您一个结果。您现在先回去休息，别的事交给我。"""

# Step 2: Replace
for fname_key, new_body in answers.items():
    # Find matching file
    matched = None
    for existing in os.listdir(out):
        if existing.endswith('.md') and fname_key[:10] in existing[:10]:
            matched = existing
            break

    if not matched:
        print(f"  MISSING: {fname_key}")
        continue

    path = os.path.join(out, matched)
    lines = open(path, encoding='utf-8').read().split('\n')

    # Find the exact line with "答题示范"
    ans_line = None
    for i, line in enumerate(lines):
        if line.startswith('###') and '答题示范' in line:
            ans_line = i
            break

    if ans_line is None:
        print(f"  NO ANS SECTION: {matched}")
        continue

    # Find next ### section
    next_section = len(lines)
    for i in range(ans_line + 1, len(lines)):
        if lines[i].startswith('###'):
            next_section = i
            break

    # Replace body content (keep heading, replace body, keep rest)
    new_lines = lines[:ans_line+1]
    new_lines.append('')
    new_lines.append(new_body)
    new_lines.append('')
    new_lines.extend(lines[next_section:])

    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))

    print(f"  DONE: {matched[:35]}")

# Step 3: Verify
print("\nFinal check:")
for fname in sorted(os.listdir(out)):
    if not fname.endswith('.md'): continue
    c = open(os.path.join(out, fname), encoding='utf-8').read()
    sections = len(re.findall(r'^### ', c, re.MULTILINE))
    size = len(c)
    print(f"  {fname[:40]}: {sections} sections, {size}B")
