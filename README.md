
# IoWarp MCPs

##  Overview

This project implements a **Scientific Model Context Protocol (MCP) Server** using **FastAPI** and **JSON-RPC 2.0**. The server simulates various scientific computing capabilities and allows **AI agents** and **Large Language Models (LLMs)**  to interact with tools and data sources in a standardized way.


##  Implemented MCP Capabilities

The following nine capabilities have been implemented:

| Capability     | Type             | Description                                                               |
|----------------|------------------|---------------------------------------------------------------------------|
| `HDF5`         | Data             | Lists `.hdf5` files from a specified local directory                      |
| `Slurm`        | Tool             | Simulates Slurm-like job submission, returns a fake job ID.               |
| `Arxiv`        | Data             | Fetches 3 recent research papers via the Arxiv API using `httpx`.         |
| `Compression`  | Tool             | Simulates gzip compression using Python’s `gzip` module.                  |
| `Plot`         | Tool             | Uses `pandas` and `matplotlib` to generate a plot from a local CSV file.  |
| `Parquet`      | Data             | Reads the temperature column from a Parquet file using `pyarrow`.         |
| `Parallel_Sort`| Tool             | Simulates sorting a large text file and returned sorted result            |
| `Node_Hardware`| Tool             | Reports the number of CPU cores on the current system .                   |
| `Pandas`       | Data             | Loads data and displays rows based on condition using the `pandas` library|
| `Jarvis`       | Tool             | Initialize, configures, list, runs and destroys the pipeline. Add, link, unlink, delete, update packages to the pipeline. Built in llm client python file to test.|
| `Adios`        | Data             | Reads the data from different type of file engines and file types by adios2|
| `ChronoLog`    | External System  | Chronolog setup and client api tools to log and retrieve data             |

## Quick Installation

- Clone the repository:
    ```bash
   git clone https://github.com/iowarp/scientific-mcps.git
   cd scientific-mcps
   ```
- Install uv:
    ```bash
    pip install uv
    ```
- Create and activate environment using uv:
    ```bash
    uv venv mcp-server
    mcp-server\Scripts\activate     #On Windows
    source mcp-server/bin/activate  #On macOS/Linux
    ```
#### **To Install Individual MCP**
  - Each MCP directory contains it's own pyproject.toml file and hence can be built seperately. 
    ```bash
    cd <mcp-name> # Arxiv
    ```
    > Detailed instructions about installation of individual mcp can be found in their respective sub directory. 
#### **To Install All MCP altogther**
- Install dependencies using uv:
    ```bash
    # Install dependencies from pyproject.toml
    uv pip install --requirement pyproject.toml
    ```
<!-- - To install all mcps as package
    ```bash
    uv add "git+https://github.com/iowarp/scientific-mcps.git@main"
    # or 
    uv pip install "git+https://github.com/iowarp/scientific-mcps.git@main"
    ```
-->

## Running the Unified Client Interface Warp Chat
Put the name of the server you want to run - Adios, HDF5, Jarvis, etc.

```bash
python3 bin/wrp_chat.py --servers=Adios
```

## Project Structure

```
scientific-mcps/
├── HDF5
├── Arxiv
    ├── pyproject.toml
    ├── README.md
    ├── src/
    │   ├── server.py
    │   ├── mcp_handlers.py
    │   └── capabilities/
    │       ├── arxiv_handler.py
    ├── tests/
    │   ├── test__handlers.py
    │   └── test_capabilities.py
    └── .gitignore
├── Slurm
├── Compression
├── Plot
├── Parquet
├── Parallel_Sort
├── Node_Hardware
├── Pandas
├── Jarvis
├── Adios 
├── Chronolog
```

## Usage

To run any MCP, navigate into its directory and follow the instructions in its **README.md**. Each MCP provides concrete examples and expected inputs/outputs