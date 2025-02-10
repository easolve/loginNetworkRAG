from langchain_core.messages import AIMessage, AnyMessage, HumanMessage, SystemMessage, ToolMessage


def message_to_text(messages: list[AnyMessage]) -> str:
    """
    Converts a list of messages into a formatted text string.
    Args:
      messages (list[AnyMessage]): A list of message objects. Each message object should have a 'content' attribute.
    Returns:
      str: A formatted string where each message is prefixed with 'user:', 'ai:', or 'system:' based on the message type.
    """

    text = ""

    for message in messages:
        if not isinstance(message.content, str):
            continue
        if isinstance(message, HumanMessage):
            text += f"user: {message.content}\n"
        elif isinstance(message, AIMessage):
            text += f"ai: {message.content}\n"
        elif isinstance(message, ToolMessage):
            text += f"tool: {message.content}\n"
        else:
            text += f"system: {message.content}\n"
    return text


if __name__ == "__main__":
    test_messages = [
        SystemMessage("Welcome to the chatbot!"),
        HumanMessage("Hello!"),
        AIMessage("Hi! How can I help you today?"),
        HumanMessage("I need help with my computer."),
        AIMessage("Sure! What seems to be the problem?"),
    ]

    print(message_to_text(test_messages))
