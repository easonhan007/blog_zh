---
title: "索引构造与信息检索 让ChatGPT成为Selenium问答助手"
date: 2023-04-21T11:16:06+08:00
draft: false
---

这是chatgpt为我生成的3个标题，我选了第3个。

1. 利用 Langchain 和 GPT 实现 Selenium 机器人自动问答
2. 向量化存储和检索：如何用相似度搜索匹配 Selenium 知识？
3. 索引构造与信息检索：让 ChatGPT 成为 Selenium 问答助手

之前有很多同学会问我一些有关selenium的问题，因为精力有限，不能一一回答。最近正好chatgpt为代表的生成式ai非常火爆，那么我们能不能训练一个有selenium知识的
机器人帮我回答问题呢？人的时间有限，但是机器人可以一直在线工作，妥妥的劳模了。

经过一番调研，我发现langchain这个库也许可以祝我一臂之力。

### 整体思路

整理思路很简单，就是gpt是预先训练好的模型，有自己的先见知识，这也是为什么我们问它问题它会给出答案的原因，因为它的模型里就固化了这些知识。然而gpt3模型用的数据应该是截止到2021年的，也就是2年多之前的数据了。尽管selenium总体得带速度不快，但这两年也多多少少发生了一些变化，直接用gpt模型的先见知识可能会造成一些回答不准确的情况。

所以我们可以用gpt的两大能力，而不是先见知识。

* 推断的能力。给出一些上下文，让gpt总结和推断问题的答案
* 生成内容的能力

所以现在问题就变成了如何给gpt”灌“入最近的selenium知识？

其实我们可以在gpt的prompt里面加上一些实时的准确的上下文，然后让gpt去根据上下文内容实时的生成问题的答案，比如下面这个prompt

```
你是selenium问答机器人，你的任务是根据我提供的selenium相关信息来回答用户提出的问题。忘掉你之前的学到的知识，只用我提供的信息去回答。如果问题超出了我提供的信息范围，你就回答不知道。

==============
selenium的一些最新的介绍
...
...
...
==============
问题：selenium是什么？

```

这样一来任务就变成了**如何根据用户的问题搜索相关的selenium知识？** 这里就要用到向量化存储和检索了。

### 向量化存储和检索

先看看chatgpt的解释吧。

```
Q: 我是一个5岁的小孩，请给我解释一下什么是向量化存储和检索，要让我能看懂

A: 嘿，你好呀！向量化存储和检索是指将文本、图像或其他数据转换成一组数字，并使用这些数字来存储和查找信息。可以把这些数字看成是一个有很多数字的表格，每一个数字代表着这个信息的一个特征。比如说，对于一张图片，可以用数字来表示它的长宽、色彩等等特征。当我们需要查找信息时，可以用相似度来比较数字之间的差距，来找到和我们要查找的信息最相似的那一组数字，从而找到相关的信息。这个技术可以用在很多场合，比如说搜索引擎、推荐系统、图像识别和自然语言处理等等。
```

其实我们可以简单理解为相似度搜索。

我们要处理的问题是：用户输入问题，然后根据相似度，找到最匹配的一些相关材料，然后返回这些内容。这种工作向量化索引和检索是可以帮我们很好的完成的。

### 实现流程

这样我们可以把流程梳理清楚了，这里有两个流程，分别是爬一些selenium的数据，向量化之后存到向量化数据库里，可以理解成为是构造索引的过程；以及搜索用户提出的问题，给出相关答案，然后要求gpt生成内容，可以理解为信息检索和生成的过程。

**索引构造过程**

我随便在selenium的主页拿了3个页面的内容，分别是

* https://www.selenium.dev/documentation/overview/
* https://www.selenium.dev/documentation/overview/components/
* https://www.selenium.dev/documentation/overview/details/

使用下面的js脚本可以直接拿到页面内容

```javascript
document.querySelector('.td-content').textContent
```
我把内容保存在了se.txt文件里。下面是流程的简单分析

```
从se.txt中读取内容 -> 切分内容里的文本 -> 调用openai的向量化接口进行向量化 -> 将向量化过的内容保存在向量数据库中
```

**检索及内容生成的过程**

```
调用openapi接口向量化用户问题 -> 在向量数据库中搜索相关答案 -> 将问题和答案合成为prompt发送给gpt3.5 -> 展示gpt返回的内容
```

### 代码实现

