from xoneaiagents import Agent

config = {
    "vector_store": {
        "provider": "chroma",
        "config": {
            "collection_name": "xone",
            "path": ".xone",
        }
    }
}

agent = Agent(
    name="Knowledge Agent",
    instructions="You answer questions based on the provided knowledge.",
    knowledge=["small.pdf"]
)

agent.start("What is KAG in one line?")