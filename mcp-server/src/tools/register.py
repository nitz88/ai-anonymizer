from . import anonymize, deanonymize

def register_tools(mcp, store):
    anonymize.register(mcp, store)
    deanonymize.register(mcp, store)