from flask import Flask, render_template, request, jsonify
from langchain_core.messages import HumanMessage, AIMessageChunk
from dental_agent.agent import dental_graph

app = Flask(__name__)

history = []

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    global history

    user_input = request.json.get("message")

    history.append(HumanMessage(content=user_input))

    final_messages = None
    response_text = ""

    for event_type, data in dental_graph.stream(
        {"messages": history},
        stream_mode=["messages", "values"],
        config={"recursion_limit": 20},
    ):
        if event_type == "messages":
            chunk, meta = data
            if (
                isinstance(chunk, AIMessageChunk)
                and chunk.content
                and not getattr(chunk, "tool_calls", None)
            ):
                response_text += chunk.content

        elif event_type == "values":
            final_messages = data.get("messages", [])

    if final_messages:
        history = final_messages

    return jsonify({"response": response_text})


if __name__ == "__main__":
    app.run(debug=True)