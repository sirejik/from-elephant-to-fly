# From elephant to fly
This tool is the solution for the game "from elephant to fly". The goal of this game: create a chain of words each of 
which is obtained from the previous one by replacing one letter. The chain must be started and finished by specified 
words. All words in the chain must exist in the dictionary. Also, the chain should have a minimal chain link.

## Run project.
To run this tool, need to execute the command with the following format:
```
python main.py --from-word муха --to-word слон
```

## Algorithm
From the beginning, the tool validates entered words: its length should be equal to the specified length (in this 
realization - 4 letters). After this, the graph will be created by the dictionary where a node is a word from the 
dictionary. Two words are connected by an edge if one word can be obtained from another by one letter changing. For the 
searching chain with the minimal chain-link numbers used the Dijkstra algorithm.
