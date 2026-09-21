"""Offline behavior checks. Fake transport responses are not model evaluations."""
import copy
import io
import json
import os
import unittest
import urllib.error
from unittest.mock import patch

import decide


class DecisionChecks(unittest.TestCase):
    def setUp(self):
        self.state = {
            "user_request": "保持人物长相，只把背景换成雨夜。",
            "confirmed_constraints": ["保留人物身份"],
            "reference_images": [{"id": "original", "role": "edit_target", "description": "已查看的原图"}]
        }

    def answer(self, phase="plan", **choices):
        default = {"intent": "edit", "preserve_identity": "yes", "preserve_layout": "no", "exact_text": "no", "next_action": "edit"}
        answers = {}
        for name, q in decide.questions(phase).items():
            selected = choices.get(name, default[name])
            answers[name] = {"type": "choice", "choice": selected, "confidence": 0.9,
                             "probabilities": {k: (1.0 if k == selected else 0.0) for k in q["criteria"]}}
        return {"model": decide.MODEL, "answers": answers, "usage": {"input_tokens": 250, "output_tokens": 30}}

    def live(self, payload, state=None, phase="plan"):
        with patch.dict(os.environ, {"TYPESAFE_API_KEY": "fake-offline-test-key"}), patch("urllib.request.OpenerDirector.open") as transport:
            if isinstance(payload, Exception):
                transport.side_effect = payload
            else:
                transport.return_value = io.BytesIO(json.dumps(payload).encode())
            result = decide.evaluate(self.state if state is None else state, phase, "live")
            self.assertEqual(transport.call_count, 1)
            req = transport.call_args.args[0]
            self.assertEqual(req.full_url, decide.ENDPOINT)
            self.assertEqual(req.method, "POST")
            self.assertEqual(transport.call_args.kwargs["timeout"], 8)
            self.assertNotIn("fake-offline-test-key", json.dumps(result))
            return result

    def test_request_and_missing_key_never_contact_network(self):
        with patch.dict(os.environ, {}, clear=True), patch("urllib.request.OpenerDirector.open") as network:
            prepared = decide.evaluate(self.state, "plan")
            self.assertEqual(prepared["status"], "request_only")
            self.assertNotIn("answers", prepared)
            self.assertEqual(decide.evaluate(self.state, "plan", "live")["reason"], "missing_key")
            network.assert_not_called()

    def test_live_decisions_preserve_input_locks(self):
        original = copy.deepcopy(self.state)
        result = self.live(self.answer())
        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["decision_source"], "jev")
        self.assertEqual(self.state, original)
        self.assertEqual(result["usage"]["input_tokens"], 250)

    def test_uncertainty_does_not_authorize_action(self):
        payload = self.answer()
        payload["answers"]["intent"]["confidence"] = 0.79
        self.assertEqual(self.live(payload)["reason"], "uncertain")
        self.assertEqual(self.live(self.answer(intent="unknown"))["reason"], "uncertain")

    def test_edit_needs_target_but_generation_can_use_style_reference(self):
        state = copy.deepcopy(self.state)
        state["reference_images"][0]["role"] = "style_reference"
        self.assertEqual(self.live(self.answer(), state)["reason"], "missing_edit_target")
        self.assertEqual(self.live(self.answer(intent="generate"), state)["status"], "ok")
        self.assertEqual(self.live(self.answer(intent="discuss"), state)["answers"]["intent"]["choice"], "discuss")

    def test_uninspected_review_never_calls_jev(self):
        state = {**self.state, "visual_report": {"output_id": "one", "observer": "codex", "inspected": False, "findings": [], "uncertainties": []}}
        with patch("urllib.request.OpenerDirector.open") as network:
            self.assertEqual(decide.evaluate(state, "review", "live")["reason"], "uninspected_output")
            network.assert_not_called()
        state["visual_report"].update(inspected=True, findings=["眼镜缺失"])
        self.assertEqual(self.live(self.answer("review"), state, "review")["answers"]["next_action"]["choice"], "edit")
        self.assertEqual(self.live(self.answer("review", next_action="human_review"), state, "review")["reason"], "uncertain")

    def test_malformed_answers_fall_back(self):
        cases = []
        for field, value in (("confidence", float("nan")), ("confidence", True), ("choice", []), ("probabilities", {"edit": 1.0})):
            item = self.answer()
            item["answers"]["intent"][field] = value
            cases.append(item)
        item = self.answer()
        del item["answers"]["exact_text"]
        cases.extend([item, {}, [], {**self.answer(), "usage": {"input_tokens": -1}}])
        for item in cases:
            with self.subTest(payload=item):
                self.assertEqual(self.live(item)["reason"], "invalid_response")

    def test_timeouts_and_http_errors_no_retry_or_sensitive_body(self):
        errors = [(TimeoutError("fake-secret-body"), "timeout"),
                  (urllib.error.URLError(TimeoutError()), "timeout"),
                  (urllib.error.URLError("fake-secret-body"), "network_error"),
                  (urllib.error.HTTPError(decide.ENDPOINT, 429, "fake-secret-body", {}, None), "http_429")]
        for error, reason in errors:
            result = self.live(error)
            self.assertEqual(result["reason"], reason)
            self.assertNotIn("fake-secret-body", json.dumps(result))
            self.assertNotIn("answers", result)
        self.assertIsNone(decide.NoRedirect().redirect_request(None, None, 302, "", {}, "https://example.org"))

    def test_input_validation_rejects_extra_fields_and_bad_values(self):
        cases = [{}, {"user_request": ""}, {**self.state, "api_key": "do-not-send"},
                 {**self.state, "confirmed_constraints": "not an array"},
                 {**self.state, "user_request": "字" * 25000}]
        with patch("urllib.request.OpenerDirector.open") as network:
            for value in cases:
                with self.assertRaises(ValueError):
                    decide.evaluate(value, "plan", "live")
            with self.assertRaises(ValueError):
                decide.evaluate(self.state, "plan", min_confidence=float("nan"))
            network.assert_not_called()


if __name__ == "__main__":
    unittest.main(verbosity=2)
