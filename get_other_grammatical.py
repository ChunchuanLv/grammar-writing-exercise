import os
if __name__ == '__main__':
    folder_list = [f for f in os.listdir('.') if not os.path.isfile(os.path.join('.', f)) and f[0] != "."]

    with open("all_sentences.txt","w+") as out_f:
        out_f.write("team\tsentence\tgrammaticality (0 - ungrammatical, 1 - a bit odd, 2 - grammatical)\n")
        for team in folder_list:
            with open(team+"/sample.txt") as f:
                for line in f:
                    out_f.write(team+"\t"+line)