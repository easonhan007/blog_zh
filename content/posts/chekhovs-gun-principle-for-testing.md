---
title: "测试用例设计中的契诃夫之枪原则"
date: 2024-11-22T09:15:23+08:00
draft: false
---

看到一篇跟用例数据准备相关的文章，觉得挺有道理的。我之前在设计用例数据的时候就会犯类似的错误，这篇文章其实说的非常在理。

翻译了一下[原文](https://solid-dry-kiss.hashnode.dev/chekhovs-gun-principle-for-testing)，供大家参考。

编写测试用例更像是讲故事而非纯技术工作，这种观点并不罕见。最近我在 The Bike Shed 播客中听到这个观点，而且在博客文章和会议演讲中也经常能看到类似的讨论。既然测试编写是一种讲故事的艺术，那么我们是否应该借鉴叙事原则来改进我们的测试呢？

谈到讲故事的原则，首先想到的就是契诃夫之枪原则。这个原则是什么？用安东·契诃夫自己的话说（引自大英百科全书）：

> 如果在舞台上放置了一支上膛的步枪，那么它就必须被开火。不要做出你不打算履行的承诺。

大英百科全书还给出了如下定义：

> 这是一条适用于戏剧、文学和其他叙事形式的原则，它强调故事中引入的每个元素都应该对情节发展必不可少。

那么这个原则如何应用到我们的测试编写中呢？想象一下你正在为电商系统编写测试用例。你有不同类别的产品，这些类别对买家有一些限制条件。最明显的例子就是不能向未满十八岁的人销售酒类产品。在我们的例子中，这类人群不能将这些产品添加到购物车。

让我们看一个测试代码示例（我使用的是 Elixir，但这个原则适用于大多数编程语言）：

```elixir
test "don't allow adding products to cart when age constraint is not met" do
  buyer = %Person{
    name: "John Smith",
    age: 17,
    country: :uk,
    registered_on: ~U[2023-09-16T18:17:22Z]
  }

  category = %Category{
    name: "Alcohol",
    external_id: 3242,
    constraints: [
      %AgeConstraint{min: 18}
    ]
  }

  product = %Product{
    name: "Triple Hazy IPA",
    category: category,
    sku: "TRI-557",
    added_at: ~U[2022-01-01T12:16:54Z]
  }

  cart = Cart.init(buyer)

  assert Cart.add(cart, product, quantity: 2) == {:error, :constraint_violated}
end
```

这个测试本身并不算糟糕，但它在多处违反了契诃夫之枪原则。在我们测试的"准备"阶段引入的每个标量都是契诃夫意义上的"枪"。它们都被放在了舞台上，读者可能会期待它们都会"开火"。这里我们有 10 个标量，相当于舞台上放了 11 把枪。什么是"开火"？就是当我们把这个值改成其他值时，测试应该失败。让我们检查一下这些标量：

- `name: "John Smith"`: 无论改成什么，测试都不会失败
- `age: 17`: 如果改成 18 或 22，测试会失败
- `country: :uk`: 不会失败（除非我们实现了基于国家的限制，但目前没有）
- `registered_on: <date>`: 无关紧要
- `name: "Alcohol"`: 无关紧要
- `external_id: 3242`: 这是什么？无关紧要
- `min: 18`: 改成 15 会导致测试失败
- 产品中剩余的 name、sku 和添加日期都不会影响测试
- `quantity: 2`: 同样无关紧要

总结一下，我们的 11 个"枪"中只有两个会"开火"，约 18%。其余的都是纯粹的干扰，如果读者试图理解测试的动态性，这些都会让他们误入歧途。

如何改进呢？通过使用抽象！测试和常规代码一样需要抽象。而且就像常规代码一样，你需要确保在特定上下文中使用正确的抽象。这里一个潜在的抽象就是工厂方法。让我们看看改进后的版本：

```elixir
test "don't allow adding products to cart when age constraint is not met" do
  buyer = person_factory(age: 17)
  category = category_factory(constraints: [%AgeConstraint{min: 18}])
  product = product_factory(category: category)

  cart = Cart.init(buyer)

  assert Cart.add(cart, product) == {:error, :constraint_violated}
end
```

测试明显变短了，只有 5 行非空代码。这里的每个标量都很重要，而且只有两个。这样我们就不会让读者负担过重，他们能够快速得出结论：啊，买家 17 岁，但限制要求至少 18 岁，所以返回了 `:constraint_violated` 错误。这很合理。

## 推论：让你的"枪"显而易见

这是我对叙事原则的补充：

> 如果某些东西要"开火"，要提前展示它。

人们通常不喜欢"机械降神"式的剧情。如果某个东西对测试通过很重要，就要明确地展示它。不要把它藏在抽象之下。

想象一下，在上面的测试中，第一行只是写着 `buyer = person_factory()`。在代码审查时被问到这一点，开发者说工厂中的默认年龄实际上是 17，所以没必要重复。这是对抽象的误用。不要依赖于隐藏的内容。理论上来说，任何人都应该能够进入工厂修改这些值 - 而测试应该仍然通过。有些人甚至认为工厂中的默认值应该是随机的。

## 总结

要让你的测试用例更好、更易读（更好地讲述故事），就要删除所有与测试流程无关的数据。只保留重要的内容 - 那些改变后会导致测试失败的值。另一方面，不要在抽象中隐藏重要的内容。让叙事流程清晰明了，不要让读者感到困惑。
