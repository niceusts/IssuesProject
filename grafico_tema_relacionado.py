import matplotlib.pyplot as plt

# Temas Relacionados
testes = ['"Testes de Regressão"', '"Refatoração,Testes de Regressão"']
total = [242, 58]


plt.figure(figsize=(8, 6))
plt.pie(total, labels=testes, autopct='%1.1f%%', startangle=90, colors=['lightblue', 'lightgreen'])
plt.title("Quantidade de Temas Relacionados")
plt.savefig("tema_relacionado.png", format='png')
plt.show()
