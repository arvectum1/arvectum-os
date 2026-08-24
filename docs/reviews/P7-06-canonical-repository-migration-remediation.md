# P7.06 - Canonical Repository Identity Migration Remediation

Status: `Implementation repair / functional cross-review PASS / deployment pending`
Date: `2026-08-24`
Owner: `ООО «Арвектум»`
Task classification: `platform` with bounded operational governance

## Finding

`P9.11-F04 - Canonical repository migration blocked governed deployment`

An owner-operated P9.11.2 governed deployment from canonical checkout
`arvectum1/arvectum-os` at `885c4c5461453b9138580780f329861bb2fc2afd`
failed at P7.06 preflight. The controller admitted only the obsolete checkout
identity `arvectum/arvectum-os`.

Runtime before the attempt was exact release
`7dc7ceff986df41c1cd8be8668d51280c871e677`, Workspace `p9.11.1`, application
contract `10`. The immutable historical manifest truthfully records
`arvectum/arvectum-os`.

## Safety result

- no deployment occurred;
- the runtime remained `p9.11.1`;
- the P7.02 service remained healthy;
- the Workspace listener remained loopback-only at `127.0.0.1:8769`;
- no canonical mutation, product effect, or external effect occurred.

The fail-closed preflight behavior worked as intended; its admitted repository
identity was stale.

## Repair disposition

This bounded migration bridge distinguishes repository provenance by role:

- current checkout and every newly prepared target use only `arvectum1/arvectum-os`;
- `arvectum/arvectum-os` is admitted only for an already-installed historical
  source release and status inspection;
- legacy or arbitrary repository identities are rejected as targets;
- immutable historical manifests and retained evidence are not rewritten.

The repair changes deployment tooling only. Workspace remains `p9.11.2` with
internal application contract `11`; it is not deployed by this change. P9.11
remains Current, R32 remains locked, M9 remains open, and owner recheck remains
pending.

## Functional cross-review

Three iterations were sufficient for this bounded repair:

1. Operations/security found that an unanchored repository-host pattern could
   admit a lookalike host. The current checkout guards now enumerate only exact
   `github.com` HTTPS, credential-prefixed HTTPS, SSH, and `ssh://` forms.
2. Historical provenance/activation found that P7.06 admitted credential-prefixed
   HTTPS while the P7.02 install primitive did not. Both coupled guards now use
   the same exact-host forms, avoiding a post-stop activation failure.
3. Current-target integrity, rollback provenance, tests, and roadmap claims found
   no remaining material objection. Legacy manifests remain source/status-only;
   no deployment was performed.