```python
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI

from langchain.document_loaders import TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
import sys

def create_index():
	loader = TextLoader('./se.txt', encoding='utf8')
	documents = loader.load()
	text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
	docs = text_splitter.split_documents(documents)

	embeddings = OpenAIEmbeddings()
	# db = Chroma.from_documents(docs, embeddings)
	vectordb = Chroma.from_documents(documents=docs, embedding=embeddings, persist_directory='.')
	vectordb.persist()
	vectordb = None

def query(question: str):
	# Load from existing index
	# Now we can load the persisted database from disk, and use it as normal. 
	embeddings = OpenAIEmbeddings()
	vectordb = Chroma(persist_directory='.', embedding_function=embeddings)
	# docs = vectordb.similarity_search(question)
	# print(docs[0].page_content)
	retriever = vectordb.as_retriever(search_kwargs={"k": 1})
	qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=retriever)
	res = qa.run(question)
	print("=" * 20)
	print(res)

if __name__ == "__main__":
	cmd = "q"
	if len(sys.argv) > 1:
		cmd = sys.argv[-1]

if cmd in ['c', 'create']:
	create_index()
elif cmd in ['q', 'query']:
	query("how selenium control the browsers")
else:
	print(f"unsupport cmd {cmd}")
```

下面是chatgpt对上面这段代码的解释

这是一段 Python 代码，其目的是建立一个问答系统，可以对输入的自然语言问题进行回答。具体地，代码中使用了以下库和模块：

- `langchain.chains`：其中包含了一个叫做 `RetrievalQA` 的类，该类封装了一个检索模型和一个答案提取模型，用于回答问题。
- `langchain.llms`：其中包含了一个叫做 `OpenAI` 的类，用于连接 OpenAI API 并执行自然语言任务。
- `langchain.document_loaders`：其中包含了一个叫做 `TextLoader` 的类，用于从本地文件系统中加载文档。
- `langchain.embeddings`：其中包含了一个叫做 `OpenAIEmbeddings` 的类，用于计算文本的向量表示。
- `langchain.text_splitter`：其中包含了一个叫做 `CharacterTextSplitter` 的类，用于将长文本切分为小段落。
- `langchain.vectorstores`：其中包含了一个叫做 `Chroma` 的类，用于构建向量数据库，并提供了向量检索的功能。

代码中的 `create_index` 函数用于创建向量数据库，具体地，它首先使用 `TextLoader` 加载一个名为 `se.txt` 的文本文件，并使用 `CharacterTextSplitter` 将该文本文件分成多个小段落。然后，它使用 `OpenAIEmbeddings` 计算每个小段落的向量表示，并使用 `Chroma` 构建向量数据库，并将其持久化到本地文件系统中。

代码中的 `query` 函数用于回答问题，具体地，它首先加载之前创建的向量数据库，并使用 `Chroma` 将输入的自然语言问题转化为向量表示，并在向量数据库中进行检索，找到最相关的文本段落。然后，它使用 `RetrievalQA` 类的实例对文本段落进行答案提取，并将结果打印输出到控制台。

在 `__main__` 函数中，代码首先解析命令行参数，如果没有参数或者参数为 `q` 或 `query`，则调用 `query` 函数回答问题；如果参数为 `c` 或 `create`，则调用 `create_index` 函数创建向量数据库；否则，打印错误信息。


只能说解释的比我好。另外RetrievalQA这个类实际上是一问一答，并没有多轮对话的能力。

### 效果



```
Q: How selenium control the browsers

Using embedded DuckDB with persistence: data will be stored in: .
====================
 Selenium controls web browsers by remotely controlling browser instances and emulating a user's interaction with the browser. It allows users to simulate common activities such as entering text into fields, selecting drop-down values, checking boxes, and clicking links in documents. Additionally, it provides many other controls such as mouse movement, arbitrary JavaScript execution, and more.
```
如果不自己灌数据的话，这个问题的答案是这样的

```
Selenium is an open-source testing tool that can control the browsers and automate web-based applications. Selenium uses the WebDriver protocol to control different browsers such as Chrome, Firefox, Safari, Internet Explorer, Edge, and Opera.

When a test script interacts with Selenium's API commands such as findElement(), click(), sendKeys(), etc., it creates a request using the WebDriver protocol. The request is then sent to a browser-specific driver (such as chromedriver.exe for Google Chrome), which interprets the command and sends instructions to the browser through its own API.

The browser executes those instructions and returns results back to the driver. The driver then processes these results and sends them back to Selenium along with any relevant information about errors or exceptions encountered during execution.

In summary, Selenium controls browsers by communicating directly with their respective drivers using protocols specific to those drivers in order to manipulate webpage elements programmatically.

```
看上去更好一点，但使用的是先见知识，不一定能保证正确性和实时性。不过对于这个问题，chatgpt生成的回答已经是非常完美了。

### 总结

让chatgpt给我写个总结。

这篇文章提出了使用生成式AI ChatGPT和LangChain库训练一个Selenium知识问答机器人的想法。机器人需要灌入最新的Selenium知识并使用向量化存储和检索来搜索相关材料以回答用户的问题。文章介绍了实现流程，包括爬取Selenium数据、向量化存储和检索、信息检索和生成内容。

这项技术非常适合构建专有领域的知识库，比如法律咨询，医疗咨询等。另外配合一些代码切片的库还可以实现代码生成功能。

总之AI技术可以让我们用非常低的成本实现一些之前很难去搞定的工作，确实挺有意思的。

