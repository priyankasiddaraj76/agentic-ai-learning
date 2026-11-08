import asyncio
import time


async def task(name: str) -> None:
    print(f"Starting {name}")
    await asyncio.sleep(2)
    print(f"Finished {name}")

async def main():
    start = time.time()

    await asyncio.gather(
        task("Task 1"),
        task("Task 2"),
        task("Task 3")
    )
    print(f"Total time: {time.time() - start:.2f} seconds")

asyncio.run(main())