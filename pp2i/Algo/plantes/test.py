liste=[0,1]
tmp=liste.copy()
for i in range(3):
    liste.extend(tmp)
liste.remove(1)
print(liste)