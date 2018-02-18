import random
from argparse import ArgumentParser

parser = ArgumentParser(description="Randomize solo audition order.")
parser.add_argument("tsvfile", type=str, help="Path to TSV file.")
args = parser.parse_args()

def split_and_strip(string, sep):
    return [s.strip() for s in string.split(sep)]

interest = {}
with open(args.tsvfile) as f:
    songs = split_and_strip(f.readline(), "\t")[2:-1]
    for song in songs:
        interest[song] = {}
    for line in f.readlines():
        row = split_and_strip(line, "\t")
        person_name = row[1]
        for song, cell in zip(songs, row[2:-1]):
            solos = split_and_strip(cell, ",")
            for solo in solos:
                if solo == '':
                    continue
                if solo not in interest[song]:
                    interest[song][solo] = []
                interest[song][solo].append(person_name)

# returns true if l1[i] == l2[i] for any i
def match_one(l1, l2):
    for i in range(len(l1)):
        if l1[i] == l2[i]:
            return True
    return False

# mutates target list to be the same as source list
def copy_list(source, target):
    for i in range(len(source)):
        if i < len(target):
            target[i] = source[i]
        else:
            target.append(source[i])
    while i < len(target) - 1:
        target.pop()
        i += 1

# return a shuffled copy of a list
def shuffled(lis):
    cpy = lis[:]
    random.shuffle(cpy)
    return cpy

# takes n random elements from list (repeating once all are drawn)
def draw(lis, n):
    out = []
    while len(out) < n:
        out.extend(shuffled(lis)[:min(len(lis), n-len(out))])
    return out

def assign_solos(interest):
    for song, solos in interest.items():
        # sort solos by most interest
        data = list(solos.items())
        data.sort(key=lambda x: len(x[1]), reverse=True)
        # get number of runs needed
        num_runs = len(data[0][1])
        # randomize order for most popular solo
        random.shuffle(data[0][1])
        # randomize orders for all other solos, avoiding to at once
        for i in range(1, len(data)):
            # save original list of people who signed up
            orig_people = data[i][1][:]
            # make sure list does not overlap with any previous list
            j = 0
            while j < i:
                # randomize the list whenever we start over
                if j == 0: 
                    copy_list(draw(orig_people, num_runs), data[i][1])
                # see if there is any overlap
                if match_one(data[j][1], data[i][1]):
                    j = 0
                else:
                    j += 1
        # pretty-print the results
        solo_names = []
        for solo, order in data:
            solo_names.append(solo)
        print("{} ({})".format(song, " / ".join(solo_names)))
        for i in range(num_runs):
            people = []
            for solo, order in data:
                people.append(order[i])
            print(" / ".join(people))
        print("")

assign_solos(interest)

