
import time

def task(name: str) -> None:
    print(f"Starting {name}")
    time.sleep(2)
    print(f"Finished {name}")

def main():
    start = time.time()

    task("Task 1")
    task("Task 2")
    task("Task 3")

    print(f"Total time: {time.time() - start:.2f} seconds")

main()
