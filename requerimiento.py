print("\nPROGRESO SEMANAL:")
for i in range(len(habitos)):
    h = habitos[i]
    nombre = h[0]
    frecuencia = h[1]
    registros = cumplimiento[i]

    if frecuencia == "diaria":
        if len(registros) > 0:
            promedio = sum(registros) / len(registros)
        else:
            promedio = 0
        print(f"{nombre}: {int(promedio)}% promedio diario")
    
    elif frecuencia == "semanal":
        if len(registros) > 0 and registros[-1] == 100:
            print(f"{nombre}: completado esta semana")
        else:
            print(f"{nombre}: pendiente esta semana")