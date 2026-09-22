import socket
import unittest
from unittest.mock import patch
from ota_auth_probe import probe


class ProbeTests(unittest.TestCase):
    def run_probe(self, replies):
        with patch("ota_auth_probe.socket.socket") as factory:
            connection = factory.return_value.__enter__.return_value
            connection.recv.side_effect = replies
            result = probe("127.0.0.1")
            self.assertLessEqual(connection.send.call_count, 2)
            return result, connection

    def test_challenge_and_explicit_rejection(self):
        result, connection = self.run_probe([b"AUTH " + b"a" * 32, b"Authentication Failed"])
        self.assertEqual("PASS", result["status"])
        self.assertEqual(2, connection.send.call_count)

    def test_no_auth_is_failure_and_stops(self):
        result, connection = self.run_probe([b"OK"])
        self.assertEqual("FAIL", result["status"])
        self.assertEqual(1, connection.send.call_count)

    def test_invalid_proof_accepted_is_failure(self):
        result, _ = self.run_probe([b"AUTH " + b"a" * 32, b"OK"])
        self.assertEqual("FAIL", result["status"])

    def test_unexpected_response_is_inconclusive(self):
        result, _ = self.run_probe([b"garbage"])
        self.assertEqual("INCONCLUSIVE", result["status"])

    def test_timeout_is_not_a_pass(self):
        with self.assertRaises(socket.timeout):
            self.run_probe([socket.timeout()])


if __name__ == "__main__":
    unittest.main()
