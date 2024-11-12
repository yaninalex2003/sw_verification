from collections import deque, defaultdict
import csv

class AhoCorasick:
    def __init__(self, patterns, mcdc_file_name):
        self.mcdc_file_name = mcdc_file_name

        self.trie = {}
        self.out = defaultdict(list)
        self.fail = {}
        self.build_trie(patterns)
        self.build_failure_links()
    
    # MC/DC
    def print_mcdc(self, data: list[bool]):
        with open(self.mcdc_file_name, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(data)
        
    def build_trie(self, patterns):
        self.trie = {}
        self.trie[0] = {}
        new_state = 0
        for p in patterns:
            current_state = 0
            for symbol in p:
                if symbol not in self.trie[current_state]:
                    new_state += 1
                    self.trie[current_state][symbol] = new_state
                    self.trie[new_state] = {}
                current_state = self.trie[current_state][symbol]
            self.out[current_state].append(p)
    
    def build_failure_links(self):
        self.fail = {}
        queue = deque()

        for symbol in self.trie[0]:
            state = self.trie[0][symbol]
            self.fail[state] = 0
            queue.append(state)
        
        while queue:
            r = queue.popleft()
            
            for symbol in self.trie[r]:
                s = self.trie[r][symbol]
                queue.append(s)
                
                state = self.fail[r]

                while state != 0 and symbol not in self.trie[state]:
                    state = self.fail[state]
                
                if symbol in self.trie[state]:
                    self.fail[s] = self.trie[state][symbol]
                else:
                    self.fail[s] = 0
                
                self.out[s].extend(self.out[self.fail[s]])
    
    def search(self, text):
        state = 0
        results = []
        
        for i, symbol in enumerate(text):
            condition_values = [] # MC/DC

            condition_values.append(bool(state != 0)) # MC/DC
            condition_values.append(bool(symbol not in self.trie[state])) # MC/DC
            while state != 0 and symbol not in self.trie[state]:
                state = self.fail[state]

            condition_values.append(bool(symbol in self.trie[state])) # MC/DC
            if symbol in self.trie[state]:
                state = self.trie[state][symbol]
            else:
                state = 0

            condition_values.append(bool(self.out[state])) # MC/DC
            if self.out[state]:
                for pattern in self.out[state]:
                    results.append((i - len(pattern) + 1, pattern))

            self.print_mcdc(condition_values) # MC/DC
        
        return results
