---
title: "Grok3和deepseek在测试领域如何落地"
date: 2025-02-21T09:19:52+08:00
draft: false
---

## Grok3

前几天马斯克发布了 Grok3。

简单试用了一下，有几点感想。

- 速度是真快。除了搜索之外，基本上大部分的问题都是秒回；
- 对中文的理解不错；
- 代码生成能力令人印象深刻；

因为只是简单的体验了一下，感触比较浅薄。

## 与测试的结合

昨天看到 DHH 在社交媒体上谈论 Grok3。

他表示 Grok3 对他来说最重要的功能是处理测试代码。

这里可以简单的理解为使用 Grok3 进行单元测试和集成测试用例的编写。

这也是我认为目前来说 AI 在测试领域可以迅速落地的点。

特别是使用 AI 进行单元测试用例，理由如下。

- 单元测试用例相对来说依赖比较少，做的事情也相对单纯，适合 AI 进行代码生成；
- 单元测试框架相对来说更新不是非常频繁，哪怕 AI 的数据不是最新，生成的代码可用性也很高；
- 我们可以先写实现代码再让 AI 对我们的实现代码进行测试，这样上下文比较精确，生成的代码基本上是可用信赖的；
- 写单元测试比较痛苦的地方是给用例取名，但对 AI 来说，这其实是小菜一碟；我发现 AI 生成的用例名称比我自己写的要有意义的多；

另外我之前也使用过 github 的 copilot 来进行单元测试用例的编写，总体来说速度和准确性都可以接受。

## Grok3 生成的单元测试

这里贴一个 Grok3 生成的测试`print("hello")`的测试用例。

平心而论，这个用例逻辑很简单，但是实现起来却不是很容易。

Grok3 非常迅速且准确的完成了这个任务。

我只能说，用例写的真好，比我自己实现的要好很多。

我来为 `print("hello")` 这段 Python 代码写几个单元测试用例。由于 print() 是内置函数，主要作用是输出到控制台，测试它的行为需要考虑如何捕获输出。我们可以使用 Python 的 unittest 框架，并结合 io.StringIO 和 sys.stdout 重定向来验证输出结果。

以下是几个单元测试用例，假设这段代码被封装在一个函数中：

### 前提代码

假设我们将 print("hello") 放入一个简单的函数：

```python
def print_hello():
    print("hello")
```

### 单元测试代码

以下是基于 unittest 的测试用例：

```python
import unittest
import sys
from io import StringIO

# 被测试的函数
def print_hello():
    print("hello")

class TestPrintHello(unittest.TestCase):

    def setUp(self):
        # 在每个测试用例前重定向 stdout
        self.held_output = StringIO()
        sys.stdout = self.held_output

    def tearDown(self):
        # 在每个测试用例后恢复 stdout
        self.held_output.close()
        sys.stdout = sys.__stdout__

    # 测试用例 1：验证输出内容是否为 "hello"
    def test_print_hello_output(self):
        print_hello()
        output = self.held_output.getvalue().strip()
        self.assertEqual(output, "hello")

    # 测试用例 2：验证输出不为空
    def test_print_hello_not_empty(self):
        print_hello()
        output = self.held_output.getvalue().strip()
        self.assertTrue(len(output) > 0)

    # 测试用例 3：验证输出不包含意外内容
    def test_print_hello_no_unexpected_content(self):
        print_hello()
        output = self.held_output.getvalue().strip()
        self.assertNotEqual(output, "hi")  # 不应输出 "hi"
        self.assertNotIn("error", output)  # 不应包含 "error"

if __name__ == "__main__":
    unittest.main()
```

### 测试用例说明

`test_print_hello_output  `

- 目标：验证 print_hello() 输出是否精确为 "hello"。
- 方法：捕获输出并与预期值比较。

`test_print_hello_not_empty `

- 目标：确保函数有输出，而不是空字符串。
- 方法：检查输出长度大于 0。

`test_print_hello_no_unexpected_content `

- 目标：确认输出不包含意外内容（如 "hi" 或 "error"）。
- 方法：使用 assertNotEqual 和 assertNotIn 检查。

