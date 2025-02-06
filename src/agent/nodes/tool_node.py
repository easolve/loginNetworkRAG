from src.agent.tools.retriever_tool import retriever_tool
from src.agent.tools.express_carrier_tool import express_carrier_tool
from src.agent.tools.courier_delivery_tool import courier_delivery_tool
from langgraph.prebuilt import ToolNode

tools = [retriever_tool, express_carrier_tool, courier_delivery_tool]
tool_node = ToolNode(tools)
