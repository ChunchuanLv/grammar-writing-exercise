import os,sys
import random

if __name__ == '__main__':
    folder_list = [f for f in os.listdir('.') if not os.path.isfile(os.path.join('.', f)) and f[0] != "."]
    grammatical_sentences = {}
    for i in range(n_output):
        with open("CGW-grader"+str(i)+".txt","w+") as graded_f:
            next(graded_f)
            for line in graded_f:
                team, snt , grammaticality = line.split("\t")
                grammaticality = int(grammaticality)
                grammatical_sentences.setdefault((team,snt),0)
                grammatical_sentences[(team,snt)] += grammaticality

    for team in folder_list:
        with open(team+"/parsed.txt") as f:
            total_sentences = 0
            parsed = 0
            entropy = 0
            for line in graded_f:
                if line.startswith("#-cross entropy (bits/word): "):
                    entropy = line[len("#-cross entropy (bits/word): "):]
                elif line.startswith("#No parses found for"):
                    total_sentences += 1
                else:
                    parsed += 1
            print ("team",team, "Recall:", parsed/total_sentences,"negative entropy:", entropy)
