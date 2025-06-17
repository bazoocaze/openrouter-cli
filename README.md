# OpenRouter CLI

A simple, lightweight command-line interface for interacting with OpenRouter AI models directly from your terminal.

![OpenRouter CLI](https://img.shields.io/badge/OpenRouter-CLI-blue)
![Python 3.12](https://img.shields.io/badge/Python-3.12-green)
![License MIT](https://img.shields.io/badge/License-MIT-yellow)

## Overview

OpenRouter CLI provides a straightforward way to interact with various AI models through the [OpenRouter](https://openrouter.ai) API, giving you access to models from providers like Anthropic, Google, and others—all from your command line.

## Features

- **Simplified AI Access**: Chat with AI models using simple commands
- **Live Streaming**: Watch responses appear in real-time as they're generated
- **Model Selection**: Choose from any model available on OpenRouter
- **Reasoning Display**: See the model's thinking process before the final response
- **Shell Integration**: Includes Bash autocomplete for models and commands

## Installation

### Prerequisites

- Python 3.6+
- Pipenv
- OpenRouter API key (get one at [https://openrouter.ai](https://openrouter.ai))

### Quick Setup

1. Clone this repository
2. Install dependencies with `pipenv install`
3. Set your API key: `export OPENROUTER_API_KEY="your_api_key_here"`
4. Make the script executable: `chmod +x openrouter_cli.sh`
5. Optional: Create a symbolic link: `sudo ln -s $(pwd)/openrouter_cli.sh /usr/local/bin/openrouter_cli`
6. Optional: Enable autocomplete by adding to your shell profile:
   ```bash
   source /path/to/openrouter_autocomplete.sh
   ```

## Usage

### Basic Commands

```bash
# Chat with default model (qwen/qwen3-14b:free)
openrouter chat "What's the weather like on Mars?"

# Use a specific model
openrouter chat "Explain quantum computing in simple terms" --model anthropic/claude-3-haiku

# List all available models
openrouter list-models
```

### Chat Options

- `-m, --model MODEL`: Specify which model to use
- `--stream`: Enable streaming responses (default)
- `--no-stream`: Disable streaming responses
- `--no-reasoning`: Hide the model's reasoning section
- `--save`: Save conversation to local history

## Examples

```bash
# Generate a creative piece
openrouter chat "Write a haiku about programming"

# Hide the reasoning process
openrouter chat "Explain relativity simply" --no-reasoning

# Save conversation to history
openrouter chat "What are the best practices for API design?" --save
```

## About OpenRouter

OpenRouter provides a unified API to access various AI models from different providers. This CLI tool makes it easy to leverage those models directly from your terminal workflow.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
