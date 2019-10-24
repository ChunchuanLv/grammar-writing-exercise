import os,sys
import random

if __name__ == '__main__':
    folder_list = [f for f in os.listdir('.') if not os.path.isfile(os.path.join('.', f)) and f[0] != "."]
    n_output = int(sys.argv[1]) if len(sys.argv)>1 else 1
    grammatical_sentences = {}
    for i in range(n_output):
        with open("CGW-grader"+str(i)+".txt") as graded_f:
            next(graded_f)
            for line in graded_f:
                team, snt , grammaticality = line.split("\t")
                grammaticality = int(grammaticality)
                grammatical_sentences.setdefault((team,snt),0)
                grammatical_sentences[(team,snt)] += grammaticality

    for team in folder_list:
        with open(team+"/other.txt","w+") as f:
            total_sentences = 0
            total_grammaticality = 0
            for snt_team,snt in grammatical_sentences:
                grammaticality = grammatical_sentences[(team,snt)]
                if snt_team!=team and grammaticality >=3:
                    f.write(snt)
                else:
                    total_sentences += 2*n_output
                    total_grammaticality += grammaticality


            print ("team",team, "Precision:", total_grammaticality/total_sentences)
