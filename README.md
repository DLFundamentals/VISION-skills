# VISION skills for Codex

Reusable Codex skills for working with the [TAMUS VISION supercomputer](https://docs.vision.tamus.edu/).

The `vision-hpc` skill searches official documentation, cites its sources, helps prepare Slurm and Pyxis job scripts, and supports troubleshooting cluster access, scheduling, containers, storage, and job failures.

This is a community-maintained project, not an official TAMUS support service. The [official VISION documentation](https://docs.vision.tamus.edu/) remains the authority for cluster policy and configuration.

## Install

In Codex, ask:

```text
Use $skill-installer to install vision-hpc from
https://github.com/DLFundamentals/VISION-skills/tree/main/skills/vision-hpc
```

Alternatively, clone this repository and copy the skill into your personal skills directory:

```bash
git clone https://github.com/DLFundamentals/VISION-skills.git
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R VISION-skills/skills/vision-hpc "${CODEX_HOME:-$HOME/.codex}/skills/"
```

These commands assume `vision-hpc` is not already installed. For an existing installation, review and replace or merge the installed folder deliberately. If the skill does not appear immediately, start a new Codex session.

## Requirements

- Codex with skill support.
- Python 3.6 or later for the search and refresh helper; it uses only the standard library.
- Network access from Python to refresh the local documentation. An available browser tool lets Codex check live source pages independently.
- Optional: `rg` (ripgrep) for broader searches.

Documentation search works from the bundled snapshot without network access. The skill does not grant a VISION account, cluster access, or permission to submit jobs.

## Use

Invoke the skill explicitly with `$vision-hpc`, for example:

```text
Use $vision-hpc to prepare a single-node, one-GPU PyTorch job for VISION.
My training entrypoint is train.py, and I need two hours. Ask for any
missing account, container, or mount details.
```

```text
Use $vision-hpc to troubleshoot this pending Slurm job. Here is my job
script and the output of squeue --me: ...
```

```text
Use $vision-hpc to explain how to mount my project directory in a Pyxis
container, citing the official documentation.
```

The skill can also be selected automatically for relevant VISION requests. Job preparation and troubleshooting do not automatically submit, cancel, or modify jobs.

## Search and refresh documentation

From the repository root:

```bash
python3 skills/vision-hpc/scripts/docs.py search 'container-image'
python3 skills/vision-hpc/scripts/docs.py refresh
```

For an installed copy:

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/vision-hpc/scripts/docs.py" search 'fairshare'
python3 "${CODEX_HOME:-$HOME/.codex}/skills/vision-hpc/scripts/docs.py" refresh
```

Search is case-insensitive; all query terms must occur on the same line. Read surrounding sections before relying on a match. Each cached page records its source URL and retrieval date.

Refresh follows same-origin HTML links from the official homepage and replaces the existing corpus only after every discovered page succeeds. It excludes external sites, images, downloads, and query URLs. A successful refresh also writes `references/docs/manifest.json` recording coverage and timestamps. A failed download preserves the previous cache. The default limit is 150 pages; use `refresh --max-pages NUMBER` if the site grows beyond that limit.

The initial snapshot covers ten pages linked in the homepage navigation and was retrieved on October 23, 2026. Text extraction excludes image contents and may omit formatting or other page details. It is not a complete archive of unlinked or authenticated material. Check live official pages for current scheduler limits, QoS policy, maintenance, supported software, and container tags.

## Updates and contributions

Updating the skill and refreshing its documentation are separate operations:

- Use `git pull` in your repository checkout to obtain changes to instructions and scripts, then update your installed copy. An installed copy does not automatically track the checkout.
- Run the refresh command to update documentation in whichever copy you invoke. Refreshing the checkout does not refresh a separate installed copy.

Contributions through issues and pull requests are welcome. Include the relevant official documentation URL when proposing changes to cluster-specific guidance. Keep credentials, private keys, and personal job data out of contributions.

## License and documentation attribution

Original skill instructions, metadata, index, and Python code are provided under the [MIT license](LICENSE).

Files in `skills/vision-hpc/references/docs/` contain text extracted from the official VISION documentation and are excluded from this project's MIT license. The source pages identify Texas A&M University System as the copyright holder. Their original rights and any applicable terms remain in effect; inclusion here does not grant additional redistribution rights. Source URLs and retrieval dates are retained in the cached files. See the [official documentation](https://docs.vision.tamus.edu/) for authoritative content.
