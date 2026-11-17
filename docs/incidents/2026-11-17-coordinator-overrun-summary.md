# Incident: Coordinator overrun during read-only CAD familiarization

**Date:** 2026-11-17. **Status:** stopped by user before final report.

## User task

Inspect the supplied `external-cad-input-package.zip`, start with `00_CAD_AGENT_BRIEF.md`, understand the existing construction, internal element purposes, and fit with visual references. Do not model or modify anything; report and stop.

## Corrected export statistics

Parsed from the source 771-line execution trace (not published; 250,583 text characters):

- 24 tool calls total.
- 17 `execute_python_mcp_freecad`.
- 5 `read_file` calls — all failed with path/permission/skill-path errors.
- 2 `get_output_page_mcp_freecad`.
- 0 `subagent` calls.
- 24 reasoning blocks, 55,668 characters / ~10,397 words.
- Tool argument text: 10,658 characters.
- Tool output JSON text: 145,317 characters; extracted page/stdout text: 63,417 characters.
- Sum of tool execution durations: ~47.1 seconds; sum of preparation durations: ~17.8 seconds.
- Three longest FreeCAD calls: ~15.0 s, ~15.0 s and ~8.6 s, producing large section/grid output.

An earlier summary incorrectly reported 26 total calls and 19 FreeCAD MCP calls. Parsing the source trace established 24 and 17 respectively. The raw trace is not included in this public repository.

## What happened

1. Coordinator checked active document and searched ``<CAD_WORKSPACE>``, `<CAD_WORKSPACE>`, `/mnt/data`, `/mnt/user-data`.
2. It attempted `read_file` with a bare filename; the tool rejected the path format.
3. It ran a broad filesystem walk looking for archives.
4. After user said the archive was attached, it still continued path-searching before finding `<FREECAD_CONFIG_ROOT>/Desktop/external-cad-input-package.zip`.
5. It listed ZIP entries and read `00_CAD_AGENT_BRIEF.md` and README using `zipfile` from FreeCAD Python.
6. It extracted CAD files and images to `<TEMP_DIR>/cad-audit`.
7. It repeatedly tried `read_file` on `<TEMP_DIR>`, `/mnt/data` and `<FREECAD_CONFIG_ROOT>/Desktop` paths; all five calls failed.
8. It decided not to delegate to Analyst, reasoning that the subagent probably had the same image limitation. This was an untested assumption.
9. It inspected STEP geometry through `Part.read`, bounding boxes, face lists, point-in-solid grids and ASCII cross-sections.
10. It generated repeated speculative hypotheses about battery/electronics bays, board guides, switch holes, USB-C opening, cable path and retention tabs.
11. It did not produce the requested report and was still investigating another notch when the user stopped it.

## Useful technical facts extracted before stop

- ZIP contained a brief, README, engineering constraints, main assembly STEP, a separate three-button overlay STEP, a DSA 1u keycap STEP, CAD view images, physical prototype photo and design renders.
- Main assembly STEP was read; the shape contained two solids (frame and overlay).
- Overlay standalone STEP and assembly instance matched after translation approximately `(+6.7, -4.65, 0)`; boolean cut volumes were zero in both directions.
- The source trace says the local working copy `Сборка.stp` and ZIP copy had zero difference by bidirectional cut-volume check.
- Images were extracted but never visually inspected.
- No source CAD file modifications or saves are visible in the export. Temporary extracted images were written under `<TEMP_DIR>/cad-audit/img`.

## What was wrong

- No Analyst delegation despite unknown geometry and explicit v3 routing rule.
- Repeated attempts to use an incompatible file-reading tool after failures.
- No hard stop after image access was found unavailable.
- Too much fine-grained geometry exploration without a bounded plan or stopping criteria.
- Repeated hypotheses and contradictory measurements were not consolidated into a structured fact/hypothesis register.
- Large ASCII grids and verbose reasoning inflated context and likely contributed to the reported ~100 RUB spend.
- No final report; no explicit blocker summary.

## Cost evidence limitation

The user reported stopping after approximately 100 RUB of reasoning. The execution trace did not include billed token counts, model billing rate or a provider usage ledger. Exact cost attribution cannot be established from the preserved aggregate evidence alone.

## Corrective questions for later work (not applied)

- Was `subagent` present in Coordinator runtime at the time? The export contains no call, but does not prove tool unavailability.
- What exact current v3 prompt was loaded? `coordinator-v3.md` is preserved and its hash matches the later report, but live runtime state was not read during this archive build.
- Why did Coordinator not follow the explicit rule to delegate unknown geometry to Analyst?
- What is the intended file/image inspection pathway from an agent with FreeCAD MCP but no `read_file` access?
- What stopping/budget limits should govern tool retries, geometry sampling and output paging?
