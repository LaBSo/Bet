def arb(sijoitus:int, n:list):
    N=0
    z = 0
    for kerroin in n:
        N += 1/kerroin
    if(1-N > 0):
        for kerroin in n:
            z+=1
            print("Laita "+str(z)+" kertoimelle "+str(round((sijoitus*(1/kerroin))/N,2))+ " eur")
    print("Voitto prosentti "+ str(round((1-N)*100,2))+ " %")

def replaceNull(x:list):
  for n in x:
    maxValue=0.0
    if n is not None:
        if n > maxValue:
            maxValue = n