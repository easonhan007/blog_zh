---
title: "使用重试模式来提升自动化测试的稳定性"
date: 2023-07-03T12:01:01+08:00
draft: false
---

看到一篇非常好的关于在自动化测试中引入重试模式的文章，https://www.thegreenreport.blog/articles/enhancing-automation-reliability-with-retry-patterns/enhancing-automation-reliability-with-retry-patterns.html 忍不住跟大家分享一下。

自动化测试，特别是ui自动化的稳定性提升是非常困难的，出错了就重试这个简单的策略可以帮助我们处理一些难以预料的异常情景，从而提升测试的整体稳定性。

这篇文章的作者就分享了几种重试的设计模式，通俗易懂而且相当实用。

### 动态重试

```javascript
async function dynamicRetry(actions, maxRetries) {
    let retryCount = 0;
                          
    async function retryAction() {
        try {
            return await actions();
        } catch (error) {
            if (retryCount < maxRetries) {
                retryCount++;
                return retryAction();
            } else {
                throw error;
            }
        }
    }
    return await retryAction();
}

               
it("Testing the dynamic retry pattern", async () => {
    await demoPage.navigateToDemoPageTextBoxes();
    await browser.pause(1000);
    await dynamicRetry(async () => {
        await demoPage.fillFullName("John Doe");
        await demoPage.fillEmail("test@gmail.com");
        await demoPage.fillCurrentAddress("test address");
        await demoPage.clickFakeButton();
    }, 3);
});

```
该模式的核心是设置一个最大的重试次数，每次重试过后次数加一，直到达到阈值。


### 轮询重试

另一种常见的重试模式是使用超时和轮询。这种方法会重复检查一组操作是否成功完成或者是否达到了超时时间。

```javascript
               
async function pollRetry(actions, timeout, pollInterval) {
    const startTime = Date.now();
    let lastError;
                          
    while (Date.now() - startTime < timeout) {
        try {
            await actions();
            return;
        } catch (error) {
            lastError = error;
            await sleep(pollInterval);
        }
    }
                          
    throw lastError;
}
                          
function sleep(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
}

               
it("Testing the poll retry pattern", async () => {
    await demoPage.navigateToDemoPageTextBoxes();
    await browser.pause(1000);
    await pollRetry(
        async () => {
            await demoPage.fillFullName("John Doe");
            await demoPage.fillEmail("test@gmail.com");
            await demoPage.fillCurrentAddress("test address");
            await demoPage.clickFakeButton();
        },
        20000,
        5000
    );
});

```
这个模式的核心是设置一个总的超时时间，如果在这个时间段内发生了异常，那么就每隔一段时间重试一下。

selenium的wait unitl 接口就是这种重试模式。



### 异常重试

这是最常见的一种重试方式，好处是可以针对不同的异常执行不同的重试策略。

```javascript
               
function errorHandlingRetry(actions) {
    return new Promise(async (resolve, reject) => {
        try {
            await actions();
            resolve();
        } catch (error) {
            if (error instanceof ElementNotFoundError) {
                // Handle the case when the element is not found
			    console.error("Element not found:", error.elementSelector);
			    await sleep(1000);
			    await actions();
            } else if (error instanceof TimeoutError) {
                // Handle the case when a timeout occurs
			    console.error("Timeout occurred:", error.message);
			    await sleep(500);
			    await actions();
            } else {
                // Handle other types of errors
				console.error("An error occurred:", error);
            }
            reject(error);
        }
    });
}

it("Testing the error handling retry pattern", async () => {
    await demoPage.navigateToDemoPageTextBoxes();
    await browser.pause(1000);
    await errorHandlingRetry(async () => {
        await demoPage.fillFullName("John Doe");
        await demoPage.fillEmail("test@gmail.com");
        await demoPage.fillCurrentAddress("test address");
        await demoPage.clickFakeButton();
    });
});
               

```


### 指数退避
指数退避是一种重试策略，其中每次尝试之间的间隔呈指数递增。这种方法有助于减轻拥塞并减少对系统的负载。以下是一个示例实现：

```javascript
               
async function retryWithExponentialBackoff(actions, maxRetries, initialDelay) {
    let retryCount = 0;
    let delay = initialDelay;
                          
    while (retryCount < maxRetries) {
        try {
            await actions();
            return;
        } catch (error) {
            console.error("Error:", error);
        }
        await sleep(delay);
        delay *= 2;
        retryCount++;
    }
    throw new Error(
        "Retry limit exceeded: Actions did not complete successfully."
    );
}

               
it("Testing the retry with exponential backoff pattern", async () => {
    await demoPage.navigateToDemoPageTextBoxes();
    await browser.pause(1000);
    await retryWithExponentialBackoff(
        async () => {
            await demoPage.fillFullName("John Doe");
            await demoPage.fillEmail("test@gmail.com");
            await demoPage.fillCurrentAddress("test address");
            await demoPage.clickFakeButton();
        },
        4,
        1000
    );
});

```

其实这种方式也是设置一个最大的重试次数，不过因为增加了指数退让的关系，所以每次重试的间隔都会变长，避免短时间反复重试给被测系统造成巨大压力。

### 随机间隔重试

随机间隔为重试机制增加了随机因素，可以帮助避免执行中的同步问题和模式。其实就是每次重试等待的时间是是随机的。

```javascript
               
async function retryWithRandomizedInterval(
    actions,
    maxRetries,
    minDelay,
    maxDelay
) {
    let retryCount = 0;
                          
    while (retryCount < maxRetries) {
        try {
            await actions();
            return;
        } catch (error) {
            console.error("Error:", error);
        }
        const delay = Math.floor(
            Math.random() * (maxDelay - minDelay + 1) + minDelay
        );
        await sleep(delay);
        retryCount++;
    }
    throw new Error(
        "Retry limit exceeded: Actions did not complete successfully."
    );
}

               
it("Testing the retry with a randomized interval pattern", async () => {
    await demoPage.navigateToDemoPageTextBoxes();
    await browser.pause(1000);
    await retryWithRandomizedInterval(
        async () => {
            await demoPage.fillFullName("John Doe");
            await demoPage.fillEmail("test@gmail.com");
            await demoPage.fillCurrentAddress("test address");
            await demoPage.clickFakeButton();
        },
        3,
        1000,
        3000
    );
});

```

### 总结

记住下面几种重试模式

- 动态重试
- 异常重试
- 轮询重试
- 指数退避



