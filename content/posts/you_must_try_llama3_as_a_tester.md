---
title: "破防了，我用本地运行的ai写代码，感觉它比我厉害多了"
date: 2024-04-25T22:14:17+08:00
draft: false
---

事情是这样的，前几天 facebook 发布了最新的[llama3 模型](https://ai.meta.com/blog/meta-llama-3/)，我第一时间就用[ollama](https://ollama.com/library/llama3)下载运行了一下，8b 模型的 size 很小，只有 4.6G 的样子，在我 16g 显存的台式机上，速度相当快，快到有点恍惚，现在的本地模型这么强了吗？

本着判断本地模型唯一的标准就是让它做中英文翻译的原则，我让 llama3 翻译了几个英文句子，不意外，基本言不达意，完全不可用，然后就简单了，给它贴上不可用的标签，就在我的模型库里待着好了。

然而几天后事情来了个 180 度大反转，我发现大家的测试结果都非常的正向，直呼这应该是目前为止最强的本地运行大模型了，有人测试了 70b 的版本，甚至把这个版本跟 gpt4 相提并论。

这不科学呀，明明这玩意连英译中都搞不好，怎么可能评价这么高呢？

本着试试不要钱的态度，我随便问了它几个跟自动化相关的问题，结果确实让人惊讶。

首先 llama3 应该 95%的训练材料都是英文的( over 5% of the Llama 3 pretraining dataset consists of high-quality non-English data that covers over 30 languages)，所以中文不好无可厚非，跟其交互的时候最好用英文提问。于是我用蹩脚的英文问了它第一个问题。

### 第一个问题

Open a browser using selenium and go to www.itest.info, then write a pytest assert to verify the page title should equal to 重定向科技, please give me the entile python code

翻译过来就是`打开浏览器，访问itest.info,然后用pytest写个断言，内容是浏览器的title应该等于重定向科技，直接给我python代码`

下面是 llama3 秒回的结果，真的是秒回，基本上刚敲完回车就开始炫了 😂。

Here is the Python code that uses Selenium WebDriver with Pytest to open a browser, navigate to `www.itest.info`, and assert that the page title equals "重定向科技":

```python
import pytest
from selenium import webdriver

@pytest.fixture
def browser():
    driver = webdriver.Chrome()  # Replace with your preferred browser
    yield driver
    driver.quit()

def test_itest_info(browser):
    browser.get("https://www.itest.info")
    assert browser.title == "重定向科技"
```

Let me explain what each line does:

1. `import pytest`: We're using Pytest for our testing framework.
2. `from selenium import webdriver`: We're importing the Selenium WebDriver library.
3. `@pytest.fixture`: This is a Pytest fixture, which sets up and tears down resources (in this case, a browser instance) for each test.
4. `def browser():`: The fixture function returns a browser object, which we'll use to interact with the website.
5. `driver = webdriver.Chrome()`: We're creating a new Chrome browser instance (replace with your preferred browser if needed).
6. `yield driver`: This is where the browser instance is yielded back to the test function.
7. `browser.quit()`: After the test is finished, we'll close the browser instance using the `quit()` method.
8. `def test_itest_info(browser):`: Our actual test function takes a browser instance as an argument.
9. `browser.get("https://www.itest.info")`: We're navigating to the website using the `get()` method.
10. `assert browser.title == "重定向科技"`: We're asserting that the page title is equal to "重定向科技". If this assertion fails, Pytest will raise an exception.

To run this code, save it in a file (e.g., `itest_test.py`) and then run it using Pytest:

```
$ pytest itest_test.py
```

This should execute the test and report any failures or errors.

怎么说呢，不仅写的比我快，而且写的还比我好，不仅写的比我好，还解释了一大堆，都说言多必失，不过它的解释似乎没啥问题。

### 第二个问题

then click a button with id = 12345

接下来点击一个 id 为 12345 的 button

依然秒回，现在的大模型，性子都那么急。

Here is the updated code that clicks a button with an ID of `12345` after navigating to the website:

```python
import pytest
from selenium import webdriver

@pytest.fixture
def browser():
    driver = webdriver.Chrome()  # Replace with your preferred browser
    yield driver
    driver.quit()

def test_itest_info(browser):
    browser.get("https://www.itest.info")

    # Find and click the button with ID 12345
    button = browser.find_element_by_id("12345")
    button.click()

    assert browser.title == "重定向科技"
```

Here's what's new:

1. We use `browser.find_element_by_id()` to locate an element (in this case, a button) with the specified ID (`12345`).
2. We store the found element in the `button` variable.
3. We call the `click()` method on the button to simulate clicking it.

Note that if there are multiple elements on the page with the same ID, Selenium will throw an exception when trying to find the element. To avoid this, you can use more specific locator strategies (e.g., CSS selectors or XPath expressions) or ensure that the ID is unique on the page.

终于出问题了，`find_element_by_id`是老的接口，这样写几年前没问题，但现在就不行了，目前比较通用的写法是使用`By.ID`这种形式。

### 第三个问题

The code above is not correct, please use By.ID to refactor it.

上面的代码不对，请使用 By.ID 来进行重构。

嗯，还是秒回，这回习惯了。

I apologize for the mistake! Here is the corrected code:

```python
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

@pytest.fixture
def browser():
    driver = webdriver.Chrome()  # Replace with your preferred browser
    yield driver
    driver.quit()

def test_itest_info(browser):
    browser.get("https://www.itest.info")

     # Find and click the button with ID 12345 using By.ID
    button = browser.find_element(by=By.ID, value="12345")
    button.click()

    assert browser.title == "重定向科技"
```

I've refactored the code to use the `By` class from Selenium's `webdriver.common.by` module, which provides a more explicit way of specifying the locator strategy. In this case, we're using `By.ID` to locate the element by its ID.

Note that I also replaced `find_element_by_id()` with `find_element(by=By.ID, value="12345")`, which is the recommended way to use the new locator strategy.

llama3 不仅道歉了，还改正了结果。如果这是 chatgpt3.5 或者 claude3，这就是基本操作，没啥大不了的，但对于一个本地运行的模型来说，这种表现实在是非常可以了。

### 有初步结论了

看来 llama3 在解决编程问题上是属于**可用**的状态。

- 对于一般的开发人员来说，我们可以从面相 google 的编程慢慢转变为部分面相本地 llm 的编程模式了。
- 对于企业来说，本地的 llm 不存在把代码传到远程的问题，信息安全性的问题可以部分解决了。
- 对于测试人员来说，会一些基本的编程技巧就可以实现使用自然语言进行测试用例编写的能力了。这是之前很多年大家追求的目标，现在一个本地 4.6g 的模型基本可以让我们摸到一点点边了；
- 对于质量管理来说，用本地 llm 跟开发人员进行结对编程似乎也有了可能性，开发人员写代码，llm 生成单元测试代码，也许只要通过微调就可以部分实现；

### 试一试稍微难一点的问题

using go access this api https://api.dictionaryapi.dev/api/v2/entries/en/<word>, then print the all the meannings from the response, the respinse is a json string, it is like `[
    {
      "word": "hello",
      "phonetic": "həˈləʊ",
      "phonetics": [
        {
          "text": "həˈləʊ",
          "audio": "//ssl.gstatic.com/dictionary/static/sounds/20200429/hello--_gb_1.mp3"
        },
        {
          "text": "hɛˈləʊ"
        }
      ],
      "origin": "early 19th century: variant of earlier hollo ; related to holla.",
      "meanings": [
        {
          "partOfSpeech": "exclamation",
          "definitions": [
            {
              "definition": "used as a greeting or to begin a phone conversation.",
              "example": "hello there, Katie!",
              "synonyms": [],
              "antonyms": []
            }
          ]
        },
        {
          "partOfSpeech": "noun",
          "definitions": [
            {
              "definition": "an utterance of ‘hello’; a greeting.",
              "example": "she was getting polite nods and hellos from people",
              "synonyms": [],
              "antonyms": []
            }
          ]
        },
        {
          "partOfSpeech": "verb",
          "definitions": [
            {
              "definition": "say or shout ‘hello’.",
              "example": "I pressed the phone button and helloed",
              "synonyms": [],
              "antonyms": []
            }
          ]
        }
      ]
    }
  ]`

用 golang 去访问 1 个 api，然后打印返回值里的 meanings 字段，这里 meannings 字段比较复杂，处理起来有点点麻烦。

这时候 llama3 的回答就有意思了。

Here is a sample Go program that sends an HTTP request to the API, parses the JSON response, and prints out all the meanings:

```go
package main

