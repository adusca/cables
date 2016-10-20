import csv
import re

with open('export.csv', 'rb') as entrada:
    with open('dados_processados.csv', 'wb') as saida:
        csvreader = csv.reader(entrada)
        csvwriter = csv.writer(saida)
        flag = True
        for linha in csvreader:
            # A primeira linha eh especial
            if flag:
                csvwriter.writerow(linha)
                flag = False
                continue
            destinos = linha[-1].split('|')
            for destino in destinos:
                # Removendo digitos de refid e destino
                nova_linha = linha[:3] + [re.sub("\d+", "", linha[3])] + [linha[4]] + [re.sub("\d+", "", destino)]
                if '' not in nova_linha:
                    csvwriter.writerow(nova_linha)
