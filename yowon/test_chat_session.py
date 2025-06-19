import unittest
import yowon.agent as agent

class FakeAgent:
    def __init__(self):
        self.calls = []
    def run(self, prompt, reset=True, **kwargs):
        self.calls.append((prompt, reset))
        return f"echo:{prompt}-{reset}"

class ChatSessionTests(unittest.TestCase):
    def test_maintains_reset_flag(self):
        original = agent.create_agent
        try:
            agent.create_agent = lambda **kwargs: FakeAgent()
            session = agent.ChatSession()
            first = session.ask("hi")
            second = session.ask("again")
        finally:
            agent.create_agent = original
        self.assertEqual(first, "echo:hi-True")
        self.assertEqual(second, "echo:again-False")

if __name__ == "__main__":
    unittest.main()
