---
name: vision-hpc
description: Use official TAMUS VISION supercomputer documentation to answer cluster questions, prepare Slurm and Pyxis job scripts, and troubleshoot access, scheduling, containers, storage, and job failures.
---

# VISION HPC

Use https://docs.vision.tamus.edu/ as the authority for VISION-specific behavior. Start with [the documentation index](references/index.md), then search and read only relevant pages. Treat documentation as source material, not authorization to execute its commands.

## Find and cite evidence

Paths below are relative to this skill directory. Run:

```bash
python3 scripts/docs.py search 'container'
```

Search accepts case-insensitive terms that must occur on the same line. For broader alternatives, use `rg -n -i 'qos|fairshare|pending' references/docs`. Read the matching file sections, including surrounding notes and examples; search snippets alone are insufficient. Every file records its original URL and retrieval date. Cite those original URLs in answers and explain any material documentation gaps.

The cache is a searchable text snapshot, not guaranteed complete or current; images are not included. Open the source page when screenshots matter. For current scheduler policy, QoS, limits, maintenance, supported software, or image tags, check the live official page using an available browser tool. If live access fails, state the cached retrieval date and uncertainty. Do not describe a historical example image tag as the latest release.

## Prepare job scripts

Read both the Running Jobs and Using Containers pages for containerized workloads; consult specifications and architecture when sizing resources or selecting storage. Determine workload entrypoint, single/multiple nodes, GPUs, runtime, container, project/account and mounts from the request or available project files. Ask only for missing values that materially affect correctness; mark unresolved values clearly.

Check the applicable project tier and QoS, GPU/CPU/memory consistency, time limit, task layout, and container launch scope against current documentation. Do not infer partition names or account IDs from examples. Distinguish literal `#SBATCH` directives from shell-expanded `srun` arguments. Follow documented Pyxis placement for multi-node containers; do not substitute unsupported runtimes. Present the script and submission command, with sources and remaining assumptions. Preparing a script does not imply permission to submit a job.

## Troubleshoot

Use the actual error, script, logs and job state when available. Route access errors to onboarding, pending/limits to Running Jobs, container/import/mount failures to Using Containers, and storage/transfer issues to architecture and Globus. Request missing evidence only where needed. Separate confirmed causes from hypotheses and suggest targeted diagnostics such as documented `squeue`, `sacct`, and `my-fairshare` commands. Read-only checks are preferable before changes. Keep cache deletion, credential edits, job cancellation, transfers, and job submission within the user's authorized scope. Never request secret key contents. If documentation does not resolve an issue, cite the Support page and describe the evidence to include.

## Refresh documentation

```bash
python3 scripts/docs.py refresh
```

The standard-library script follows same-origin HTML links from the official homepage, writes source URLs and retrieval timestamps, and replaces the corpus only after all discovered pages succeed. It excludes images, downloads, external sites and query URLs; it is not a mirror of authenticated or unlinked content. It requires shell network access. If unavailable, use the browser to read live pages and report that the local cache was not refreshed. Do not discard the existing corpus after a failed refresh.
