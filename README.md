# IoWarp MCPs

## Overview

This project implements a **Scientific Model Context Protocol (MCP) Server** using **FastAPI** and **JSON-RPC 2.0**. The server simulates various scientific computing capabilities and allows **AI agents** and **Large Language Models (LLMs)** to interact with tools and data sources in a standardized way.

## Implemented MCP Capabilities

The following capabilities have been implemented:

| Capability | Type | Description |
|---|---|---|
| `Adios` | Data | Reads data from different file types using the ADIOS2 engine. |
| `Arxiv` | Data | Fetches recent research papers from the Arxiv API. |
| `ChronoLog` | External System | Provides tools to log and retrieve data from a ChronoLog server. |
| `Compression` | Tool | Simulates file compression using Python's `gzip` module. |
| `HDF5` | Data | Lists `.hdf5` files from a specified local directory. |
| `Jarvis` | Tool | Manages the full lifecycle of data-centric pipelines. |
| `Node_Hardware` | Tool | Reports the number of CPU cores on the current system. |
| `Pandas` | Data | Loads and filters data from a CSV file using the `pandas` library. |
| `Parallel_Sort`| Tool | Simulates sorting a large text file and returns the sorted result. |
| `Parquet` | Data | Reads a specific column from a Parquet file using `pyarrow`. |
| `Plot` | Tool | Generates a plot from a local CSV file using `pandas` and `matplotlib`. |
| `Slurm` | Tool | Simulates Slurm-like job submission and returns a fake job ID. |

---

