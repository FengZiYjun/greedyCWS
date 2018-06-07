# -*- coding: UTF-8 -*-

"""
Compare two word segmented files with the same input characters but different word seg schemes,
return a label score

"""

#import logger
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("--f1")
parser.add_argument("--f2", default="predict_to_cmp")
parser.add_argument("--output", default="tmp")
args = parser.parse_args()
file1 = args.f1
file2 = args.f2
output = args.output


NUMS = "0123456789"


def build_labels(input_file):
    with open(input_file, "r", encoding="utf-8") as f:
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

    with open("tmp0", "w", encoding="utf-8") as f:
        f.write(string)

    with open("tmp0", "r", encoding="utf-8") as f:
        lines = f.readlines()
    return lines


lines1 = build_labels(file1)
lines2 = build_labels(file2)

# if len(lines1) != len(lines2):
#    print("length not equal")

length = min(len(lines1), len(lines2))
length1 = len(lines1)
length2 = len(lines2)


total = 0
correct = 0
i = 0
j = 0
truth = ""
pred = ""
diff = False

# logger = logger.Logger("./cmp_" + file1[:3] + "_" + file2[:3])
#logger = logger.Logger(output)
#log_text = ""

while i < length1 and j < length2:
    tokens1 = lines1[i]
    tokens2 = lines2[j]
    if len(tokens1) < 4 or len(tokens2) < 4:
        i += 1
        j += 1
        if diff:
            # log_text += ("truth" + truth + "\n")
            # log_text += ("pred " + pred + "\n\n")
            # print("truth: ", truth)
            # print("pred: ", pred)
            diff = False
        truth = ""
        pred = ""
        continue

    truth += tokens2[0]
    if tokens2[-4] == "E" or tokens2[-4] == "S":
        truth += " "
    pred += tokens1[0]
    if tokens1[-4] == "E" or tokens1[-4] == "S":
        pred += " "

    if tokens2[0] == tokens1[0]:  # the same character
        total += 1
        i += 1
        j += 1
        truth_tk = tokens2[-4]
        pred_tk = tokens1[-4]
        if truth_tk == pred_tk:
            correct += 1
        else:
            diff = True

    else:
        # print("error at line ", i, " and ", j, ": ", tokens2[0], " != ", tokens1[0])
        flag = False
        for k in range(1, 5):
            # print("test ", lines1[i+k][0], " and ", tokens2[0])
            if i + k >= length1:
                break
            if lines1[i + k][0] == tokens2[0]:
                i = i + k
                flag = True
                break
        if flag == False:
            for k in range(1, 5):
                if j + k >= length2:
                    break
                # print("test ", lines2[j+k][0], " and ", tokens1[0])
                if lines2[j + k][0] == tokens1[0]:
                    j = j + k
                    flag = True
                    break
        if flag == False:
            i += 1
            j += 1
            # total += 1
        # print("restart at line ", i, " and ", j, " ", lines1[i][0], " and ", lines2[j][0])

# print("length=", length)
# print("total=", total)
# print("correct=", correct)
print("Accuracy={}".format(correct / total))

#log_text += str(float(correct) / total)

#logger.log(log_text)