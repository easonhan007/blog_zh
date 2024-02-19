---
title: "AI大语言模型在自动化用例生成中的探索"
date: 2024-02-19T11:53:47+08:00
draft: false
---

最近读到[这篇文章](https://drlee.io/implementing-ai-in-software-testing-creating-a-text-generation-model-for-test-automation-7294b26f93c4)，原文在是https://drlee.io/implementing-ai-in-software-testing-creating-a-text-generation-model-for-test-automation-7294b26f93c4，里面涉及到一些基于ai进行自动化测试的探索，原文是这么说的：

> 将人工智能 (AI) 纳入软件测试可谓是游戏规则的改变者，能够显著提升效率和有效性。本文利用 OpenAI 的文本生成模型——尤其是 GPT-3.5-turbo 和 GPT-4-turbo-preview——在 Google Colab 中构建了一个文本生成模型，重点关注测试自动化用例。

看了一下，里面列举了3个测试用例。

**The system shall allow users to securely login with a username and password.**

这是用户登录的用例。

**Ensure that the shopping cart allows users to add items, remove items, and proceed to checkout.** 

这是购物车的用例。

**The weather API should return a JSON response with fields for temperature, humidity, and precipitation forecast for the next 5 days.**

这是用生成基于json返回值的天气api的用例。

下面是ai生成的购物车用例，看起来还是比较完备的。

```
Regression Test Scenarios for Shopping Cart Feature:
1. Test Case: Adding items to the shopping cart
- Verify that the user can add a single item to the shopping cart.
- Verify that the user can add multiple items to the shopping cart.
- Verify that the quantity of the added items is correctly displayed in the shopping cart.
- Verify that the total price of the added items is correctly calculated and updated in the shopping cart.
- Verify that the user is able to add items with different variations (e.g., size, color).
2. Test Case: Removing items from the shopping cart
- Verify that the user can remove a single item from the shopping cart.
- Verify that the user can remove multiple items from the shopping cart.
- Verify that the quantity and total price of the removed items are correctly updated in the shopping cart.
- Verify that the user is able to remove items with different variations.
3. Test Case: Proceeding to checkout
- Verify that the user can proceed to the checkout page from the shopping cart.
- Verify that the user is redirected to the correct checkout page.
- Verify that the items in the shopping cart are correctly displayed in the checkout page.
- Verify that the total price of the items in the shopping cart is correctly displayed in the checkout page.
- Verify that the user is able to navigate back to the shopping cart from the checkout page.
```

后面的工作就是人工介入查缺补漏，然后导入用例管理工具。

本身代码也很简单。

```python
def generate_test_cases(requirement):
    response = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": "You are a helpful assistant capable of generating software test cases."},
        {"role": "user", "content": requirement}
      ]
    )
    return response.choices[0].message.content

feature_description = "Ensure that the shopping cart allows users to add items, remove items, and proceed to checkout."
regression_tests = generate_regression_tests(feature_description)
print(regression_tests)
```

### 总结

总的来看这篇文章的没什么太多新意，客观上讲目前ai直接生成的用例是不能直接使用的，需要进行一定的加工和优化，不过另一方面我们也必须注意到

- AI确实可以辅助我们进行测试用例的编写，有一定的提效效果
- AI的使用门槛确实很低，只需要几行代码就可以实现之前完全无法想象的功能
- AI生成的用例可能在教学演示中会有不错的应用，毕竟ai在短时间内创造材料的能力是人类所无法达到的