import (
    "bytes"
    "encoding/json"
    "fmt"
    "io/ioutil"
    "net/http"
)

func main() {
    // Set the word you want to look up
    word := "hello"

    // Make an HTTP request to the API
    url := fmt.Sprintf("https://api.dictionaryapi.dev/api/v2/entries/en/%s", word)
    resp, err := http.Get(url)
    if err != nil {
        panic(err)
    }
    defer resp.Body.Close()

    // Read the response body
    body, err := ioutil.ReadAll(resp.Body)
    if err != nil {
        panic(err)
    }

    // Unmarshal the JSON response
    var data []map[string]interface{}
    err = json.Unmarshal(body, &data)
    if err != nil {
        panic(err)
    }

    // Print out all the meanings
    for _, entry := range data {
        for _, meaning := range entry["meanings"].([]interface{}) {
            fmt.Println("Part of speech:", (meaning.(map[string]interface{}))["partOfSpeech"])
            for _, definition := range (meaning.(map[string]interface{}))["definitions"].([]interface{}) {
                fmt.Println("Definition:", definition.(map[string]interface{})["definition"])
                if example, ok := definition.(map[string]interface{})["example"]; ok {
                    fmt.Println("Example:", example)
                }
                if synonyms, ok := definition.(map[string]interface{})["synonyms"]; ok && len(synonyms.([]interface{})) > 0 {
                    fmt.Println("Synonyms:", synonyms)
                }
            }
        }
    }
}
```

This program sends an HTTP GET request to the API with the specified word, reads the response body, and then unmarshals it into a slice of maps. It then iterates over this slice and prints out all the meanings.

Please note that you should handle the error cases more robustly in production code. This is just a sample program.

我没运行代码，不过看上去可能是跑得起来的。不过很显然这种实现方式不是很妙呀。

继续让它用 struct 来重构。

refactor the above code, use a struct to parse the json string

这时候 llama3 应该是混乱了。

Here's how you can refactor the above code using structs:

```go
package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
)

