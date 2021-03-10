ls = ["Acceptance",
      "Curiosity",
      "Freedom",
      "Status",
      "Goal",
      "Honor",
      "Mastery",
      "Order",
      "Power",
      "Relatedness",
      ]

old = []
new_ls = []

for i in ls:
    old.append(i)
    for k in ls:
        if k not in old:
            new_ls.append([i, k])

for i in new_ls:
    print(i[0], ">>>", i[1])
