---
title: "用起来，在提交代码时实现自动化验证"
date: 2024-05-10T09:27:45+08:00
draft: false
---

不怕开发写 bug，就怕开发带私货，这应该是很多小伙伴都经历过的职场噩梦。目前看来一个比较好的方案就是在开发提交的时候进行一些自动化的检查，让夹带私货这件事情成本提高，从而减少这种情况的发生。

### 1. 我们可以在代码提交时进行哪些检查

- Linters：Linters 是分析源代码以找到编程问题、语法错误和其他潜在问题的工具。流行的例子包括 pylint、flake8 和 pyflakes。
- 代码格式化器：代码格式化器自动化根据预定义的样式约定格式化源代码的过程。示例包括 black、autopep8 和 yapf。
- 自动化测试：自动化测试，如单元和集成测试，对于确保代码的功能性和质量至关重要。框架如 unittest、pytest 和 nose 允许以自动化方式编写和运行测试。
- 静态代码分析：静态分析工具如 bandit（用于检测安全问题）、mypy（用于静态类型检查）和 prospector（集成了几个静态分析器）可以在不需要运行代码的情况下识别潜在问题。这些工具可以帮助找到安全漏洞、逻辑错误和可能的性能改进。

好的，那么……我们如何在我们的项目中应用这些测试/分析呢？别担心，这就是 Pre-commit 的用武之地。

### 2. Pre-commit

pre-commit 是一个用于管理和维护多语言 pre-commit 钩子的框架。我们称之为“钩子”的是一个脚本或一组命令，它们会自动执行。但是，我们什么时候要执行这些测试呢？

这个工具允许我们配置一组质量测试，在运行 git 命令（commit、push 等）之前自动执行。这在某种意义上非常强大，因为每次我们修改 git 仓库时，我们都可以确保添加的代码遵循我们设定的质量规则。

#### 2.1 Pre-commit: 安装

要安装 pre-commit，首先执行以下命令行：

```
pip install pre-commit
```

#### 2.2 Pre-commit: 仓库结构

为了配置 pre-commit，我们需要 2 个文件，这些文件必须位于根文件夹中。这些文件是.pre-commit-config.yaml 和 pyproject.toml。

```
project/
├── src/
├── .pre-commit-config.yaml
└── pyproject.toml
```

.pre-commit-config.yaml：必需。配置 QA 流水线。它包含要在执行 git 命令之前执行的每个钩子。
pyproject.toml：可选。配置文件，由打包工具以及其他工具（如 linters、类型检查器等）使用。它允许更具体的钩子配置。

#### 2.3 Pre-commit: QA 流水线

现在，让我们看看如何修改这些文件。首先，我们将看到一个简单的.pre-commit-config.yaml 配置示例：

```
repos:
-   repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v2.3.0
    hooks:
    -   id: check-yaml
    -   id: end-of-file-fixer
    -   id: trailing-whitespace
-   repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.4.2
    hooks:
    -   id: ruff
        args: [ --fix ]
    -   id: ruff-format
```

在这种情况下，我们定义了 5 个步骤（每个 ID 一个），其中前三个将检查 yaml 语法、文件结尾和尾随空格。最后两个钩子来自 Ruff（一个新的强大的 linter）。让我们了解文件的结构。

- repo：存储库位于的 URL。否则可以是本地的，如果我们要执行自定义钩子。
- rev：我们要使用的版本标签。
- hooks：我们在其中指定我们要使用的该 repo 的所有钩子。
- id：特定钩子的 ID。

对于每个钩子，我们可以指定更多参数，如 types、stages 等。我们可以在官方文档中查看列表。

另一方面，有些工具还可以加入进来，所以，在这种情况下，我们将在 pyproject.toml 文件中更具体：

```
# 其他Pyproject内容
# ...

# Ruff钩子配置
[tool.ruff]
line-length = 88
```

在这个示例中，我们配置了 Ruff，以强制我们的代码行长度不超过 88 个字符。要知道您可以在此文件中设置哪些配置，您将需要访问官方包网站并进行研究。

#### 2.4 Pre-commit: 执行

