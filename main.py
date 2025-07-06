from aiFanNEW.agent.agent import mainAgent

import os
from dotenv import load_dotenv

def main():
    print("Hello from aifannew!")
    print("__________________________")

    agent = mainAgent()
    while True:
        user_input = str(input(":"))
        if user_input == "quit":
            break
        agent.run(user_input)
        print("")

if __name__ == "__main__":
    main()
