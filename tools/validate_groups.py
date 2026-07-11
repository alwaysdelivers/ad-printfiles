#!/usr/bin/env python3
"""
validate_groups.py -- enforces the AlwaysDelivers prefix->group invariant.

Rules enforced:
  1. Every prefix in catalog.json MUST have a non-empty `groups` array.
  2. Every group a prefix references MUST exist in the top-level `groups` registry.
  3. The `groups` registry entries MUST each have `label`, `order`, and `status`.

Explicitly NOT an error:
  - A registered group with zero member prefixes. Empty groups are intentional
    plumbing placeholders for prefixes that will be built later (e.g. Holidays,
    Military). They are reported as INFO, not failures.

Usage:
    python3 validate_groups.py [path/to/catalog.json]
Exit code 0 = pass, 1 = fail. Safe to wire into CI / pre-ship checks.
"""
import json, sys

def validate(path='catalog.json'):
    with open(path) as f:
        c = json.load(f)

    errors = []
    info = []

    registry = c.get('groups')
    if not isinstance(registry, dict) or not registry:
        errors.append("Top-level `groups` registry is missing or empty.")
        registry = {}

    # Rule 3: registry entries well-formed
    for gkey, gval in registry.items():
        for req in ('label', 'order', 'status'):
            if req not in gval:
                errors.append(f"Group '{gkey}' registry entry missing '{req}'.")

    valid_group_keys = set(registry.keys())
    prefixes = c.get('prefixes', {})

    # Rules 1 & 2: every prefix has valid, non-empty groups
    for pname, pdata in prefixes.items():
        gs = pdata.get('groups')
        if not gs or not isinstance(gs, list):
            errors.append(f"Prefix '{pname}' has no `groups` array (or it is empty). "
                          f"Every prefix MUST belong to at least one group.")
            continue
        for g in gs:
            if g not in valid_group_keys:
                errors.append(f"Prefix '{pname}' references unknown group '{g}'. "
                              f"Add it to the `groups` registry or fix the typo.")

    # INFO: empty groups (allowed, but surfaced)
    membership = {g: [] for g in valid_group_keys}
    for pname, pdata in prefixes.items():
        for g in (pdata.get('groups') or []):
            if g in membership:
                membership[g].append(pname)
    for g, members in sorted(membership.items(),
                             key=lambda x: registry.get(x[0], {}).get('order', 999)):
        tag = 'INFO(empty placeholder)' if not members else ''
        print(f"  {registry.get(g,{}).get('label',g):20} [{g}] "
              f"{len(members)} member(s) {tag}")

    print()
    if errors:
        print(f"VALIDATION FAILED -- {len(errors)} error(s):")
        for e in errors:
            print(f"  ✗ {e}")
        return 1
    print(f"VALIDATION PASSED -- {len(prefixes)} prefixes, "
          f"{len(registry)} groups, every prefix has valid group membership.")
    return 0

if __name__ == '__main__':
    path = sys.argv[1] if len(sys.argv) > 1 else 'catalog.json'
    sys.exit(validate(path))