在执行它们之前，我们需要安装使用的钩子。Pre-commit 默认会在隔离的虚拟环境中安装所有来自钩子的依赖项，所以我们不必担心与我们的包发生冲突。这很酷！然而，如果我们想强制 pre-commit 使用与同一环境中安装的库，我们将需要强制所有执行的钩子都是自定义的（在下一节中解释）。

因此，无论钩子是否使用隔离的 venv 来处理依赖项，我们都需要安装它们。为此，我们使用以下命令行：

```
pre-commit install
```

之后，如果需要，我们可以安装额外的钩子类型。在这种情况下，我发现安装 commit-msg 和 pre-push 很有趣。这使我们能够在提交消息或进行推送之前配置自动执行。

```
pre-commit install --hook-type commit-msg --hook-type pre-push
```

从现在开始，pre-commit 将监听所有 git 执行（commit、push 等）并将在其 stages 参数中定义的所有钩子执行。默认情况下，所有都设置为在每次 git 提交时执行。

否则，我们可以使用以下命令行手动运行它：

```
# 在一组文件上运行
pre-commit run --files file1 file2 ...

# 在所有文件上运行
pre-commit run --all-files
```

#### 2.5 自定义钩子

自定义钩子可以提供更加灵活和强大的检查。

接下来是自定义钩子的实现（check_file_extensions.py）。

```python
import sys
from pathlib import Path
from typing import List
import configargparse

def check_file_extensions(
    file_extensions: List[Path],
    files: List[Path],
) -> List[Path]:
    """
    查找具有不需要的格式的文件。
    参数
    ----------
    file_extensions : List[Path]
        我们要检查的扩展名。
    files : List[Path]
        要检查的文件。
    返回
    -------
    List[Path]
        返回具有不正确格式的文件列表。
    """
    invalid_files = []
    for file_path in files:
        if (
            file_path.is_file()
            and file_path.suffix.lower() in file_extensions
            and not str(file_path).startswith(".")
        ):
            invalid_files.append(file_path)
    return invalid_files

if __name__ == "__main__":
    # 解析参数
    parser = configargparse.ArgumentParser(description="文件扩展名检查器")
    parser.add_argument(
        "--formats",
        nargs="+",
        required=True,
        help="不需要的文件扩展名列表",
        type=str.lower,
    )
    parser.add_argument(
        "--files",
        nargs="+",
        required=True,
        help="文件列表",
        type=Path,
    )
    args = parser.parse_args()
    # 检查无效格式文件
    invalid_files = check_file_extensions(
        args.formats,
        args.files,
    )
    if invalid_files:
        print("文件具有与以下不同的格式：")
        for file_path in invalid_files:
            print(file_path)
        sys.exit(1)
```

一旦实现了钩子，它需要以以下方式添加到配置文件.pre-commit-config.yaml 中：

```
repos:
  # 自定义钩子
  - repo: local
    hooks:
    - id: my-custom-hook
      name: extension-file-checker
      entry: python qa_code/custom_hooks/check_file_extensions.py  # 脚本路径
      types: [file]
      language: system
      args: ["--formats", ".json", "--files"]
      require_serial: true
      pass_filenames: true
      stages: [commit, manual]
```

这个配置指定了以下内容：

- repo: 由于它是本地的，定义了一个自定义钩子。
- id: 显示的新钩子的 ID。
- name: 显示的新钩子的名称。
- entry: 执行钩子的命令。
- language: 执行钩子的语言。设置为 system 将强制使用当前环境中安装的库。否则，pre-commit 将创建一个虚拟环境来安装必要的依赖项。
- args: 脚本接收的参数。
- require_serial: 强制执行不并行完成。
- additional_dependencies: 启动钩子所需的依赖项。
- pass_filenames: 定义是否将所有要分析的文件作为参数传递。
- stages: 我们希望钩子在什么阶段执行 在这种情况下，每次我们想进行 git 提交时，也可以手动使用 pre-commit 命令。

### 3. Pre-commit 配置实例

下面一些钩子都比较实用。

