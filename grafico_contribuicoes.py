import matplotlib.pyplot as plt

# top contribuidores
nomes = ["Venkat6871", "tilakrayal", "gaikwadrahul8", "pkgoogle", "sushreebarsa"]
total = [103, 101, 26, 23, 21]


plt.bar(nomes, total , color=['blue', 'orange', 'green', 'red', 'purple'])
plt.title("Top 5 Contribuições")
plt.xlabel("username")
plt.ylabel("Quantidade")


plt.xticks(rotation=45)  
plt.tight_layout()  

plt.savefig("contribuidores.png", format='png')


plt.show()
