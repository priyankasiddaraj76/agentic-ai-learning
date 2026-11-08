from app.models import ProcessResponse, EchoResponse, AgentMessage

def create_echo_response(request: AgentMessage) -> EchoResponse:
    return EchoResponse(
        message=request.message,
        agent_name=request.agent_name,
        status="received",
        message_length=len(request.message)
    )

def process_message(request: AgentMessage) -> ProcessResponse:
    processed_message = request.message.lower()  # Example processing: convert to lowercase
    word_count = len(request.message.split())
    return ProcessResponse(
        original_message=request.message,
        processed_message=processed_message,
        agent_name=request.agent_name,
        word_count=word_count
    )