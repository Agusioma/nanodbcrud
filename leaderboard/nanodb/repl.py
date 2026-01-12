from parser import parse
from engine import Engine

def repl():
    engine = Engine()
    print("The Database is ready for use!\nType SQL commands or type 'exit' to return to close.\n\n----------------------------------------------")

    while True:
        sql = input("$nanoDB> ")
        if sql.lower() == "exit":
            print("\nBYE!\n----------------------------------------------")
            break

        try:
            parsed_input = parse(sql)
            result = engine.execute(parsed_input)
            print(result)
        except Exception as e:
            print("Error:", e)


if __name__ == "__main__":
    repl()