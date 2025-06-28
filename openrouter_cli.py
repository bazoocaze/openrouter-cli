import argparse
import json
import os
import sys

import requests


# ========= Config =========

def get_api_key():
    return os.getenv("OPENROUTER_API_KEY")


HEADERS = {
    "Authorization": f"Bearer {get_api_key()}",
    "Content-Type": "application/json",
    "HTTP-Referer": "https://github.com/bazoocaze/openrouter-cli",
    "X-Title": "OpenRouter CLI"
}

API_URL = "https://openrouter.ai/api/v1/chat/completions"
HISTORY_FILE = "history.jsonl"


# ========= API Calls =========

def send_chat(model, messages, stream=False):
    payload = {
        "model": model,
        "messages": messages,
        "stream": stream
    }
    response = requests.post(API_URL, json=payload, headers=HEADERS, stream=stream)
    response.raise_for_status()
    return response


def list_models():
    url = "https://openrouter.ai/api/v1/models"
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    return r.json().get("data", [])


# ========= Util =========

def print_stream(response, hide_reasoning=False):
    thinking = False
    content = ""
    reasoning = ""
    for line in response.iter_lines():
        if line:
            try:
                data = json.loads(line.decode("utf-8").removeprefix("data: "))
                delta = data.get("choices", [{}])[0].get("delta", {})

                if not hide_reasoning and delta.get("reasoning"):
                    if not thinking:
                        sys.stdout.write("<think>")
                        thinking = True
                    sys.stdout.write(delta["reasoning"])
                    sys.stdout.flush()
                    reasoning += delta["reasoning"]

                if len(delta.get("content", "")) > 0:
                    if thinking:
                        sys.stdout.write("</think>\n\n")
                        thinking = False
                    sys.stdout.write(delta["content"])
                    sys.stdout.flush()
                    content += delta["content"]
            except Exception:
                continue
    if thinking:
        sys.stdout.write("</think>")
    sys.stdout.write("\n")
    return content.strip(), reasoning.strip()


def save_to_history(messages):
    try:
        print(f"Appending history to file {HISTORY_FILE}")
        with open(HISTORY_FILE, "a") as f:
            f.write(json.dumps(messages) + "\n")
    except Exception:
        pass


# ========= CLI Logic =========

def run_chat(args):
    if args.prompt is None:
        args.prompt = sys.stdin.read().strip()

    messages = [{"role": "user", "content": args.prompt}]
    response = send_chat(args.model, messages, args.stream)

    if args.stream:
        content, reasoning = print_stream(response, hide_reasoning=args.no_reasoning)

    else:
        data = response.json()
        msg = data["choices"][0]["message"]
        content = msg.get("content", "")
        reasoning = msg.get("reasoning", "")

        if not args.no_reasoning and reasoning:
            print("<think>")
            print(reasoning.strip())
            print("</think>\n\n")

        print(content.strip())

    if args.save:
        messages.append({"role": "assistant", "content": content, "reasoning": reasoning})
        save_to_history(messages)

    return 0


def run_list(args):
    models = list_models()
    for m in models:
        print(f"{m['id']:50} {m.get('description', '')}")
    return 0


def run_list_json(args):
    models = list_models()
    json.dump(models, sys.stdout)
    print()  # Add a newline at the end
    return 0


def run_list_ids(args):
    models = list_models()
    for m in models:
        print(m["id"])
    return 0


def main():
    parser = argparse.ArgumentParser(description="OpenRouter CLI")
    subparsers = parser.add_subparsers()

    # chat
    chat_parser = subparsers.add_parser("chat", help="Send a message to the model")
    chat_parser.add_argument("prompt", nargs='?', help="User message")
    chat_parser.add_argument("-m", "--model", default="qwen/qwen3-14b:free",
                             help="Model to use (default qwen/qwen3-14b:free)")
    chat_parser.add_argument("--stream", dest="stream", action="store_true", help="Use stream (default)")
    chat_parser.add_argument("--no-stream", dest="stream", action="store_false", help="Disable stream")
    chat_parser.set_defaults(stream=True)
    chat_parser.add_argument("--no-reasoning", action="store_true", help="Do not show reasoning part")
    chat_parser.add_argument("--save", action="store_true", help=f"Save/append local history ({HISTORY_FILE})")
    chat_parser.set_defaults(func=run_chat)

    # list-models
    list_parser = subparsers.add_parser("list-models", help="List available models")
    list_parser.set_defaults(func=run_list)

    # list-models-json
    list_json_parser = subparsers.add_parser("list-models-json", help="List available models in JSON format")
    list_json_parser.set_defaults(func=run_list_json)

    # list-models-ids
    list_ids_parser = subparsers.add_parser("list-models-ids", help="List only the IDs of available models")
    list_ids_parser.set_defaults(func=run_list_ids)

    args = parser.parse_args()
    if hasattr(args, "func"):
        try:
            return args.func(args)
        except KeyboardInterrupt:
            print("\nInterrupted")
            return 1
        except Exception as e:
            print(f"Error while executing command: {e}")
            return 1
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
