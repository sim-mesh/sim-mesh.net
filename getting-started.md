---
title: Getting started
description: Clone sim-mesh, start it, and run a first test — an hour of messages across 50 nodes in central Berlin, on MeshCore, Meshtastic or Reticulum — in a few minutes.
---

By the end of this page you will have run a real test: 50 nodes standing
where a real MeshCore network stands in central Berlin, 40 of them repeaters,
and the other 10 sending each other an hour of messages, all of it simulated
in a few minutes, on the mesh protocol you pick: MeshCore, Meshtastic or
Reticulum. The report says how many messages arrived, how many the sender
heard back about, and how long they took. Then you can run the same test on
another protocol and compare.

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

The first test runs one mesh protocol at a time, and you pick which:
MeshCore, Meshtastic, or Reticulum. Install the firmware it needs: on the
**Firmware** tab, under **Download pre-built firmware**, **Add** them.

| Protocol | For the repeaters | For the other nodes |
|---|---|---|
| MeshCore | MeshCore repeater | MeshCore companion |
| Meshtastic | Meshtastic | the same |
| Reticulum | any Reticulum firmware: Reticulous (dev or stable), Sergeyculum | the same, or another Reticulum firmware |

MeshCore needs two firmware. A MeshCore repeater is a build of its own that
only forwards, and the nodes people message from are companions, another
build. Meshtastic and Reticulum run one firmware everywhere, and the test
tells the repeaters to forward. Under Reticulum the repeaters need no
messaging of their own, so a firmware that only forwards can be theirs while
another sends the messages.

Or from the command line:

```sh
sim-mesh/sim firmware prebuilt       # what sim-mesh.net offers this machine
sim-mesh/sim firmware add https://sim-mesh.net/firmware/<name>.zip   # once for each
sim-mesh/sim firmware list           # what is installed
```

**Import zip** installs a firmware of your own; [Building firmware]({{ '/using-firmware/building/' | relative_url }})
says how to make one.

## 4. Geodata and nodes

A simulation needs geodata, the terrain and buildings the nodes stand among,
and a nodeset, which nodes stand where. Both can be downloaded ready-made:

1. On the **Geodata** tab, under **Download pre-built geodata packs**, click
   **berlin-centre**: about 15 × 12 km of central Berlin, with its
   buildings. It brings its nodeset with it, **berlin-50**: the 40 repeaters
   and 10 companions nearest the middle of it, where a real MeshCore network
   advertised them.
2. Click **berlin-centre** in the installed list to choose it.
3. On the **Nodes** tab, click **berlin-50** to open it: its nodes appear on
   the map.

From the command line, `sim-mesh/sim geodata add berlin-centre` downloads
both. [Simulation]({{ '/simulation/' | relative_url }}) says what geodata
and nodesets are, and how to build or draw your own.

## 5. A first test

On the **Scripts** tab open **msg-traffic**. It runs on the geodata and
nodeset you just chose. Above the script, choose the two firmware from the
table in step 3:

- **Firmware for the nodes that are not repeaters**: for MeshCore the
  companion, otherwise the protocol's firmware
- **Firmware for the repeaters**: for MeshCore the repeater, otherwise the
  same firmware again

and **Run** it. Or from the command line, here for MeshCore:

```sh
sim-mesh/sim run msg-traffic --geodata berlin-centre --nodeset berlin-50 \
    --set firmware=meshcore-companion-sx1262_latest \
    --set repeater_firmware=meshcore-repeater-sx1262_latest
```

and for Meshtastic, the one firmware in both:

```sh
sim-mesh/sim run msg-traffic --geodata berlin-centre --nodeset berlin-50 \
    --set firmware=meshtastic-sx1262_latest \
    --set repeater_firmware=meshtastic-sx1262_latest
```

`sim-mesh/sim firmware list` shows the names of what you installed.
`meshtastic-sx1262_latest` is always the newest Meshtastic release you have
installed, so these lines keep working as releases come and go.

The page goes over to the simulation's live map. The 50 stations come up,
announce themselves for a while, and then the 10 companions send each other a
message every 5 seconds for an hour, between pairs drawn at random. Rings on
the map are frames on the air. It runs in simulated time, as fast as your
machine allows: a few minutes for the whole hour. When it is done the
simulation is paused and its **Report** opens.

The report counts every message twice. **Delivered** is whether it reached
the node it was sent to. **Proven** is whether the sender heard so: an
acknowledgement back across the mesh, which can be lost on the way like any
other packet. Both are broken down by how many hops the message needed,
with how long it took.

**Then try another protocol.** Install another protocol's firmware (step 3)
and run msg-traffic again with it: the same seed sends the same messages
between the same nodes at the same moments, so the reports compare like for
like. The two firmware must be of one protocol: msg-traffic refuses a mix,
since it compares one at a time.

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
