#!/usr/bin/env python3
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REQUIRED_FILES = [
    'README.md',
    'AGENTS.md',
    'manifest.yaml',
    'agents/manifest.yaml',
    'agents/hermes/agent.yaml',
    'agents/openclaw/agent.yaml',
    'agents/future-agent/agent.yaml',
    'registry/manifest.yaml',
    'registry/capabilities/manifest.yaml',
    'registry/capabilities/hermes.yaml',
    'registry/capabilities/openclaw.yaml',
    'registry/capabilities/future-agent.yaml',
    'truth/memory/MEMORY.md',
    'truth/memory/facts/.gitkeep',
    'truth/memory/projects/.gitkeep',
    'truth/promote-logs/.gitkeep',
    'sandbox/hermes/.gitkeep',
    'sandbox/openclaw/.gitkeep',
    'sandbox/future-agent/.gitkeep',
    'sandbox/openclaw/submissions/demo-fact.md',
    'sandbox/hermes/promote-requests/demo-fact.md',
    'schema/manifest.schema.yaml',
    'schema/agent.schema.yaml',
    'policy/write-rules.yaml',
    'protocol/promote-protocol.md',
    'protocol/promote-log-template.md',
    'tools/promote_executor.py',
    'scripts/verify_v3.sh',
]
FORBIDDEN_DIRS = ['compat', 'memory', 'skills']
REQUIRED_AGENT_FIELDS = [
    'agent_id:',
    'role:',
    'mode:',
    'direct_truth_write:',
    'truth_access:',
    'sandbox_path:',
    'allowed_operations:',
]
DEMO_RECORD = 'sandbox/hermes/promote-requests/demo-fact.md'
DEMO_SOURCE = 'sandbox/openclaw/submissions/demo-fact.md'
DEMO_TARGET = 'truth/memory/facts/demo-fact.md'
DEMO_LOG = 'truth/promote-logs/promote-20260417-demo001.md'


def read_text(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding='utf-8')


