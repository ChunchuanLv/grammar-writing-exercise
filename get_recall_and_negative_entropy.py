import os,sys
import random

if __name__ == '__main__':
    folder_list = [f for f in os.listdir('.') if not os.path.isfile(os.path.join('.', f)) and f[0] != "."]
    grammatical_sentences = {}

    print("team\tRecall\tnegative entropy:")
    for team in folder_list:
        try:
            with open(team+"/parsed.txt") as f:
                total_sentences = 0
                parsed = 0
                entropy = 0
                for line in f:
                    if line.startswith("#-cross entropy (bits/word): "):
                        entropy = line[len("#-cross entropy (bits/word): "):]
                    elif line.startswith("#No parses found for"):
                        total_sentences += 1
                    else:
                        parsed += 1
                        total_sentences += 1
                if entropy == 0:
                    print (team, "\t","failed")
                else:
                    print (team, "\t", parsed/total_sentences,"\t", entropy)
        except:
                print (team, "\t","failed")
