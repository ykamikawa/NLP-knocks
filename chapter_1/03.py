# 円周率
target = "Now I need a drink, alcoholic of course, after the heavy lectures involving quantum mechanics."
target_list = target.split(" ")
target_list = [[c for c in word if c.isalpha()] for word in target_list]
count_list = [len(word) for word in target_list]
print(count_list)
