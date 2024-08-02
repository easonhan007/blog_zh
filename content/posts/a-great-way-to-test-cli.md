---
title: "如何优雅的测试cli应用"
date: 2024-08-02T17:33:25+08:00
draft: false
---

之前写过一篇文章讨论如何去做hello world的单元测试，当时想到的一个方法是将hello world抽象成1个函数，这个函数返回hello world字符串，然后测试这个函数的返回值就好了，代码大概如下所示。

```
def hello_world():
    return "hello world"
```

前几天看到rust cli手册里的一个做法，比上面的方案更加的合理，这里忍不住分享一下。

## 更优雅的解决方案

测试功能有两种互补的方法:测试构建完整应用程序的小单元,这些称为"单元测试"。还有从"外部"测试最终应用程序,称为"黑盒测试"或"集成测试"。让我们从第一种开始。

为了弄清楚我们应该测试什么,让我们看看我们的程序功能是什么。主要来说,grrs应该打印出与给定模式匹配的行。因此,让我们为此编写单元测试:我们要确保我们最重要的逻辑能正常工作,并且我们要以一种不依赖于周围任何设置代码(例如处理CLI参数)的方式来做到这一点。

回到我们对grrs的第一个实现,我们在main函数中添加了这段代码:

```rust
// ...
for line in content.lines() {
    if line.contains(&args.pattern) {
        println!("{}", line);
    }
}
```

遗憾的是,这不太容易测试。首先,它在main函数中,所以我们不能轻易调用它。这可以通过将这段代码移到一个函数中来轻松解决:

```rust
fn find_matches(content: &str, pattern: &str) {
    for line in content.lines() {
        if line.contains(pattern) {
            println!("{}", line);
        }
    }
}
```

现在我们可以在测试中调用这个函数,看看它的输出是什么:

```rust
#[test]
fn find_a_match() {
    find_matches("lorem ipsum\ndolor sit amet", "lorem");
    assert_eq!( // 呃呃呃
```

或者...我们能吗？现在,find_matches直接打印到stdout,即终端。我们不能在测试中轻易捕获这个!这是在实现之后编写测试时经常出现的问题:我们编写了一个与使用它的上下文紧密集成的函数。

注意:在编写小型CLI应用程序时,这完全没问题。不需要让一切都可测试!然而,思考你可能想要为代码的哪些部分编写单元测试是很重要的。虽然我们将看到改变这个函数使其可测试很容易,但情况并非总是如此。

好的,我们怎样才能让它可测试呢?我们需要以某种方式捕获输出。Rust的标准库有一些处理I/O(输入/输出)的巧妙抽象,我们将使用其中一个叫做std::io::Write的。这是一个抽象了我们可以写入的东西的trait,包括字符串但也包括stdout。

如果这是你第一次在Rust上下文中听到"trait"这个词,那你有福了。Trait是Rust最强大的特性之一。你可以把它们想象成Java中的接口,或者Haskell中的类型类(取决于你更熟悉哪个)。它们允许你抽象可以由不同类型共享的行为。使用trait的代码可以以非常通用和灵活的方式表达想法。这也意味着它可能变得难以阅读。不要让这吓到你:即使使用Rust多年的人也不总是立即理解泛型代码在做什么。在这种情况下,考虑具体用途会有帮助。例如,在我们的例子中,我们抽象的行为是"写入它"。实现("impl")它的类型的例子包括:终端的标准输出,文件,内存中的缓冲区,或TCP网络连接。(向下滚动std::io::Write的文档以查看"实现者"列表。)

有了这些知识,让我们改变我们的函数以接受第三个参数。它应该是任何实现Write的类型。这样,我们就可以在测试中提供一个简单的字符串,并对其进行断言。这是我们如何编写这个版本的find_matches:

```rust
fn find_matches(content: &str, pattern: &str, mut writer: impl std::io::Write) {
    for line in content.lines() {
        if line.contains(pattern) {
            writeln!(writer, "{}", line);
        }
    }
}
```

新参数是mut writer,即一个可变的我们称之为"writer"的东西。它的类型是impl std::io::Write,你可以理解为"任何实现Write trait的类型的占位符"。还要注意我们如何用writeln!(writer, …)替换了之前使用的println!(…)。println!的工作方式与writeln!相同,但总是使用标准输出。

现在我们可以测试输出:

```rust
#[test]
fn find_a_match() {
    let mut result = Vec::new();
    find_matches("Loren ipsum\ndolor sit amet", "lorem", &mut result);
    assert_eq!(result, b"lorem ipsum\n");
}
```

要在我们的应用程序代码中使用这个,我们必须通过添加&mut std::io::stdout()作为第三个参数来改变main中对find_matches的调用。这里是一个main函数的例子,它基于我们在前几章中看到的内容,并使用我们提取的find_matches函数:

```rust
fn main() -> Result<()> {
    let args = Cli::parse();
    let content = std::fs::read_to_string(&args.path)
        .with_context(|| format!("could not read file `{}`", args.path.display()))?;

    find_matches(&content, &args.pattern, &mut std::io::stdout());

    Ok(())
}
```

注意:由于stdout期望字节(而不是字符串),我们使用std::io::Write而不是std::fmt::Write。因此,我们在测试中给出一个空数组作为"writer"(它的类型将被推断为Vec<u8>),在assert_eq!中我们使用b"foo"。(b前缀使这成为一个字节字符串字面量,所以它的类型将是&[u8]而不是&str)。

注意:我们也可以让这个函数返回一个String,但那会改变它的行为。它不会直接写入终端,而是将所有内容收集到一个字符串中,并在最后一次性转储所有结果。

读者练习:writeln!返回一个io::Result,因为写入可能失败,例如当缓冲区已满且无法扩展时。为find_matches添加错误处理。

我们刚刚看到了如何使这段代码易于测试。我们

识别了我们应用程序的核心部分之一,
将它放入自己的函数中,
并使它更加灵活。
尽管目标是使它可测试,但我们最终得到的结果实际上是一段非常惯用和可重用的Rust代码。这太棒了!

## 总结

这里优雅的部分在于主体功能并没有因为测试而进行一些很不自然的重构，比如我之前解决方案中返回hello world的函数。

这里直接用了一个类似于buffer的解决方案，把需要打印的内容放到1个result writer里，可以简单理解成是缓存起来了，而且可以直接读出来，我们只要断言读出来的那部分结果就好了。

更值得称道的是，这里用了trait的方式进行了泛化处理，使得任何实现了`Write trait`的类型都可以作为参数传进去，并进行测试。




