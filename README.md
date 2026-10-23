# VISION skills for Codex

Reusable Codex skills for working with the [TAMUS VISION supercomputer](https://docs.vision.tamus.edu/).

The `vision-hpc` skill searches official documentation, cites its sources, helps prepare Slurm and Pyxis job scripts, and supports troubleshooting cluster access, scheduling, containers, storage, and job failures.

The [official VISION documentation](https://docs.vision.tamus.edu/) remains the authority for cluster policy and configuration.

## Install

Clone this repository and link the skill into Codex's personal skills directory, `~/.agents/skills`. Run these commands in your terminal:

```bash
git clone https://github.com/DLFundamentals/VISION-skills.git
mkdir -p "$HOME/.agents/skills"
ln -s "$PWD/VISION-skills/skills/vision-hpc" "$HOME/.agents/skills/vision-hpc"
```

If you already cloned the repository, run only the `mkdir` and `ln` commands from its parent directory, or substitute the absolute path to your checkout in the `ln` command. Keep the checkout in place: the link points to it.

These commands assume `~/.agents/skills/vision-hpc` does not already exist. Inspect an existing installation before replacing it.

Restart Codex if the skill does not appear, then type `$vision-hpc` or open `/skills` to select it. The required layout is `~/.agents/skills/vision-hpc/SKILL.md`; placing the folder directly inside `~/.agents` does not install it. See the [official skill discovery guidance](https://learn.chatgpt.com/docs/build-skills).

Alternatively, ask Codex to install from GitHub:

```text
Use $skill-installer to install vision-hpc from
https://github.com/DLFundamentals/VISION-skills/tree/main/skills/vision-hpc
into ~/.agents/skills.
```

The installer creates a separate copy. Use either the linked checkout or the installer approach to avoid duplicate installations.

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
python3 "$HOME/.agents/skills/vision-hpc/scripts/docs.py" search 'fairshare'
python3 "$HOME/.agents/skills/vision-hpc/scripts/docs.py" refresh
```

Search is case-insensitive; all query terms must occur on the same line. Read surrounding sections before relying on a match. Each cached page records its source URL and retrieval date.

Refresh follows same-origin HTML links from the official homepage and replaces the existing corpus only after every discovered page succeeds. It excludes external sites, images, downloads, and query URLs. A successful refresh also writes `references/docs/manifest.json` recording coverage and timestamps. A failed download preserves the previous cache. The default limit is 150 pages; use `refresh --max-pages NUMBER` if the site grows beyond that limit.

The initial snapshot covers ten pages linked in the homepage navigation and was retrieved on October 23, 2026. Text extraction excludes image contents and may omit formatting or other page details. It is not a complete archive of unlinked or authenticated material. Check live official pages for current scheduler limits, QoS policy, maintenance, supported software, and container tags.

## License and documentation attribution

Original skill instructions, metadata, index, and Python code are provided under the [MIT license](LICENSE).

Files in `skills/vision-hpc/references/docs/` contain text extracted from the official VISION documentation and are excluded from this project's MIT license. The source pages identify Texas A&M University System as the copyright holder. Their original rights and any applicable terms remain in effect; inclusion here does not grant additional redistribution rights. Source URLs and retrieval dates are retained in the cached files. See the [official documentation](https://docs.vision.tamus.edu/) for authoritative content.