type Meaning struct {
	PartOfSpeech string   `json:"partOfSpeech"`
_DEFINITIONS  []Definition `json:"definitions"`
}

type Definition struct {
	Definition    string `json:"definition"`
	Example       string `json:"example,omitempty"`
	Synonyms      []string `json:"synonyms,omitempty"`
	Antonyms      []string `json:"antonyms,omitempty"`
}

func main() {
	word := "hello"

	url := fmt.Sprintf("https://api.dictionaryapi.dev/api/v2/entries/en/%s", word)
	resp, err := http.Get(url)
	if err != nil {
		panic(err)
	}
	defer resp.Body.Close()

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		panic(err)
	}

	var data []Entry
	err = json.Unmarshal(body, &data)
	if err != nil {
		panic(err)
	}

	for _, entry := range data {
		fmt.Println("Word:", entry.Word)
		for _, meaning := range entry.Meanings {
			fmt.Println("Part of speech:", meaning.PartOfSpeech)
			for _, definition := range meaning._DEFINITIONS {
				fmt.Println("Definition:", definition.Definition)
				if definition.Example != "" {
					fmt.Println("Example:", definition.Example)
				}
				if len(definition.Synonyms) > 0 {
					fmt.Println("Synonyms:", definition.Synonyms)
				}
				if len(definition.Antonyms) > 0 {
					fmt.println("Antonyms:", definition.Antonyms)
				}
			}
		}
	}
}

type Entry struct {
	Word       string     `json:"word"`
	Pronunciation string    `json:"phonetic"`
	Pronunciations []Pronunciation `json:"phonetics"`
	Origin      string     `json:"origin"`
	Meanings    []Meaning  `json:"meanings"`
}

type Pronunciation struct {
	Text  string `json:"text"`
	Audio string `json:"audio"`
}
```

In this code, I've defined three structs: `Meaning`, `Definition`, and `Entry`. The `Meaning` struct has a part of speech and a slice of definitions. The `Definition` struct has a definition, example, synonyms, and antonyms. The `Entry` struct has a word, pronunciation, origin, and meanings.

I then used these structs to unmarshal the JSON response from the API. This makes the code more readable and easier to maintain, as it separates the logic of parsing the JSON into its constituent parts from the logic of printing out the results.

意思对了，但是代码不够准确，稍微复杂一点的代码，llama3 处理起来还是有难度的。

### 结论

测试人员福音，很多公司访问不了 chatgpt 等国外的 ai 站点，用这个本地写写简单的测试用例还是有搞头的，很多测试同学的代码能力其实并不强，可以用本地 llm 来帮忙检查代码或者生成部分代码，应该能节约不少时间。

### 本文用到的工具

- ollama
- [openwebui](https://openwebui.com/)
- Raycast llama3 插件
- vscode continue 插件

### 彩蛋

这是我不小心发现的 1 个软件测试的 system prompt，有兴趣的同学可以试试。

```
SYSTEM """
As a certified Software Testing expert, I am equipped to provide comprehensive assistance in Software Testing using official ISTQB terminology and methodologies. My expertise encompasses roles such as Test Analyst, Technical Test Analyst and Test Manager. I offer training and education in Software Testing, providing in-depth knowledge and practical insights.

As specialist, I interactively assist organizations in implementing robust test processes, concepts and strategies step by step. Additionally, I support individuals in their day-to-day software testing tasks, carrying out work steps, offering expert advice and solutions tailored to specific software testing challenges. For example, clients may provide test cases, requirements documentation and bug reports to aid in the testing process. To streamline my assistance, I recommend that clients upload relevant work items using Open WebUI with document upload support <https://docs.openwebui.com>. Alternatively, text input can be provided when Open WebUI is not available.

For adherence to ISTQB standards, clients are encouraged to use Open WebUI together with glossary, syllabus, and text exam documents uploaded from <https://www.istqb.org/certifications/>. This will ensure that my assistance is aligned with the latest industry best practices and standards. Together, we can achieve exceptional results in Software Testing.
"""

```
