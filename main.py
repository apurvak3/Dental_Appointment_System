from flask import Flask, render_template, request, jsonify, redirect, url_for
from langchain_core.messages import HumanMessage, AIMessage
from dental_agent.agent import dental_graph

app = Flask(__name__)

history = []

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["GET", "POST"])
def chat():
    global history

    if request.method == "GET":
        return redirect(url_for("home"))

    user_input = request.json.get("message")

    history.append(HumanMessage(content=user_input))

    result = dental_graph.invoke(
        {"messages": history},
        config={"recursion_limit": 20},
    )

    final_messages = result.get("messages", [])
    history = final_messages

    response_text = ""
    for message in reversed(final_messages):
        if isinstance(message, AIMessage) and message.content and not getattr(message, "tool_calls", None):
            response_text = str(message.content)
            break

    return jsonify({"response": response_text})


if __name__ == "__main__":
    app.run(debug=True)
