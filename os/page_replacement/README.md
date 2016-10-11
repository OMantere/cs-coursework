Implementations of some simple page replacement algorithms produced during a very boring lecture on operating systems. Takes algorithm (OPT, FIFO, LRU), page sequence of page numbers 0-9 and max number of pages in memory concurrently. 

Usage: ```echo "<algorithm> <page sequence> <max pages in memory>" | python page_replacement.py```

For example: ```echo "OPT 12345353 3" | python page_replacement.py```
