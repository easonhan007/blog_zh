---
title: "Playwright v1.50.5发布了"
date: 2025-02-14T09:23:25+08:00
draft: false
---

Playwright v1.50.0 引入了多项值得关注的功能和改进，旨在提升测试体验。以下是这些新增功能的详细概述，并附有示例以说明其使用方法。

## Runner 增强

### 1. 步骤超时配置

现在可以通过 timeout 选项为单个测试步骤指定最大运行时间。如果某个步骤的运行时间超过此限制，测试将失败。

示例：

```javascript
test("example test", async ({ page }) => {
  await test.step(
    "step with timeout",
    async () => {
      // 此步骤必须在 1000 毫秒内完成
      await page.click("#some-button");
    },
    { timeout: 1000 }
  );
});
```

### 2. 跳过测试步骤

新增的`test.step.skip()`方法允许跳过特定的测试步骤，这在某些条件未满足或功能尚未实现的情况下非常有用。

示例：

```javascript
test("some test", async ({ page }) => {
  await test.step("before running step", async () => {
    // 正常步骤
  });

  await test.step.skip("not yet ready", async () => {
    // 此步骤将被跳过
  });

  await test.step("after running step", async () => {
    // 即使上一步被跳过，此步骤仍会运行
  });
});
```

### 3. ARIA 快照存储于单独文件

`expect(locator).toMatchAriaSnapshot()`方法已扩展，允许将 ARIA 快照存储在单独的 YAML 文件中，便于更好地组织和版本控制。

示例：

```javascript
test("ARIA snapshot test", async ({ page }) => {
  await page.goto("https://example.com");
  await expect(page.locator("body")).toMatchAriaSnapshot();
});
```

在此示例中，ARIA 快照将存储在对应的 YAML 文件中。

### 4. 可访问性错误消息断言

新增方法`expect(locator).toHaveAccessibleErrorMessage()`，可用于断言某个定位器指向的元素具有特定的 ARIA 错误消息。

示例：

```javascript
test("accessible error message test", async ({ page }) => {
  await page.goto("https://example.com/form");
  await page.click("#submit-button");
  const input = page.locator("#username");
  await expect(input).toHaveAccessibleErrorMessage("Username is required");
});
```

### 5. 快照更新配置

`testConfig.updateSnapshots`选项现在包含一个新的枚举值。将此选项设置为`changed`时，仅更新已更改的快照；设置为`all`时，无论是否有差异，都会更新所有快照。

命令行示例：

```
npx playwright test --update-snapshots=changed

```

### 6. 源代码更新方法配置

新增选项`testConfig.updateSourceMethod`，定义在配置`testConfig.updateSnapshots`时如何更新源代码。可用模式包括 overwrite、3-way 和 patch。

命令行示例：

```text
npx playwright test --update-snapshots=changed --update-source-method=3way
```

### 7. Web 服务器的优雅关闭

`testConfig.webServer`选项现在包含一个`gracefulShutdown`字段，允许你指定一个进程终止信号，而不是默认的`SIGKILL`。

配置示例：

```javascript
// playwright.config.js
module.exports = {
  webServer: {
    command: "npm run start",
    port: 3000,
    gracefulShutdown: "SIGTERM",
  },
};
```

### 8. 访问测试步骤附件

现在在报告器 API 中公开了`testStep.attachments`属性，允许检索特定测试步骤创建的所有附件。

示例：

```javascript
class CustomReporter {
  onStepEnd(test, result, step) {
    const attachments = step.attachments;
    // 按需处理附件
  }
}
```

## 用户界面更新

### 1. 增强的 HTML 报告器

默认的 HTML 报告器已更新，改进了附件的显示方式，提供更直观和信息丰富的布局。

### 2. ARIA 快照元素选择器

UI 中新增了一个按钮，用于选择生成 ARIA 快照的元素，简化了创建无障碍性测试的流程。

### 3. 详细的行动信息

现在在追踪中会显示额外的细节，例如在行动中按下的按键，这些信息会与 API 调用一起显示，为测试执行提供更深入的洞察。

### 4. 默认禁用 Canvas 内容显示

由于可能引发错误，现在默认禁用在追踪中显示`<canvas>`内容。可以通过 UI 中的“显示 Canvas 内容”设置启用。

### 5. 增强的计时信息

“调用”和“网络”面板现在显示额外的计时信息，有助于性能分析和调试。

## 破坏性变更

### 1. 可编辑元素断言

如果目标元素不是`<input>`、`<select>`或其他已识别的可编辑元素，`expect(locator).toBeEditable()`和`locator.isEditable()`方法现在会抛出错误。

示例：

```javascript
const element = page.locator("#non-editable-element");
await expect(element).toBeEditable(); // 抛出错误
```

2. 快照更新行为

将`testConfig.updateSnapshots`设置为`all`时，现在会更新所有快照，而不仅仅是失败或已更改的快照。要保留之前仅更新已更改快照的行为，请使用新的`changed`枚举值。

命令行示例：

```
npx playwright test --update-snapshots=changed

```

## 浏览器版本更新

Playwright v1.50.0 包含以下浏览器版本：

• Chromium 133.0.6943.16

• Mozilla Firefox 134.0

• WebKit 18.2

## 结论

Playwright v1.50.0 带来了显著的改进，提升了测试效率、无障碍性验证和调试能力。新的步骤超时配置、步骤跳过和 ARIA 快照增强功能提高了测试执行的健壮性。Web 服务器的优雅关闭和追踪中详细的行动信息为开发者提供了更友好的测试体验。此外，诸如更严格的可编辑元素断言等破坏性变更，进一步增强了测试的可靠性。
