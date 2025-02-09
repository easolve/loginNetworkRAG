from agent.tools.express_carrier_tool import express_carrier_tool
from agent.tools.courier_delivery_tool import courier_delivery_tool
from agent.tools.send_message_tool import send_message_tool
from agent.tools.get_deposit_details_tool import get_deposit_details_tool
from agent.tools.get_customs_info_tool import get_customs_info_tool
from agent.tools.connect_manager_tool import connect_manager_tool
from agent.tools.company_info_tool import company_info_tool
from agent.tools.get_user_info_tool import get_user_info_tool
from agent.tools.proceed_import_declaration_tool import (
    proceed_import_declaration_tool,
)
from langgraph.prebuilt import ToolNode

tools = [
    express_carrier_tool,
    # courier_delivery_tool,
    send_message_tool,
    get_deposit_details_tool,
    get_customs_info_tool,
    connect_manager_tool,
    courier_delivery_tool,
    company_info_tool,
    get_user_info_tool,
    proceed_import_declaration_tool,
]
tool_node = ToolNode(tools)
