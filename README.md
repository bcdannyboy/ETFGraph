# ETFGraph

ETFGraph is a comprehensive analytics tool for creating and analyzing an attributed graph of exchange traded funds (ETFs) and their underlying assets. It utilizes financial data to aid investors, analysts, and researchers in exploring complex relationships between ETFs and their components, identifying influential stocks, and understanding market dynamics through community structures and centrality metrics.

## Features

- **Data Pull and Graph Generation**: Automatically retrieves data on ETFs and their holdings from the Financial Modeling Prep API, constructing a graph representation.
- **Graph Visualization**: Provides visual representation of the ETF graph to facilitate understanding of connections and clusters.
- **Community Detection and Clustering**: Employs algorithms like the Louvain method to detect communities, identifying potential market segments.
- **Centrality and PageRank Analysis**: Computes centrality measures and PageRank to spotlight influential stocks within ETFs.
- **Link Analysis**: Investigates relationships between ETFs and stocks based on attributes such as weight and multiple ETF inclusions.
- **Detailed Community Analysis**: Focuses on the largest communities to pinpoint the top stocks based on their connectivity weights.
- **Graph Serialization**: Offers capabilities to save the graph to a file for subsequent analysis or transfer using serialization formats like pickle.

## Requirements

ETFGraph requires a Financial Modeling Prep API key to access financial data for ETFs and their underlying assets. Obtain your API key by signing up for a free account at [Financial Modeling Prep](https://financialmodelingprep.com/).

### Environment Setup

Before running ETFGraph, ensure you have a `.env` file in the root directory of the project with the following content:

```plaintext
FMPKey=your_financial_modeling_prep_api_key_here
```

### Installation

To set up ETFGraph, clone the repository and install the required Python packages:

```bash
git clone https://github.com/bcdannyboy/ETFGraph/
cd ETFGraph
python3 -m pip install -r requirements.txt
```

### Usage

#### Basic Usage

To run the tool and perform a basic analysis on all ETFs available in the Financial Modeling Prep API, execute the following command:

```bash
python3 main.py
```

#### Advanced Usage

Advanced Usage
You can specify various options through command-line arguments:

- `-n, --num <int>`: Specify the number of ETFs to analyze.
- `-d, --display`: Enable graph visualization.
- `-r, --rate_limit <int>`: Set the API request rate limit (default 150/minute).
- `-o, --output <path>`: Save the results of the analysis to a JSON file.
- `-g, --save_graph <path>`: Save the graph object for later use or analysis in pickle format.
- `-l --load_graph <path>`: Load a saved graph object from a pickle file.

#### Examples:

To analyze 50 ETFs, display the graph, set the rate limit to 200 requests per minute, and save the results to a JSON file and graph object, use the following command:
```bash
python main.py -n 50 -d -r 200 -o output.json -g graph.pkl
```

To load a saved graph object and analyze the data without fetching new information, run:
```bash
python main.py -l graph.pkl
```

To analyze 100 ETFs at the default rate limit with only console output, execute:
```bash
python main.py -n 100
```

### Roadmap

- [X] Pull Data & Generate Graph
- [X] Graph Visualization
- [X] Basic Community Detection / Clustering
- [X] Basic Centrality Analysis
- [X] PageRank Analysis
- [X] Basic Link Analysis
- [ ] Better Data Visualization
- [ ] Overlapping community detection
- [ ] Better leveraged / inverse indication
- [ ] Better bull / bear indication
- [ ] Deep community analysis
- [ ] Graph structure sparcification
- [ ] Price simulation / price calculation as part of graph weights

### Contribute

Contributers welcome