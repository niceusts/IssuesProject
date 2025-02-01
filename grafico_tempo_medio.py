import matplotlib.pyplot as plt

# Tempo Médio
tempos = ['Dias', 'Horas', 'Minutos']
valores = [30, 9, 7] 


plt.bar(tempos, valores, color=['blue', 'orange', 'green'])


plt.title('Tempo Médio de Resolução de Issues')
plt.ylabel('Tempo')
plt.xlabel('Unidades de Tempo')

plt.savefig("tempo_medio.png", format='png')

plt.show()
