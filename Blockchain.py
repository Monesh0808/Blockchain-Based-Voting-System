from flask import Flask, request, render_template
import hashlib
import json
import time

app = Flask(__name__)

blockchain = []
votes = {}

def create_block(data):
    previous_hash = (
        blockchain[-1]["hash"] if blockchain else "0"
    )

    block = {
        "index": len(blockchain) + 1,
        "timestamp": time.time(),
        "data": data,
        "previous_hash": previous_hash
    }

    block_string = json.dumps(block, sort_keys=True).encode()
    block["hash"] = hashlib.sha256(block_string).hexdigest()

    blockchain.append(block)


@app.route("/")
def home():
    return """
    <h2>Blockchain Voting System</h2>
    <form method="POST" action="/vote">
        Voter ID: <input name="voter"><br><br>
        Candidate: <input name="candidate"><br><br>
        <button type="submit">Vote</button>
    </form>
    """


@app.route("/vote", methods=["POST"])
def vote():
    voter = request.form["voter"]
    candidate = request.form["candidate"]

    if voter in votes:
        return "Voter has already voted!"

    votes[voter] = candidate

    create_block({
        "voter": voter,
        "candidate": candidate
    })

    return "Vote successfully recorded!"


@app.route("/blockchain")
def show_blockchain():
    return {
        "blockchain": blockchain
    }


if __name__ == "__main__":
    app.run(debug=True)
