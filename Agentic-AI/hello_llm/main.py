import os
from dotenv import load_dotenv
load_dotenv()

def main():
    #path = os.getenv("PATH")
    #print(path)

    abc = os.getenv("GOOGLE_API_KEY")
    print(abc)


if __name__ == "__main__":
    main()
