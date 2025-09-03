def function_name():
    hello = input("DO SOMETHING: ")
    print(hello)

    stop_condition = hello == "quit"

    if stop_condition:
        pass
    else:
        function_name()


function_name()
