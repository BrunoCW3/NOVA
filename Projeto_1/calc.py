def calculator():
    while True:
        print("Calculadora Simples")
        print("1. Soma")
        print("2. Subtração")
        print("3. Multiplicação")
        print("4. Divisão")
        opcao = input("Escolha uma opção (1/2/3/4 ou 'sair'): ")

        if opcao == "1":
            num1 = float(input("Insira o primeiro número: "))
            num2 = float(input("Insira o segundo número: "))
            print(f"Resultado: {num1 + num2}")
        elif opcao == "2":
            num1 = float(input("Insira o primeiro número: "))
            num2 = float(input("Insira o segundo número: "))
            print(f"Resultado: {num1 - num2}")
        elif opcao == "3":
            num1 = float(input("Insira o primeiro número: "))
            num2 = float(input("Insira o segundo número: "))
            print(f"Resultado: {num1 * num2}")
        elif opcao == "4":
            num1 = float(input("Insira o primeiro número: "))
            num2 = float(input("Insira o segundo número: "))
            if num2 != 0:
                print(f"Resultado: {num1 / num2}")
            else:
                print("Erro! Não é possível dividir por zero!")
        elif opcao.lower() == "sair":
            break
        else:
            print("Opção inválida. Tente novamente!")

calculator()