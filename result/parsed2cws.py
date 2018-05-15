"""
from parsed text to CWS input

"""
file = "test_gold"

NUMS = "0123456789"

with open(file, "r", encoding="utf-8") as f:
    lines = f.readlines()

string = ""
for line in lines:
    for tokens in line[:-1].split():
        if tokens[0] in NUMS:
            string += (tokens + '#<NUM>#S_N\n')
            continue

        if len(tokens) == 1:
            string += (tokens[0] + '#' + tokens[0] + '#S_N\n')
        else:
            string += (tokens[0] + '#' + tokens[0] + '#B_N\n')
            for idx in range(1, len(tokens)-1):
                string += (tokens[idx] + '#' + tokens[idx] + '#M_N\n')
            string += (tokens[len(tokens)-1] + '#' + tokens[len(tokens)-1] + '#E_N\n')
    string += "\n"


with open(file + "_to_input", "w", encoding="utf-8") as f:
    f.write(string)