### 运行结果

运行这段测试代码时：
所有测试应该通过，因为 print("hello") 会稳定输出 "hello"。
如果你修改 print_hello() 为 print("hi")，则 test_print_hello_output 会失败。

### 注意事项

sys.stdout 重定向：因为 print() 直接输出到标准输出，我们需要用 StringIO 捕获它。
测试局限：如果 print_hello() 被改为写入文件或不调用 print()，这些测试需要调整。
扩展性：你可以添加更多用例，比如测试换行符 \n（默认 print() 带换行）：

```python
def test_print_hello_with_newline(self):
    print_hello()
    output = self.held_output.getvalue()
    self.assertTrue(output.endswith("\n"))
```

如果你想测试其他场景（比如异常处理、参数化输出），告诉我，我可以进一步扩展！

## 目前的实践

目前工程化方面，除了 github 的 copilot 和 cursor 等工具之外，很多时候我们都是在做复制和粘贴的工作。

先把实现代码粘贴进 AI 对话框，然后把单元测试用例拷贝出来。

效率不高，而且过程很枯燥，时间长了会让人陷入自我怀疑。

难道我只是复制粘贴的工具么？

所以后面 AI 生成单元测试的实践可能会是：

- 更深层次 IDE 级别的集成，比如一键生成单元测试用例并且运行的能力；
- 框架级别的 AI 集成。在开发框架里集成 AI 生成测试用例的能力，并进行执行；

## Deepseek 与单元测试

同样的题目，让 deepseek 去实现`print("hello")`的测试用例。

以下是针对 `print("hello")` 的单元测试用例，使用 Python 的 `unittest` 框架并捕获标准输出验证结果：

```python
import unittest
from io import StringIO
import sys
from unittest.mock import patch

# 要测试的代码
def hello_world():
    print("hello")

# 单元测试类
class TestHelloWorld(unittest.TestCase):
    def test_hello_output(self):
        # 捕获标准输出
        captured_output = StringIO()
        sys.stdout = captured_output

        # 执行函数
        hello_world()

        # 恢复标准输出
        sys.stdout = sys.__stdout__

        # 验证输出结果（注意 print 会自动换行，输出实际为 "hello\n"）
        self.assertEqual(captured_output.getvalue().strip(), "hello")

    # 另一种方法：使用 unittest.mock.patch 直接捕获输出
    @patch('sys.stdout', new_callable=StringIO)
    def test_hello_output_with_patch(self, mock_stdout):
        hello_world()
        self.assertEqual(mock_stdout.getvalue().strip(), "hello")

if __name__ == "__main__":
    unittest.main()
```

### 说明：

1. **捕获输出逻辑**：

   - 第一种方法手动将 `sys.stdout` 重定向到 `StringIO` 对象，执行后恢复原输出。
   - 第二种方法使用 `@patch` 装饰器自动模拟 `sys.stdout`，更简洁且避免资源泄漏。

2. **注意换行符**：
   - `print("hello")` 实际输出 `"hello\n"`，因此断言时使用 `.strip()` 去掉首尾空白（包括换行符）。

### 运行测试：

将代码保存为 `test_hello.py`，执行以下命令：

```bash
python -m unittest test_hello.py
```

### 预期结果：

测试通过，输出类似：

```
..
----------------------------------------------------------------------
Ran 2 tests in 0.001s

OK
```

其实 deepseek R1 也能一次写对，但是用例的完备程度是不如 grok3 的，另外输出速度上 grok3 的优势还是比较明显的。

不过我觉得用 deepseek R1 写单元测试用例应该也没什么问题，用例完备性默认不高的问题可以在 prompt 里面增加引导，有可能会得到不错的效果。

## 总结

总之目前看来 AI 在代码能力上的表现是可圈可点的。

而代码跟测试结合的最紧密的点就是单元测试。

而开发不写单元测试的原因无非是不会写和没时间写。

现在 ai 代码助手的出现让这两个理由已经站不住脚了。

有理由相信在不远的将来，ai 生成的单元测试用例将是大部分软件项目的标配。
