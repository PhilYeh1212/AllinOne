import asyncio

async def task1():
    print("Task 1 started")
    await asyncio.sleep(2)
    print("Task 1 completed")

async def task2():
    print("Task 2 started")
    await asyncio.sleep(1)
    print("Task 2 completed")

async def main():
    # 使用 asyncio.gather 并发执行多个任务
    await asyncio.gather(task1(), task2())

# 运行异步程序
asyncio.run(main())