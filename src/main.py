import argparse
import os
from dotenv import load_dotenv


def load_environment():
    load_dotenv()
    return {
        "api_key": os.getenv("API_KEY")
    }


def run_demo(env):
    print("🚀 AI Project Template running successfully")

    if env["api_key"]:
        print("✅ API Key loaded")
    else:
        print("⚠️ API Key not found. Add it in .env file")


def main():
    parser = argparse.ArgumentParser(description="AI Project Template")
    parser.add_argument("--mode", type=str, default="demo", help="Execution mode")

    args = parser.parse_args()

    env = load_environment()

    if args.mode == "demo":
        run_demo(env)
    else:
        print(f"Unknown mode: {args.mode}")


if __name__ == "__main__":
    main()