## Prerequisites
- Python 3.10 or higher (https://www.python.org/)
- [uv](https://docs.astral.sh/uv/) package manager
- Linux/macOS environment (for optimal compatibility)


## Installation

The Scientific Mcps supports three installation methods:

1. Global Installation of all mcps together -

- Clone the repository:
    ```bash
   git clone https://github.com/iowarp/scientific-mcps.git
   cd scientific-mcps
   ```
- Create and activate environment:
    ```bash
    # On Windows
    python -m venv mcp-server
    mcp-server\Scripts\activate 

    #On macOS/Linux
    python3 -m venv mcp-server
    source mcp-server/bin/activate  #On macOS/Linux
    ```
- Install uv:
    ```bash
    pip install uv
    ```

You can install all MCPs at once or select them individually.

---

**To install all MCPs:**
```bash
# This installs all dependencies listed in the pyproject.toml
uv pip install --requirement pyproject.toml
```

**To install individual or multiple MCPs:**

| MCP | Installation Code (`uv pip install ...`) | Documentation |
|---|---|---|
| `Adios` | `"git+https://github.com/iowarp/scientific-mcps.git@main#subdirectory=Adios"` | [docs](./Adios/README.md) |
| `Arxiv` | `"git+https://github.com/iowarp/scientific-mcps.git@main#subdirectory=Arxiv"` | [docs](./Arxiv/README.md) |
| `ChronoLog` | `"git+https://github.com/iowarp/scientific-mcps.git@main#subdirectory=Chronolog"` | [docs](./Chronolog/README.md) |
| `Compression` | `"git+https://github.com/iowarp/scientific-mcps.git@main#subdirectory=Compression"` | [docs](./Compression/README.md) |
| `HDF5` | `"git+https://github.com/iowarp/scientific-mcps.git@main#subdirectory=HDF5"` | [docs](./HDF5/README.md) |
| `Jarvis` | `"git+https://github.com/iowarp/scientific-mcps.git@main#subdirectory=Jarvis"` | [docs](./Jarvis/README.md) |
| `Node_Hardware` | `"git+https://github.com/iowarp/scientific-mcps.git@main#subdirectory=Node_Hardware"` | [docs](./Node_Hardware/README.md) |
| `Pandas` | `"git+https://github.com/iowarp/scientific-mcps.git@main#subdirectory=Pandas"` | [docs](./Pandas/README.md) |
| `Parallel_Sort` | `"git+https://github.com/iowarp/scientific-mcps.git@main#subdirectory=Parallel_Sort"`| [docs](./Parallel_Sort/README.md) |
| `Parquet` | `"git+https://github.com/iowarp/scientific-mcps.git@main#subdirectory=parquet"` | [docs](./parquet/README.md) |
| `Plot` | `"git+https://github.com/iowarp/scientific-mcps.git@main#subdirectory=Plot"` | [docs](./Plot/README.md) |
| `Slurm` | `"git+https://github.com/iowarp/scientific-mcps.git@main#subdirectory=Slurm"` | [docs](./Slurm/README.md) |

> **Tip**: You can install multiple MCPs in a single command by listing them one after another (e.g., `uv pip install "adios-mcp..." "arxiv-mcp..."`).

---

## Running the Server with different types of Clients:


### Running the Universal Client (`wrp_chat`)

This repository includes a universal client, `bin/wrp.py`, that allows you to interact with any MCP server using natural language. It supports multiple LLM providers (Gemini, OpenAI, Claude, Ollama).

> For detailed setup instructions, provider-specific examples, and troubleshooting, please see the **[in-depth instructions](./bin/docs/instructions.md)**.

For a quick Gemini setup -

1.  **Install Client Dependencies:**
    ```bash
    # From the root directory
    uv pip install -r bin/requirements.txt
    ```
2.  **Configure API Keys:**
    Your API keys for providers like Gemini, OpenAI, or Anthropic are managed in the configuration files.

    For long-term use, open the relevant pre-configured file in `bin/confs` (e.g., `Gemini.yaml`) and enter your key directly:
    ```yaml
    # In bin/confs/Gemini.yaml
    LLM:
    Provider: Gemini
    api_key: your-gemini-api-key # <-- ADD KEY HERE
    model_name: gemini-1.5-flash
    ```

    For one-time use, you can use environment variables. First, export the key in your terminal:
    ```bash
    # On macOS/Linux
    export GEMINI_API_KEY="your-gemini-api-key"
    # On Windows
    $env:GEMINI_API_KEY="your-gemini-api-key"

3.  **Run the Client:**
    To run the client, execute the `wrp` script from your terminal, specifying a configuration file with the `--conf` flag.

    **Example for Gemini:**
    ```bash
    python bin/wrp.py --conf=bin/confs/Gemini.yaml
    ```

4. **For Additional Troubleshooting & Debugging use verbose:**
```bash
python bin/wrp.py --conf=bin/confs/Gemini.yaml --verbose
```

2. Running a specific Mcp directly.
**Run the Mcp Server directly:**

   ```bash
   cd Adios     # Jarvis or any other specific mcp.
   uv run adios-mcp     # change the mcp name ex. jarvis-mcp   
   ```
   
   This will create a `.venv/` folder, install all required packages, and run the server directly.
--- 

### Running the Server on Claude Command Line Interface Tool.

1. Install the Claude Code using NPM,
Install [NodeJS 18+](https://nodejs.org/en/download), then run:

```bash
npm install -g @anthropic-ai/claude-code
```

2. Running the server:
```bash
claude add mcp jarvis -- uv --directory ~/scientific-mcps/Jarvis run jarvis-mcp
```

### Running the Server on open source LLM client (Claude, Copilot, etc.)

**To add the Adios MCP**
**Put the following in settings.json of any open source LLMs like Claude or Microsoft Co-pilot:**

```bash
"adios-mcp": {
    "command": "uv",
    "args": [
        "--directory",
        "path/to/directory/src/adiosmcp/",
        "run",
        "server.py"
    ]
}
```

---
## Project Structure

```
scientific-mcps/
├── Adios/
├── Arxiv/
├── Chronolog/
├── Compression/
├── HDF5/
├── Jarvis/
├── Node_Hardware/
├── Pandas/
├── Parallel_Sort/
├── parquet/
├── Plot/
├── Slurm/
├── bin/
│   ├── wrp.py
│   ├── README.md
│   ├── instructions.md
│   └── ...
└── ...
```

## Usage

To run any MCP server directly or learn more about its specific capabilities, navigate into its directory and follow the instructions in its local `README.md`.