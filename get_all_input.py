import os,sys
import random

if __name__ == '__main__':
    folder_list = [f for f in os.listdir('.') if not os.path.isfile(os.path.join('.', f)) and f[0] != "."]
    n_output = int(sys.argv[1]) if len(sys.argv)>1 else 1
    output = []
    for team in folder_list:
        with open(team+"/sample.txt") as f:
            for line in f:
                output.append(team+"\t"+line)
    for i in range(n_output):
        with open("CGW-grader"+str(i)+".txt","w+") as out_f:
            out_f.write("team\tsentence\tgrammaticality (0 - ungrammatical, 1 - a bit odd, 2 - grammatical)\n")
            random.shuffle(output)
            for line in output:
                out_f.write(line)