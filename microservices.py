import zmq

LABELS_PORT = 5557
PROMPTS_PORT = 5556
TIMESTAMP_PORT = 5555

def send_request(port, request_data):
    """
    Send a request to a microservice and return the response.
    """
    context = zmq.Context()
    socket = context.socket(zmq.REQ)

    socket.connect(f"tcp://127.0.0.1:{port}")

    socket.send_json(request_data)
    response = socket.recv_json()

    socket.close()
    context.term()

    return response


def request_label(request_text, details=None):
    """
    Request a label from the Labels Microservice.
    """
    try:
        response = send_request(
            LABELS_PORT,
            {
                "request": request_text,
                "details": details
            }
        )

        if response["success"]:
            label = response["label"]

            if label.startswith("Error:"):
                return None

            return label

        return None

    except Exception:
        return None


def request_prompt(request_text, details=None):
    """
    Request a prompt from the Prompts Microservice.
    """
    try:
        response = send_request(
            PROMPTS_PORT,
            {
                "request": request_text,
                "details": details
            }
        )

        if response["success"]:
            prompt = response["prompt"]

            if prompt.startswith("Error:"):
                return None

            return prompt

        return None

    except Exception:
        return None


def request_timestamp(app_name, user_id, timestamp_format):
    """
    Request a timestamp from the Timestamp Microservice.
    """

    response = send_request(
        TIMESTAMP_PORT,
        {
            "app_name": app_name,
            "user_id": user_id,
            "timestamp_format": timestamp_format
        }
    )

    return response