- check-added-large-files：来自 Pre commit hooks。检查是否上传了大文件。
- check-yaml：来自 Pre commit hooks。检查.yaml 文件是否正确编写。
- check-toml：来自 Pre commit hooks。检查.toml 文件是否正确编写。
- end-of-file-fixer：来自 Pre commit hooks。检查文件是否以新行结束。
- trailing-whitespace：来自 Pre commit hooks。删除尾随空格。
- ruff：来自 Ruff。运行代码质量检查。应用 PEP8 约定、语法错误、代码复杂性等检查。
- ruff-format：来自 Ruff。根据特定样式自动格式化代码。一些示例包括：代码对齐、空白、行长度等。
- numpydoc：来自 Numpydoc。验证 docstrings 是否符合 numpy 格式。
- mypy：来自 Mypy。分析代码中与数据类型相关的错误，并在代码执行前提供可能的类型问题信息。
- vulture：来自 Vulture。帮助识别不运行的代码，可能安全地删除。
- commitizen：来自 Commitizen。用于确保确认消息遵循特定格式。
- commitizen-branch：来自 Commitizen。用于确保分支名称遵循特定格式。
- nbstripout：来自 Nbstripout。允许您在提交更改之前从 Jupyter 笔记本单元格中删除运行输出。
- pytest-check：来自自定义钩子。使用 pytest 运行一组单元测试。
- extension-file-checker：来自自定义钩子。允许您检查是否添加了具有特定扩展名的文件。

这是一个.pre-commit-config.yaml 例子。

```
# 适用于python>=3.8的pre-commit配置文件
repos:
  - repo: local
    hooks:
      # Pre commit hooks https://github.com/pre-commit/pre-commit-hooks
      - id: check-added-large-files
        name: check for added large files
        description: prevents giant files from being committed.
        entry: check-added-large-files
        language: system
        args: ['--maxkb=123']
        stages: [commit, manual]
      - id: check-yaml
        name: check yaml
        description: checks yaml files for parseable syntax.
        entry: check-yaml
        language: system
        types: [yaml]
        stages: [commit, manual]
      - id: check-toml
        name: check toml
        description: checks toml files for parseable syntax.
        entry: check-toml
        language: system
        types: [toml]
        stages: [commit, manual]
      - id: end-of-file-fixer
        name: fix end of files
        description: ensures that a file is either empty, or ends with one newline.
        entry: end-of-file-fixer
        language: system
        types: [python]
        exclude: ^data/mlruns/
        stages: [commit, manual]
      - id: trailing-whitespace
        name: trim trailing whitespace
        description: trims trailing whitespace.
        entry: trailing-whitespace-fixer
        language: system
        types: [text]
        exclude: ^data/mlruns/
        stages: [commit, manual]
      # Ruff hooks https://github.com/astral-sh/ruff-pre-commit
      - id: ruff # Linter
        name: ruff
        description: "Run 'ruff' for extremely fast Python linting"
        entry: ruff check --force-exclude
        language: system
        require_serial: true
        types_or: [ python, pyi ]
        args: [ --fix]
        stages: [commit, manual]
      - id: ruff-format # Formatter
        name: ruff-format
        description: "Run 'ruff format' for extremely fast Python formatting"
        entry: ruff format --force-exclude
        language: system
        exclude:
          '^(docs/|notebooks/demo_custom_argparse/)'
        types_or: [ python, pyi, jupyter ]
        require_serial: true
        stages: [commit, manual]
      # Numpy docstrings https://github.com/numpy/numpydoc
      - id: numpydoc-validation
        name: numpydoc-validation
        description: This hook validates that docstrings in committed files adhere to numpydoc standards.
        entry: python -m numpydoc.hooks.validate_docstrings
        require_serial: true
        language: system
        exclude:
          '^(docs/|notebooks/demo_custom_argparse/)'
        types: [python]

```

### 总结

总的来说下面这些钩子是完全可以用起来的。

- 代码风格扫描，代码语法扫描，静态代码分析，代码自动格式化
- 配置文件扫描，比如 yaml 和 json 的语法扫描
- 文件保护扫描，一些核心文件我们不希望进行变动
- 自动化用例执行，一般情况下推荐执行单元测试，毕竟扫描的时候需要速度优先
