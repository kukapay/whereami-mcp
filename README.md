# WhereAmI MCP Server

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)

A lightweight mcp server that tells you exactly where you are based on your current IP, powered by [ipapi.co](https://ipapi.co/). 

## Features

- **Dynamic Resources**: Fetch specific data (e.g., IP, country, city) via `location://{type}`.
- **Detailed Tool**: Generate a comprehensive location report with `get_location()`.
- **Natural Language Prompt**: Ask "Where am I?" to get detailed results.
- **Robust Error Handling**: Gracefully manages API and network issues.
- **Minimal Dependencies**: Requires only `mcp` and `httpx`.

## Installation

### Prerequisites
- Python 3.10+
- `pip`

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/kukapay/whereami-mcp.git
   cd whereami-mcp
   ```
2. Install dependencies:
   ```bash
   pip install mcp httpx
   ```
3. (Optional) Install as an MCP service:
   ```bash
   mcp install whereami_mcp.py --name "WhereAmI"
   ```

## Usage

### Running the Server
- Direct execution:
  ```bash
  python whereami_mcp.py
  ```
- Development mode:
  ```bash
  mcp dev whereami_mcp.py
  ```

### Components

#### Resource: `location://{type}`
Returns a specific location detail based on `{type}`.
- **Supported Types**: `ip`, `country`, `country_code`, `region`, `city`, `latitude`, `longitude`, `timezone`, `isp`, `asn`
- **Examples**:
  - `@location://ip` → `"8.8.8.8"`
  - `@location://city` → `"Mountain View"`
  - `@location://country` → `"United States"`

#### Tool: `get_location()`
Generates a detailed Markdown table of geolocation data.
- **Fields**:
  - IP
  - Country
  - Country Code
  - Region
  - City
  - Latitude
  - Longitude
  - Timezone
  - ISP
  - ASN
- **Sample Output**:
  ```
  | Field          | Value             |
  |----------------|-------------------|
  | IP            | 8.8.8.8           |
  | Country       | United States     |
  | Country Code  | US                |
  | Region        | California        |
  | City          | Mountain View     |
  | Latitude      | 37.4223           |
  | Longitude     | -122.0848         |
  | Timezone      | America/Los_Angeles |
  | ISP           | GOOGLE            |
  | ASN           | AS15169           |
  ```

#### Prompt: `where_am_i_prompt`
Predefined query: "Please tell me where I am based on my current IP address." Triggers `get_location()`.

### Examples in Claude Desktop
1. Install the server:
   ```bash
   mcp install whereami_mcp.py --name "WhereAmI"
   ```
2. Query data:
   - "My IP is `@location://ip`"
   - "I’m in `@location://city`, `@location://country`"
3. Get full report:
   - "Where am I?"
   - `get_location()`

## License

MIT License. See [LICENSE](LICENSE) for details.

