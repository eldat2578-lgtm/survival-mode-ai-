from datetime import datetime

def main():
    today = datetime.now().strftime("%Y-%m-%d")

    print("================================")
    print("       SURVIVAL MODE")
    print("================================")
    print(f"Date: {today}")
    print("Automation system started!")
    print("Next step: topic generation.")

if __name__ == "__main__":
    main()