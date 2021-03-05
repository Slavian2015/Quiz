ls = ["Freedom",
"Mastery",
"Power",""
"Goal",
"Curiosity",
"Honor",
"Acceptance",
"Relatedness",
"Order",
"Status",
]


old = []
new_ls = []

for i in ls:
    old.append(i)
    for k in ls:
        if k not in old:
            new_ls.append([i,k])

for i in new_ls:
    print(i[0], ">>>", i[1])

