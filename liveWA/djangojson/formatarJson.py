import json

# Caminho para o arquivo JSON
file_path = "C:\\Users\\JEAN\\Documents\\Lista 4\\estacoes_microparticula.json"

try:
    # Abra o arquivo JSON para leitura
    with open(file_path, "r") as file:
        # Leia as linhas do arquivo
        lines = file.readlines()

    # Abra o arquivo JSON para escrita
    with open(file_path, "w") as file:
        file.write("[\n")  # Adicione o colchete de abertura no início do arquivo
        for i, line in enumerate(lines):
            try:
                json_data = json.loads(line)
                formatted_json = json.dumps(json_data, indent=4)
                file.write(formatted_json)  # Salve o objeto JSON formatado
                if i < len(lines) - 1:
                    file.write(",")  # Adicione uma vírgula se não for o último objeto
                file.write("\n")  # Adicione uma nova linha após cada objeto
            except json.JSONDecodeError as e:
                print(f"Ocorreu um erro ao analisar o JSON na linha {i + 1}: {e}")

        file.write("]\n")  # Adicione o colchete de fechamento no final do arquivo

except FileNotFoundError:
    print("O arquivo JSON não foi encontrado.")
except Exception as e:
    print(f"Ocorreu um erro: {e}")
