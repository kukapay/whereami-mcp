# whereami_mcp.py
import httpx
from mcp.server.fastmcp import FastMCP, Context

# Initialize the MCP server
mcp = FastMCP("WhereAmI", dependencies=["httpx"])

# API endpoint from ipapi.co
API_URL = "https://ipapi.co/json/"

# Mapping of type to API field names
LOCATION_FIELDS = {
    "ip": "ip",
    "country": "country_name",
    "country_code": "country_code",
    "region": "region",
    "city": "city",
    "latitude": "latitude",
    "longitude": "longitude",
    "timezone": "timezone",
    "isp": "org",
    "asn": "asn"
}

@mcp.resource("location://{type}")
def get_location_data(type: str) -> str:
    """
    Get specific location data based on the type parameter.
    Supported types: ip, country, country_code, region, city, latitude, longitude, timezone, isp, asn
    """
    if type not in LOCATION_FIELDS:
        return f"Error: Invalid type '{type}'. Supported types: {', '.join(LOCATION_FIELDS.keys())}"
    
    try:
        response = httpx.get(API_URL)
        response.raise_for_status()
        data = response.json()
        field = LOCATION_FIELDS[type]
        return str(data[field])
    except httpx.HTTPError as e:
        return f"Error fetching location data: {str(e)}"
    except KeyError:
        return f"Error: Field '{field}' not found in API response"

@mcp.tool()
def get_location(ctx: Context) -> str:
    """
    Get detailed location information based on current IP.
    
    Returns a Markdown table containing:
    - IP: The current public IP address
    - Country: Full country name
    - Country Code: Two-letter country code (ISO 3166-1 alpha-2)
    - Region: State or region name
    - City: City name
    - Latitude: Geographic latitude coordinate
    - Longitude: Geographic longitude coordinate
    - Timezone: IANA timezone identifier
    - ISP: Internet Service Provider name
    - ASN: Autonomous System Number
    """
    try:
        # Make API request
        response = httpx.get(API_URL)
        response.raise_for_status()
        data = response.json()
        
        # Construct Markdown table
        table = [
            "| Field          | Value             |",
            "|----------------|-------------------|",
            f"| IP            | {data['ip']}      |",
            f"| Country       | {data['country_name']} |",
            f"| Country Code  | {data['country_code']} |",
            f"| Region        | {data['region']}   |",
            f"| City          | {data['city']}     |",
            f"| Latitude      | {data['latitude']} |",
            f"| Longitude     | {data['longitude']}|",
            f"| Timezone      | {data['timezone']} |",
            f"| ISP           | {data['org']}      |",
            f"| ASN           | {data['asn']}      |"
        ]
        
        markdown_table = "\n".join(table)
        
        ctx.info(f"Successfully retrieved location for IP: {data['ip']}")
        return markdown_table
    
    except httpx.HTTPError as e:
        ctx.error(f"Failed to fetch location data: {str(e)}")
        return f"Error: HTTP error occurred - {str(e)}"
    except Exception as e:
        ctx.error(f"Unexpected error: {str(e)}")
        return f"Error: Unexpected error occurred - {str(e)}"

@mcp.prompt()
def where_am_i_prompt() -> str:
    """Prompt template for asking about current location"""
    return "Please tell me where I am based on my current IP address."

if __name__ == "__main__":
    mcp.run()