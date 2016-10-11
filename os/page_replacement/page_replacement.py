# Simple implementations of some basic page replacement algorithms
# produced during a very boring lecture on operating systems

from sys import stdin, exit

s = stdin.read().split(" ")
if len(s) != 3:
    print("Incorrent amount of arguments")
    exit()

alg = s[0]
seq = map(int, list(s[1]))
num_of_pages = int(s[2])
page_faults = 0

if num_of_pages < 1:
    print("Page number must be at least 1")
    exit()


def error():
    global alg
    print(alg + " is not a valid algorithm")

def get_next_reference(page_number, start):
    global seq
    for i in range(start, len(seq)):
        if seq[i] == page_number:
            return i + 1
    return 1e9 

def optimal():
    global seq, page_faults
    pages = []
    next_reference = [1e9]*num_of_pages
    for i in range(0, len(seq)):
        for j in range(0, len(next_reference)):
            next_reference[j] -= 1
        page = seq[i]
        print("pages=" + str(pages))
        if len(pages) < num_of_pages:
            next_reference[len(pages)] = get_next_reference(page, i + 1)
            pages.append(page)
        else:
            if page in pages:
                next_reference[pages.index(page)] = get_next_reference(page, i + 1)
                continue
            to_be_replaced = next_reference.index(max(next_reference))
            next_reference[to_be_replaced] = get_next_reference(page, i + 1)
            pages[to_be_replaced] = page 
            page_faults += 1


def fifo():
    global seq, page_faults
    queue = []
    pages = []
    for i in range(0, len(seq)):
        page = seq[i]
        print("pages=" + str(pages))
        if len(pages) < num_of_pages:
            queue.insert(0, len(pages))
            pages.append(page)
        else:
            if page in pages:
                continue
            to_be_replaced = queue.pop()
            queue.insert(0, to_be_replaced)
            pages[to_be_replaced] = page
            page_faults += 1

def lru():
    global seq, page_faults
    least_recent = []
    pages = []
    for i in range(0, len(seq)):
        page = seq[i]
        print("pages=" + str(pages))
        if len(pages) < num_of_pages:
            least_recent.append(len(pages))
            pages.append(page)
        else:
            if page in pages:
                least_recent.remove(pages.index(page))
                least_recent.append(pages.index(page))
                continue
            pages[least_recent[0]] = page
            least_recent.append(least_recent.pop(0))
            page_faults += 1


{
        "FIFO": fifo,
        "LRU": lru,
        "OPT": optimal
        }.get(alg, error)()

print(str(page_faults) + " page faults occurred")