def require(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def top_level_scalar(text: str, key: str) -> str | None:
    pattern = re.compile(rf'^{re.escape(key)}:\s*(.+?)\s*$', re.MULTILINE)
    match = pattern.search(text)
    return match.group(1) if match else None


def path_exists(relative_path: str) -> bool:
    return (ROOT / relative_path).exists()


def contains_all(text: str, tokens: list[str]) -> bool:
    return all(token in text for token in tokens)


def count_token(text: str, token: str) -> int:
    return text.count(token)


def run_command(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=ROOT, capture_output=True, text=True)


def clean_demo_outputs() -> None:
    for relative_path in (DEMO_TARGET, DEMO_LOG):
        path = ROOT / relative_path
        if path.exists():
            path.unlink()


def verify_stage3_execution(failures: list[str]) -> None:
    clean_demo_outputs()

    dry_run = run_command([sys.executable, str(ROOT / 'tools/promote_executor.py'), DEMO_RECORD, '--dry-run'])
    require(dry_run.returncode == 0, 'promote executor dry-run must succeed', failures)
    require('DRY-RUN' in dry_run.stdout, 'promote executor dry-run output must mention DRY-RUN', failures)
    require(DEMO_TARGET in dry_run.stdout, 'promote executor dry-run must resolve demo target path', failures)

    apply_run = run_command([sys.executable, str(ROOT / 'tools/promote_executor.py'), DEMO_RECORD])
    require(apply_run.returncode == 0, 'promote executor apply run must succeed', failures)
    require('SUCCESS' in apply_run.stdout, 'promote executor apply output must mention SUCCESS', failures)

    require(path_exists(DEMO_TARGET), f'demo promote target must exist: {DEMO_TARGET}', failures)
    require(path_exists(DEMO_LOG), f'demo promote log must exist: {DEMO_LOG}', failures)

    if path_exists(DEMO_SOURCE) and path_exists(DEMO_TARGET):
        require(read_text(DEMO_SOURCE) == read_text(DEMO_TARGET), 'demo target content must match sandbox source', failures)

    memory_text = read_text('truth/memory/MEMORY.md') if path_exists('truth/memory/MEMORY.md') else ''
    require('<!-- SHARED-V3-PROMOTE-ENTRIES:START -->' in memory_text, 'MEMORY.md must contain managed promote block start marker', failures)
    require('<!-- SHARED-V3-PROMOTE-ENTRIES:END -->' in memory_text, 'MEMORY.md must contain managed promote block end marker', failures)
    require('promote-20260417-demo001' in memory_text, 'MEMORY.md managed block must include demo promote record', failures)

    log_text = read_text(DEMO_LOG) if path_exists(DEMO_LOG) else ''
    for field in ('executed_at:', 'source_sha256:', 'target_sha256:'):
        require(field in log_text, f'demo promote log must include {field}', failures)


def main() -> int:
    failures: list[str] = []

    for relative_path in REQUIRED_FILES:
        require(path_exists(relative_path), f'missing required file: {relative_path}', failures)

    manifest_text = read_text('manifest.yaml') if path_exists('manifest.yaml') else ''
    require(top_level_scalar(manifest_text, 'version') == '3', 'manifest version must be 3', failures)
    require(top_level_scalar(manifest_text, 'name') == 'shared-hub-v3', 'manifest name must be shared-hub-v3', failures)
    require(top_level_scalar(manifest_text, 'layout') == 'protocol-first', 'manifest layout must be protocol-first', failures)
    require(top_level_scalar(manifest_text, 'root_model') == 'minimal-kernel', 'manifest root_model must be minimal-kernel', failures)
    require(top_level_scalar(manifest_text, 'status') == 'stage3', 'manifest status must be stage3', failures)
    require('capability_registry: registry/capabilities/manifest.yaml' in manifest_text, 'manifest must reference capability registry', failures)
    require('agent_schema: schema/agent.schema.yaml' in manifest_text, 'manifest must reference agent schema', failures)
    require('promote_protocol: protocol/promote-protocol.md' in manifest_text, 'manifest must reference promote protocol', failures)
    require('promote_executor: tools/promote_executor.py' in manifest_text, 'manifest must reference promote executor', failures)

    for forbidden_dir in FORBIDDEN_DIRS:
        require(not (ROOT / forbidden_dir).exists(), f'forbidden legacy root dir exists: {forbidden_dir}/', failures)

    agents_manifest = read_text('agents/manifest.yaml') if path_exists('agents/manifest.yaml') else ''
    for agent_id in ('hermes', 'openclaw', 'future-agent'):
        require(f'id: {agent_id}' in agents_manifest, f'agents/manifest.yaml missing agent id: {agent_id}', failures)

    for agent_rel in ('agents/hermes/agent.yaml', 'agents/openclaw/agent.yaml', 'agents/future-agent/agent.yaml'):
        text = read_text(agent_rel) if path_exists(agent_rel) else ''
        require(contains_all(text, REQUIRED_AGENT_FIELDS), f'{agent_rel} missing required schema fields', failures)
        require('sandbox_path: sandbox/' in text, f'{agent_rel} must use sandbox/ path', failures)

    for agent_rel in ('agents/openclaw/agent.yaml', 'agents/future-agent/agent.yaml'):
        text = read_text(agent_rel) if path_exists(agent_rel) else ''
        require('direct_truth_write: false' in text, f'{agent_rel} must set direct_truth_write: false', failures)

    hermes_text = read_text('agents/hermes/agent.yaml') if path_exists('agents/hermes/agent.yaml') else ''
    require('role: orchestrator' in hermes_text, 'agents/hermes/agent.yaml must declare orchestrator role', failures)
    require('direct_truth_write: true' in hermes_text, 'agents/hermes/agent.yaml must keep mediated promote authority', failures)

    memory_text = read_text('truth/memory/MEMORY.md') if path_exists('truth/memory/MEMORY.md') else ''
    require('truth/' in memory_text, 'truth/memory/MEMORY.md should mention truth/ as source of truth', failures)
    require('truth/promote-logs/' in memory_text, 'truth/memory/MEMORY.md should mention promote logs', failures)

    policy_text = read_text('policy/write-rules.yaml') if path_exists('policy/write-rules.yaml') else ''
    require('truth_source: truth/' in policy_text, 'policy/write-rules.yaml must keep truth/ as truth source', failures)
    require('write_entry: sandbox/' in policy_text, 'policy/write-rules.yaml must keep sandbox/ as write entry', failures)
    require('default_direct_truth_write: false' in policy_text, 'policy/write-rules.yaml must default direct truth writes to false', failures)

    registry_text = read_text('registry/manifest.yaml') if path_exists('registry/manifest.yaml') else ''
    require('capabilities: registry/capabilities/manifest.yaml' in registry_text, 'registry/manifest.yaml must reference capability manifest index', failures)

    capability_index = read_text('registry/capabilities/manifest.yaml') if path_exists('registry/capabilities/manifest.yaml') else ''
    for agent_id in ('hermes', 'openclaw', 'future-agent'):
        require(f'agent_id: {agent_id}' in capability_index, f'capability index missing agent_id: {agent_id}', failures)
        require(f'file: registry/capabilities/{agent_id}.yaml' in capability_index, f'capability index missing file mapping for: {agent_id}', failures)

    for agent_id in ('hermes', 'openclaw', 'future-agent'):
        path = f'registry/capabilities/{agent_id}.yaml'
        text = read_text(path) if path_exists(path) else ''
        require(f'agent_id: {agent_id}' in text, f'{path} must declare agent_id: {agent_id}', failures)
        require(count_token(text, 'capability_id:') >= 1, f'{path} must declare at least one capability_id', failures)
        require('default_enabled: true' in text, f'{path} must include enabled capability records', failures)

    role_pairs = [
        ('agents/hermes/agent.yaml', 'registry/capabilities/hermes.yaml'),
        ('agents/openclaw/agent.yaml', 'registry/capabilities/openclaw.yaml'),
        ('agents/future-agent/agent.yaml', 'registry/capabilities/future-agent.yaml'),
    ]
    for agent_path, capability_path in role_pairs:
        agent_text = read_text(agent_path) if path_exists(agent_path) else ''
        capability_text = read_text(capability_path) if path_exists(capability_path) else ''
        agent_role = top_level_scalar(agent_text, 'role')
        capability_role = top_level_scalar(capability_text, 'role')
        require(agent_role == capability_role, f'role mismatch between {agent_path} and {capability_path}', failures)

    schema_text = read_text('schema/agent.schema.yaml') if path_exists('schema/agent.schema.yaml') else ''
    require('name: shared-hub-v3-agent-schema' in schema_text, 'schema/agent.schema.yaml must declare schema name', failures)
    require('worker_direct_truth_write_must_be_false: true' in schema_text, 'agent schema must enforce worker truth-write restriction', failures)
    require('sandbox_path_prefix: sandbox/' in schema_text, 'agent schema must require sandbox/ prefix', failures)

    protocol_text = read_text('protocol/promote-protocol.md') if path_exists('protocol/promote-protocol.md') else ''
    require(contains_all(protocol_text, ['## Trigger', '## Record-Format', '## Constraints']), 'promote protocol must include required sections', failures)
    require('只有 orchestrator 可以做最终 promote 决策。' in protocol_text, 'promote protocol must reserve final decision to orchestrator', failures)
    require('tools/promote_executor.py' in protocol_text, 'promote protocol must mention executor', failures)
    require('状态：stage3-executable' in protocol_text, 'promote protocol must declare stage3 executable status', failures)

    template_text = read_text('protocol/promote-log-template.md') if path_exists('protocol/promote-log-template.md') else ''
    require(template_text.startswith('---\n'), 'promote log template must start with YAML frontmatter', failures)
    require('\n---\n' in template_text, 'promote log template must contain closing YAML frontmatter fence', failures)
    for field in ('record_id:', 'submitter_agent:', 'source_path:', 'target_path:', 'decision:', 'executed_at:', 'source_sha256:', 'target_sha256:'):
        require(field in template_text, f'promote log template missing field: {field}', failures)

    executor_text = read_text('tools/promote_executor.py') if path_exists('tools/promote_executor.py') else ''
    require('CONTENT_KIND_TARGET_PREFIXES' in executor_text, 'promote executor must define content kind target prefixes', failures)
    require('SHARED-V3-PROMOTE-ENTRIES:START' in executor_text, 'promote executor must manage MEMORY markers', failures)

    verify_stage3_execution(failures)

    if failures:
        print('[shared-v3-verify] FAIL')
        for item in failures:
            print(f'- {item}')
        return 1

    print('[shared-v3-verify] PASS')
    print(f'- root: {ROOT}')
    print('- kernel: agents/ registry/ truth/ sandbox/')
    print('- stage3: approved promote executor + demo promote + audit log + MEMORY index')
    print('- worker direct truth writes: disabled')
    return 0


if __name__ == '__main__':
    sys.exit(main())
