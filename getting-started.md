---
title: Getting started
description: Clone sim-mesh, start it, add firmware, and run a first simulation.
---

sim-mesh needs no firmware tree: stations are firmware zips, added from a
file or from the [pre-built ones]({{ '/firmware/' | relative_url }}).

It needs **Docker or Podman** and nothing else, on Linux, a Mac or Windows:
`sim` builds its own image on first use (a few minutes, once) and runs
everything inside it, with port 8800 published.

## 1. Clone it

As you can see below, we're creating a new directory and clone into it. That intermediary directory you clone into is the one `sim` mounts into its Docker/podman container. This allows optional firmware images later cloned/built next to sim-mesh to build against its radio.

```sh
mkdir mesh && cd mesh
git clone https://github.com/sim-mesh/sim-mesh.git
```

## 2. Start it

```sh
sim-mesh/sim
```

It builds whichever of the page, the virtual radios and the planner is not
built yet or is older than its sources. So the first time this may take several minutes. Then it starts the server and opens `http://localhost:8800/` in your default browser to show the UI. The terminal window itself shows events and errors: Ctrl-C there stops every simulation and everything they started.

`sim run <script> [...]` runs a script instead, by its name on the Scripts tab or as a path to a .py file. If the sim-mesh server isn't already running, it starts it in the background first, and opens the page on the run.

## 3. Add firmware

On the **Firmware** tab, **Download pre-built firmware** lists what this site
offers for your machine's architecture and **Add** installs one; **Import
zip** installs a zip of your own. Or from the command line:

```sh
sim-mesh/sim firmware prebuilt       # list what sim-mesh.net offers this machine
sim-mesh/sim firmware add <a zip, or its URL>
sim-mesh/sim firmware list           # show list of installed firmware
```

For the purposes of showing something quickly, let's run some reticulum software. Install "Reticulous" ESP32 firmware and "Sergeyculum" nRF firmware. 

## 4. Geodata and nodes

Geodata and nodesets can be fetched from an index or made locally. On the
**Geodata** tab, **Download pre-built geodata packs** lists what sim-mesh's own
index and any you add offer, and a click on one installs it; or make geodata packs —
**Build** over a rectangle of the map, or **New synthetic** — and click it
to choose it. The **Nodes** tab lists the nodesets on it beside a map of
them: **New** one and place nodes on it, **Import** them from a public node
map or a file, or fetch one under **Download pre-built nodesets**; a click
on a nodeset opens it to edit. [Simulation]({{ '/simulation/' | relative_url }})
says what each of those is.

For the purposes of the demonstration, install the 'berlin-centre' example provided.

## 5. A first simulation

On the **Scripts** tab open `lxmf-traffic`, choose the firmware its nodes
run in **Firmware for nodes not otherwise configured** above the script, and
**Run** it: a new simulation of the nodeset on that geodata, in virtual time.
The page goes over to the simulation's live map and its stations come up;
rings on the map are frames on the air. When it is done the simulation is
paused and its **Report** says how much of an hour of messages arrived.

For a simulation to work with by hand, run `realtime`: every node on the
chosen firmware, on the wall clock, set up and left running.

## 6. Play with it

- **Click a station** for its editor, its **Console** (its serial console)
  and **Web UI** (its own web interface, for a firmware that serves one).
- **Right-click the map ▸ New node here** puts down a station. It comes up
  and is set up on its own.
- **Drag a station** and its links change once its row of the loss table is
  recomputed.
- **Right-click a station ▸ Run command…** types one line at the selected
  stations, in their firmware's own language.
- **Pause** on the simulation's row of the Simulations tab stops it with its
  state kept; **Resume** (▶) starts it again as it ended, in real time, and
  a script run on a paused one resumes it in the script's own time.
  **Stop** ends a simulation for good, a paused one's state deleted.
- **⋯ ▸ Save snapshot as…** keeps the network and everything its stations
  have become, and **⋯ ▸ Load snapshot into it…** brings one back.
