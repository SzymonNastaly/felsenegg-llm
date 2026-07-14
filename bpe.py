import re

class BPETokenizer:
    def __init__(self):
        self.stoi = {}
        self.itos = {}
        self.merges = {}

    def train(self, text, target_vocab_size):
        vocab = BPETokenizer._list_of_unique_characters(text) # not updated anymore, only initial
        self.stoi = {token: integer_id for integer_id, token in enumerate(vocab)}
        self.itos = {integer_id: token for integer_id, token in enumerate(vocab)}
        number_merges_needed = target_vocab_size - len(vocab)
        # token_ids = [self.stoi[char] for char in text]

        pattern1 = r"['’‘]s|['’‘]t|['’‘]re|['’‘]re|['’‘]ve|['’‘]m|['’‘]ll|['’‘]d | ?[^\W\d_]+| ?\d+| ?[^\w\s\d]+"
        preprocessed_text = re.findall(pattern1, text)
        token_ids = [([self.stoi[char] for char in chunk]) for chunk in preprocessed_text]

        for i in range(number_merges_needed):
            pair_counts = {}
            for chunk in token_ids:
                for i_chunk in range(len(chunk)-1):
                    pair = (chunk[i_chunk],chunk[i_chunk+1])
                    if not pair in pair_counts:
                        pair_counts[pair] = 1
                    else:
                        pair_counts[pair] += 1
            if not pair_counts:
                break
            best_pair = max(pair_counts, key=pair_counts.get)
            new_token_id = len(self.stoi)
            self.stoi[f"{self.itos[best_pair[0]]}{self.itos[best_pair[1]]}"] = new_token_id
            self.itos[new_token_id] = f"{self.itos[best_pair[0]]}{self.itos[best_pair[1]]}"
            self.merges[best_pair] = new_token_id
        
            new_token_ids = []
            for chunk in token_ids:
                j=0
                new_chunk = []
                while j < len(chunk):
                    if j < len(chunk)-1 and (chunk[j],chunk[j+1]) == best_pair:
                        new_chunk.append(new_token_id)
                        j+=2
                    else:
                        new_chunk.append(chunk[j])
                        j+=1
                new_token_ids.append(new_chunk)
            token_ids = new_token_ids

        special_tokens = ["<|eos|>"]
        for st in special_tokens:
            new_id = len(self.stoi)
            self.stoi[st] = new_id
            self.itos[new_id] = st

    def encode(self, text):
        pass

    def decode(self, token_ids):
        pass

    def _list_of_unique_characters(text):
        res = set()
        for c in text:
            res.add(c)
        return sorted(list(res))