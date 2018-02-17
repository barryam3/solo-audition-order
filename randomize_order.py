import random

xprods = [
  "Michaye",
  "Alex",
  "Jessica",
  "Erica",
  "Helen",
  "Matthew",
  "John",
  "Dongho",
  "Yeye",
  "Craig",
  "Barry"
]

interest = {
    "You Will Be Found" : {
        "Solo 1" : [
            "Craig",
            "Barry",
            "Alex",
            "Matthew",
            "John",
            "Yeye",
            "Dongho",
            "Helen"
        ],
        "Solo 2" : [
            "Alex",
            "Matthew",
            "John",
            "Helen"
        ],
        "Perc" : [
            "Craig",
            "John",
            "Yeye"
        ]
    },
    "No Longer Slaves" : {
        "Solo 1" : [
            "Craig",
            "Alex",
            "Jessica",
            "Matthew",
            "Yeye",
            "John",
            "Michaye"
        ],
        "Solo 2" : [
            "Matthew",
            "Michaye",
            "Jessica",
            "Alex"
        ],
        "Perc" : [
            "Craig",
            "Jessica",
            "John"
        ]
    },
    "Beloved" : {
        "Solo" : [
            "Craig",
            "Matthew",
            "Yeye",
            "John",
            "Dongho",
            "Jessica"
        ],
        "Perc" : [
            "Craig",
            "Jessica",
            "Yeye",
            "John"
        ]
    }
}

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
        out.extend(shuffled(lis)[:max(len(lis), n-len(out))])
    return out

def assign_solos():
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

assign_solos()

