import os
from dotenv import load_dotenv
from api import SpaceTradersError, SpaceTradersClient, CooldownError, TokenInvalidError

load_dotenv()
TOKEN = os.getenv("SPACETRADERS_TOKEN")

if not TOKEN:
    print("Token not found in .env file")
    exit()

client = SpaceTradersClient(TOKEN)

def main():
    agent_data = client._request("GET", "/my/agent")
    if agent_data:
        data = agent_data.get('data', {})
        print(f"Logged in as: {data.get('symbol')}")
        print(f"Credits: {data.get('credits')}")
        print(f"Headquarters: {data.get('headquarters')}")

if __name__ == "__main__":
    main()