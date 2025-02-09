from src.agent.tools.manual_tool import manual_tool
from src.agent.tools.express_carrier_tool import express_carrier_tool
from src.agent.tools.courier_delivery_tool import courier_delivery_tool
from src.agent.tools.company_info_tool import company_info_tool
from langgraph.prebuilt import ToolNode

tools = [
    manual_tool,
    express_carrier_tool,
    courier_delivery_tool,
    company_info_tool,
]
tool_node = ToolNode(tools)
