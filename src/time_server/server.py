"""
Time Server - Get current time in your configured timezone
"""

from datetime import datetime
from zoneinfo import ZoneInfo

from mcp.server.fastmcp import Context, FastMCP
from pydantic import BaseModel, Field

from smithery.decorators import smithery


# Configuration schema for timezone
class ConfigSchema(BaseModel):
    timezone: str = Field(
        "UTC", 
        description="Timezone (e.g., 'America/New_York', 'Europe/London', 'Asia/Tokyo')"
    )


@smithery.server(config_schema=ConfigSchema)
def create_server():
    """Create and configure the time server."""

    server = FastMCP("Time Server")

    @server.tool()
    def get_current_time(ctx: Context) -> str:
        """Get the current time in the configured timezone."""
        session_config = ctx.session_config
        
        try:
            # Get current time in the configured timezone
            tz = ZoneInfo(session_config.timezone)
            current_time = datetime.now(tz)
            
            # Format the time nicely
            formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S %Z")
            day_name = current_time.strftime("%A")
            
            return f"The current time in {session_config.timezone} is:\n{formatted_time} ({day_name})"
        
        except Exception as e:
            return f"Error: Invalid timezone '{session_config.timezone}'. Please use a valid timezone like 'America/New_York', 'Europe/London', or 'Asia/Tokyo'."

    @server.resource("timezone://info")
    def timezone_info() -> str:
        """Information about common timezones."""
        return """Common Timezones:
- UTC (Coordinated Universal Time)
- America/New_York (Eastern Time)
- America/Chicago (Central Time)
- America/Denver (Mountain Time)
- America/Los_Angeles (Pacific Time)
- Europe/London (GMT/BST)
- Europe/Paris (CET/CEST)
- Asia/Tokyo (JST)
- Asia/Shanghai (CST)
- Australia/Sydney (AEST/AEDT)

For a full list, see: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones"""

    return server
