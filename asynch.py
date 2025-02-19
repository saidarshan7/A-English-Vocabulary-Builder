import multiprocessing

print(multiprocessing.cpu_count())

#In Python, a coroutine is a function that can pause and resume execution, allowing multiple tasks to run simultaneously. Coroutines are useful for tasks that might otherwise block the main thread, like reading files or fetching data from the web. 

#When are coroutines useful?
# Coroutines are particularly useful for tasks that involve waiting for external events, such as network or file I/O. 
# They are well-suited for implementing program components such as cooperative tasks, exceptions, event loops, iterators, infinite lists, and pipes

#await used to pause the coroutine