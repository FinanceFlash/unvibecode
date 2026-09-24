"""Validate guardrail design configuration; never execute configured bindings."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import re
import sys

SCHEMA_VERSION = "1.0"
APPLICATIONS = ("chatbot", "rag", "agent", "multi_agent")
CONTROLS = {
    "input_pii": ("input", "specialized_classifier"),
    "input_intent": ("input", "semantic_classifier"),
    "input_injection": ("input", "specialized_classifier"),
    "input_content_policy": ("input", "specialized_classifier"),
    "output_pii": ("answer", "specialized_classifier"),
    "output_content_policy": ("answer", "specialized_classifier"),
    "retrieval_authorization": ("retrieval", "deterministic"),
    "source_provenance": ("retrieval", "deterministic"),
    "retrieved_injection": ("retrieval", "specialized_classifier"),
    "evidence_sufficiency": ("evidence", "evaluator"),
    "answer_grounding": ("answer", "evaluator"),
    "tool_schema": ("before_tool", "deterministic"),
    "tool_authorization": ("before_tool", "deterministic"),
    "resource_ownership": ("before_tool", "deterministic"),
    "egress_allowlist": ("before_tool", "deterministic"),
    "side_effect_idempotency": ("before_tool", "deterministic"),
    "tool_result_injection": ("after_tool", "specialized_classifier"),
    "memory_write_policy": ("memory_write", "deterministic"),
    "memory_write_injection": ("memory_write", "specialized_classifier"),
    "memory_read_injection": ("memory_read", "specialized_classifier"),
    "message_identity": ("agent_handoff", "deterministic"),
    "delegation_permissions": ("agent_handoff", "deterministic"),
    "handoff_provenance": ("agent_handoff", "deterministic"),
    "handoff_injection": ("agent_handoff", "specialized_classifier"),
}
BASE = {"input_pii", "input_intent", "input_injection", "input_content_policy",
        "output_pii", "output_content_policy"}
GROUPS = {
    "retrieval": {"retrieval_authorization", "source_provenance", "retrieved_injection",
                  "evidence_sufficiency", "answer_grounding"},
    "tools": {"tool_schema", "tool_authorization", "resource_ownership", "egress_allowlist",
              "side_effect_idempotency", "tool_result_injection"},
    "memory": {"memory_write_policy", "memory_write_injection", "memory_read_injection"},
    "multi_agent": {"message_identity", "delegation_permissions", "handoff_provenance", "handoff_injection"},
}


def make_profile(application):
    if application not in APPLICATIONS:
        raise ValueError("Unknown application.")
    features = {"retrieval": application in ("rag", "multi_agent"),
                "tools": application in ("agent", "multi_agent"),
                "memory": application in ("agent", "multi_agent")}
    required = set(BASE)
    for name, enabled in features.items():
        if enabled:
            required.update(GROUPS[name])
    if application == "multi_agent":
        required.update(GROUPS["multi_agent"])
    return {
        "schema_version": SCHEMA_VERSION, "policy_version": "0.1.0", "application": application,
        "features": features,
        "controls": {name: {"stage": CONTROLS[name][0], "tier": CONTROLS[name][1],
                            "execution": "before_release", "on_error": "withhold",
                            "binding": None} for name in sorted(required)},
        "pii": {"geographies": ["IN"], "language": "en", "action": "redact",
                "recognizer_version": "2.2.364"},
        "intent": {"supported": ["invoice", "duplicate_charge", "payment_failure", "refund", "cancel", "account_access"],
                   "on_uncertain": "clarify", "max_clarifications": 2,
                   "model_artifact": None, "thresholds_artifact": None},
        "injection": {"model_id": "rogue-security/prompt-injection-jailbreak-sentinel-v2",
                      "revision": "05ff9bfd1f28c5228e53121d5ee4427bb5205212",
                      "context_tokens": 32768, "max_input_tokens": 32768,
                      "overflow": "withhold", "review_threshold": 0.30, "block_threshold": 0.85,
                      "access_confirmed": False},
        "runtime": {"request_deadline_ms": 15000, "guard_deadline_ms": 5000,
                    "timeout_enforcement": "supervised_worker", "queue_limit": 32,
                    "max_inflight": 4, "max_model_calls": 4, "max_tool_calls": 6,
                    "max_retries": 1, "max_agent_hops": 4,
                    "budget_scope": "shared_request", "output_release": "after_checks"},
        "observability": {"log_payloads": False, "retention_days": 14,
                          "include_policy_version": True, "include_model_revision": True},
    }


def fingerprint(config):
    return sha256(json.dumps(config, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()).hexdigest()


def read_config(path):
    path = Path(path)
    if path.stat().st_size > 1_000_000:
        raise ValueError("Configuration exceeds 1 MB.")
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError("Duplicate JSON key.")
            result[key] = value
        return result
    def reject_constant(value):
        raise ValueError("Non-finite JSON number.")
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=pairs,
                      parse_constant=reject_constant)


def check(config):
    issues = []
    def issue(level, code, path, message):
        issues.append({"severity": level, "code": code, "path": path, "message": message})
    def error(code, path, message):
        issue("ERROR", code, path, message)
    def warning(code, path, message):
        issue("WARNING", code, path, message)
    def positive(value):
        return type(value) is int and value > 0
    def shape(value, expected, path):
        if not isinstance(value, dict):
            error("SCHEMA", path, "Expected an object.")
            return False
        if set(value) != set(expected):
            error("SCHEMA", path, "Keys must match the supplied profile schema; missing or unknown keys found.")
            return False
        return True
    template = make_profile("chatbot")
    if not shape(config, template, "$"):
        return report(config, issues)
    for name in ("features", "pii", "intent", "injection", "runtime", "observability"):
        shape(config[name], template[name], name)
    if issues:
        return report(config, issues)
    application = config["application"]
    if application not in APPLICATIONS:
        error("APPLICATION", "application", "Choose chatbot, rag, agent, or multi_agent.")
    if config["schema_version"] != SCHEMA_VERSION:
        error("SCHEMA_VERSION", "schema_version", "Unsupported schema version.")
    if not isinstance(config["policy_version"], str) or not re.fullmatch(r"\d+\.\d+\.\d+", config["policy_version"]):
        error("POLICY_VERSION", "policy_version", "Use an explicit major.minor.patch version.")
    features = config["features"]
    if any(type(value) is not bool for value in features.values()):
        error("FEATURE_TYPE", "features", "Feature flags must be booleans.")
    if application == "rag" and features["retrieval"] is not True:
        error("RAG_RETRIEVAL", "features.retrieval", "RAG requires retrieval controls.")
    if application in ("agent", "multi_agent") and features["tools"] is not True:
        error("AGENT_TOOLS", "features.tools", "These agent profiles require tool controls.")
    required = set(BASE)
    for name, enabled in features.items():
        if enabled is True:
            required.update(GROUPS[name])
    if application == "multi_agent":
        required.update(GROUPS["multi_agent"])
    controls = config["controls"]
    if not isinstance(controls, dict):
        error("CONTROLS", "controls", "Expected a control dictionary.")
    else:
        for name in sorted(required - set(controls)):
            error("MISSING_CONTROL", "controls." + name, "Required control is absent for this application or feature.")
        for name, control in controls.items():
            path = "controls." + name
            if name not in CONTROLS:
                error("UNKNOWN_CONTROL", path, "Unknown control; extend the checker before introducing new control names.")
                continue
            expected = {"stage", "tier", "execution", "on_error", "binding"}
            if not shape(control, expected, path):
                continue
            if control["stage"] != CONTROLS[name][0]:
                error("WRONG_STAGE", path + ".stage", "Place the control at " + CONTROLS[name][0] + ".")
            if control["tier"] not in ("deterministic", "semantic_classifier", "specialized_classifier", "evaluator"):
                error("TIER", path + ".tier", "Unknown implementation tier.")
            if CONTROLS[name][1] == "deterministic" and control["tier"] != "deterministic":
                error("AUTHORITY_BY_MODEL", path + ".tier", "Permissions and structural constraints require deterministic enforcement.")
            if control["execution"] != "before_release":
                error("LATE_CHECK", path + ".execution", "Complete this check before its protected boundary is crossed.")
            if control["on_error"] not in ("withhold", "human_review"):
                error("FAIL_OPEN", path + ".on_error", "This mandatory control must withhold or require human review on failure.")
            binding = control["binding"]
            if binding is None:
                warning("UNBOUND", path + ".binding", "Supply the application's callable reference; it is not implemented by this config.")
            elif not isinstance(binding, str) or not re.fullmatch(r"[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)+", binding):
                error("BINDING", path + ".binding", "Use a dotted callable reference, or null while designing.")
    pii = config["pii"]
    if (not isinstance(pii["geographies"], list) or not pii["geographies"]
            or any(not isinstance(g, str) or g not in ("IN", "US", "GB", "SG", "AU", "CA") for g in pii["geographies"])):
        error("PII_GEOGRAPHY", "pii.geographies", "Use the geographies implemented by notebook 01; extend coverage explicitly.")
    if pii["language"] != "en" or pii["action"] not in ("redact", "block"):
        error("PII_POLICY", "pii", "The supplied integration supports English and redact/block actions.")
    if not isinstance(pii["recognizer_version"], str) or not pii["recognizer_version"].strip():
        error("PII_VERSION", "pii.recognizer_version", "Pin the recognizer package version.")
    intent = config["intent"]
    supported = intent["supported"]
    if not isinstance(supported, list) or not supported or any(not isinstance(v, str) or not v for v in supported):
        error("INTENT_LABELS", "intent.supported", "Provide nonempty supported business intent labels.")
    if intent["on_uncertain"] not in ("clarify", "human_review"):
        error("UNCERTAIN_IS_NOT_OOS", "intent.on_uncertain", "Uncertain classification must not automatically become out of scope.")
    if not positive(intent["max_clarifications"]):
        error("CLARIFICATION_LIMIT", "intent.max_clarifications", "Bound clarification attempts.")
    for name in ("model_artifact", "thresholds_artifact"):
        if intent[name] is None:
            warning("MISSING_ARTIFACT", "intent." + name, "Reference the trained model or validation-selected thresholds from notebook 02.")
        elif not isinstance(intent[name], str) or not intent[name].strip():
            error("ARTIFACT", "intent." + name, "Expected a nonempty artifact reference.")
    injection = config["injection"]
    if injection["model_id"] != template["injection"]["model_id"]:
        error("MODEL_CONTRACT", "injection.model_id", "This profile targets the notebook 03 Sentinel adapter; review the contract before replacing it.")
    if not isinstance(injection["revision"], str) or not re.fullmatch(r"[a-f0-9]{40}", injection["revision"]):
        error("MODEL_REVISION", "injection.revision", "Pin a full model commit SHA.")
    context, maximum = injection["context_tokens"], injection["max_input_tokens"]
    if not positive(context) or not positive(maximum) or maximum > context or context > 32768:
        error("CONTEXT_LIMIT", "injection", "Require 0 < max_input_tokens <= context_tokens <= 32768.")
    if injection["overflow"] != "withhold":
        error("SILENT_TRUNCATION", "injection.overflow", "Do not pass a partially scanned input.")
    low, high = injection["review_threshold"], injection["block_threshold"]
    if type(low) not in (int, float) or type(high) not in (int, float) or not 0 <= low < high <= 1:
        error("THRESHOLDS", "injection", "Require 0 <= review_threshold < block_threshold <= 1.")
    if type(injection["access_confirmed"]) is not bool:
        error("ACCESS_TYPE", "injection.access_confirmed", "Expected a boolean.")
    elif not injection["access_confirmed"]:
        warning("MODEL_ACCESS", "injection.access_confirmed", "Confirm authorized model access; initialization must withhold on failure.")
    runtime = config["runtime"]
    for name in ("request_deadline_ms", "guard_deadline_ms", "queue_limit", "max_inflight",
                 "max_model_calls", "max_tool_calls", "max_agent_hops"):
        if not positive(runtime[name]):
            error("UNBOUNDED_WORK", "runtime." + name, "Set a positive integer bound.")
    if type(runtime["max_retries"]) is not int or runtime["max_retries"] < 0:
        error("RETRIES", "runtime.max_retries", "Set a nonnegative integer retry bound.")
    if positive(runtime["guard_deadline_ms"]) and positive(runtime["request_deadline_ms"]) and runtime["guard_deadline_ms"] >= runtime["request_deadline_ms"]:
        error("DEADLINE_ORDER", "runtime", "A guard deadline must fit inside the request deadline.")
    if runtime["timeout_enforcement"] not in ("supervised_worker", "external_service"):
        error("SOFT_TIMEOUT", "runtime.timeout_enforcement", "Declare real deadline enforcement; an elapsed-time check alone is insufficient.")
    if runtime["budget_scope"] != "shared_request":
        error("BUDGET_RESET", "runtime.budget_scope", "Keep model/tool/retry/handoff counters across the entire request.")
    if runtime["output_release"] != "after_checks":
        error("OUTPUT_LEAK", "runtime.output_release", "Hold output until its mandatory checks pass.")
    obs = config["observability"]
    if obs["log_payloads"] is not False:
        error("SENSITIVE_LOGS", "observability.log_payloads", "This baseline records metadata only; raw and redacted text can contain sensitive data.")
    if obs["include_policy_version"] is not True or obs["include_model_revision"] is not True:
        error("UNVERSIONED_DECISIONS", "observability", "Record policy and model versions with decisions.")
    if not positive(obs["retention_days"]):
        error("LOG_RETENTION", "observability.retention_days", "Specify a positive retention period.")
    return report(config, issues)


def report(config, issues):
    try:
        digest = fingerprint(config)
    except (ValueError, TypeError):
        digest = None
    return {"configuration_valid": not any(i["severity"] == "ERROR" for i in issues),
            "runtime_verified": False, "configuration_sha256": digest,
            "errors": sum(i["severity"] == "ERROR" for i in issues),
            "warnings": sum(i["severity"] == "WARNING" for i in issues), "issues": issues}


def questions(config):
    result = check(config)
    if not result["configuration_valid"]:
        raise ValueError("Fix configuration errors before generating design questions.")
    features = config["features"]
    boundary = "document/tenant permissions and source versions" if features["retrieval"] else "account identity and conversation state"
    operations = "tool allowlists, ownership, approval limits, and idempotency" if features["tools"] else "supported intents, missing fields, and handoff destinations"
    memory = "memory retention, permitted writes, and checks before reuse" if features["memory"] else "conversation retention and isolation between users"
    return [
        f"For this {config['application']} profile, which listed intents apply, which exclusions need examples, and what data languages/geographies differ from the English/PII settings?",
        f"How will the application enforce {boundary}, and which service is authoritative?",
        f"What concrete rules and test cases define {operations}?",
        f"What requirements govern {memory}, and who can change the policy?",
        "What measured latency, false-rejection, missed-risk, and handoff targets should determine thresholds and worker/queue limits?",
        "For each missing binding/artifact, which implementation will enforce the check, and what should the user see on timeout, uncertainty, or exhausted shared budgets?",
    ]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    init = commands.add_parser("init")
    init.add_argument("--app", choices=APPLICATIONS, required=True)
    init.add_argument("--out", type=Path, required=True)
    validate = commands.add_parser("check")
    validate.add_argument("--config", type=Path, required=True)
    validate.add_argument("--strict", action="store_true", help="Exit nonzero on unresolved warnings too.")
    guide = commands.add_parser("questions")
    guide.add_argument("--config", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "init":
            with args.out.open("x", encoding="utf-8") as file:
                json.dump(make_profile(args.app), file, indent=2)
            print(f"Created {args.out}")
            return 0
        config = read_config(args.config)
        if args.command == "questions":
            print(json.dumps({"questions": questions(config)}, indent=2))
            return 0
        result = check(config)
        print(json.dumps(result, indent=2))
        return int(not result["configuration_valid"] or (args.strict and result["warnings"] > 0))
    except (OSError, ValueError, TypeError):
        print(json.dumps({"configuration_valid": False, "runtime_verified": False,
                          "error": "Invalid configuration or file operation; check the schema and path."}))
        return 2


if __name__ == "__main__":
    sys.exit(main())
