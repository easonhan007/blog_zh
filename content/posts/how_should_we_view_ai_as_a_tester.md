---
title: "作为测试人员，我们该如何看待AI"
date: 2023-06-29T11:30:55+08:00
draft: false
---

前几天看到一篇文章讨论从测试人员的角度去理解AI的，稍微翻译了一下。原文地址https://stevethedoc.wordpress.com/2023/06/18/how-should-we-view-ai-as-testers

上周三和周四，我有幸与我的两位同事Sushmitha Sivan和Bhavana Akula一起参加了伦敦的AI峰会。在那里，我们不仅听到了一些非常有趣的关于人工智能的演讲，还有机会为黑客马拉松的参与者们进行了大约一个小时的测试和质量工程的培训，教他们如何将这些知识应用到他们所面临的挑战中。

人工智能对我来说还是比较新的（我猜很多人也是如此），所以我们都处于学习的不同阶段，但这个学习过程非常有趣，因为它的范围和对社会的影响都是令人着迷的。

我不会告诉你如何测试人工智能，或者如何优化数据模型等等，这方面有其他地方可以去了解。这篇文章主要是关于我从参加的不同讲座中得到的一些更普遍的学习和想法，我脑海中浮现出了一些流行词和短语（以下是随机排列的）：

* 道德
* 法规
* 抵抗
* 未知的恐惧
* 失业
* 激发人类创造力
* 减轻繁琐工作
* 数据模型偏见
* 训练数据模型
* 负责任地使用人工智能
* 深度伪造

这让我思考起作为测试专业人员，我们应该如何应对人工智能。我故意使用这个词汇，因为它涵盖了测试中的每个角色。

我们大多数人在职业生涯中都测试过用户界面、后端数据库、API等等，这些都可以生成特定的已知结果。我们有用户故事告诉我们预期的行为，以便我们可以相应地进行测试。那么对于这个新世界，我们该怎么看待呢？

我认为人工智能的目的是增强我们人类的工具，帮助我们做出决策。计算机的思维速度比我们快得多，因此它们可以帮助我们摆脱一些乏味的工作，我们可以利用我们的大脑去做更有创造力的事情。

当然，依赖人工智能可能会导致忽视固有的偏见，我们所做的决策可能基于有缺陷的数据。因此，我们需要谨慎对待我们对结果所放置的信任程度

* 我们能相信AI工具使用的数据集吗？
* 可能包含假数据吗？
* 它是否包含偏见或者是偏差？
* 我们是否相信输出涵盖了我们需要考虑的一切？
* 结果是否受到了可能会影响的缺失参考文献的影响？

如果机器能够替我们进行批判性思考，并且我们毫无疑问地依赖它们，我们也可能失去自己的批判性思维能力。这种情况已经发生了，一个现实世界的例子是这样的——有多少30岁以下的人能够从书上读地图？如果他们的手机或汽车导航系统出故障了，有多少年轻一代能够应对并使用地图作为备用计划？他们在科技依赖下长大，而我们这些年纪稍大一点的人则能够两者兼顾。

作为测试人员，我们很容易陷入打开像ChatGPT这样的东西，并要求它根据我们提供的信息帮助生成测试计划或测试用例的陷阱中，然后将其用作完美答案。我们必须谨慎行事。是的，我们可能会得到一些可以开始的东西，而不是一张空白纸，但如果一直这样做，我们就会失去从头开始自己启动这个过程的能力。有时候，将事物进行思维导图有助于我们自己建立联系-我们必须训练自己从AI给我们的任何想法中开始中途进行，这可能行得通也可能不行。我并不是说这一定是件坏事，但我们需要小心，不要失去自己思考的能力。

有一些很棒的现实场景可以利用人工智能：

- 寻找最佳的抵押贷款利率并将其整理在一张表格中
- 为一个不熟悉的情况起草一封信件
- 准备主持一场测验的研究工作
- 准备一档广播节目（我可能会这样做）

随着我们在日常生活中开始使用人工智能，我们会越来越依赖它，它不会消失，而是需要受到监管（人类有一种令人羡慕的能力，可以将任何发明变成可以用于有害目的的东西！！），并且需要人们对其使用进行质疑。

作为测试人员，我的建议是以适度的怀疑态度接受人工智能。质疑所得到的结果，并进行独立验证。你无法获得结果所基于的数据，因此要谨慎行事，做好测试人员最擅长的事情——深入探究、调查和提问。

最后，保持你的批判性思维能力——在一个人们越来越依赖所听到的话作为真相的世界中，这一点将比以往任何时候都更加重要。那些能够退后一步，采取客观的方法的人将在未来脱颖而出。

欢迎来到崭新的世界。


### 谨慎的在测试过程中使用人工智能

作者的观点我是大部分赞同的，最近一直在关注AI领域，生成式AI爆发性的增长以及快速的落地应用让很多人都印象深刻。我甚至听到过一种观点：凡是现在可以被外包的工作将来都可能被ai所取代。

但事实果真如此吗？

首先我必须说明，我是非常看好AI在测试领域的应用的，从三体里借用一个词语，那我可能是降临派，历史的车轮滚滚向前，螳臂当车可能是不太明智的。尽管我看好未来，不过从现在这个阶段来说，把AI应用到测试工作中我们还有很多问题需要解决。

* 首先值得借鉴的应用场景目前并不多。这篇推文写作的时间是2023年的年中，从目前的情况看将AI应用到测试中的案例并不多见.有一个非常有启发的例子是用AI自动进行网页上操作，不过离真正的测试活动还是有些差距的，预期结果和断言的缺失让这个想法目前还只是属于自动化的范畴。

* 数据安全性。这是老生常谈的问题，目前很多的ai应用都会将数据发送到openAI的后台，这就意味着很有可能你的组织内的隐私数据或者个人的敏感信息会被openAI存在数据库中。只要是落库了，那么你就没办法避免openAI被攻击导致数据泄露，或者被openAI的员工惊鸿一瞥，这些顾虑也会导致大型的组织和公司会非常谨慎的使用AI应用。另外如果OpenAI使用你的敏感数据进行模型的训练，那么你的一些私人信息将会成为模型的内建知识，供所有人参观和品评，这可能不是是一个令人愉快的体验。

* 准确性。AI会出现幻觉，也就是一本正经的胡说八道，对于一些应用来说这是没问题的，比如算命和星座预测。但对于测试来说这是不可接受的，测试要求客观性，定义的结果和实际的结果一定要尽可能的一致，然而目前这个阶段，AI在这方面的表现还是有很大的提升空间的。

* 结果的一致性。我写过一些AI应用，在很多情况下我发现AI给出的结果是不一致的，相当的输入可能无法得到完全一致的输出。比如我希望ai处理完数据之后以json格式输出结果，有时候ai就是很任性的给出其他格式的输出，对一些需要规模化的应用来说，这是不可接受的，需要在工程层面做很多事情来进行纠偏。对于倾向于开发短平快的测试应用来说，这点也会拖慢我们的开发周期以及降低运行的稳定性。

* 更好的模型还在路上。随着玩家的增加，更好的模型可能在路上。也许这周你需要花费很多精力去做的事情下个月就已经成为模型的内建能力了，比如现在chatgpt的plugin就是很好的例子。如果我们对模型的内在能力有更高要求的话，稍微等一等可能算是个比较现实优选方案。另外测试行为对多模态的依赖也相对较深，这方面目前的模型能力还不是特别成熟。

最后, 欢迎来到崭新的世界。测试领域也需要探索未知，如果上面的问题对你来说不是阻碍，那么现在这个时间点就是是投入研究的最佳时期。


