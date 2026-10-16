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

You don't need to build any firmware: the nodes run
[pre-built firmware]({{ '/firmware/' | relative_url }}) you download from
inside sim-mesh.

You need **Docker or Podman**, nothing else, on Linux, Mac or Windows. On
first start it pulls a 50 MB image and runs everything inside it. On Linux,
`sim-mesh/sim install` runs it directly, without a container.

## 1. Clone it

Clone sim-mesh into a directory of its own. `sim` mounts that directory into
the container, so any firmware you optionally build later can live next to
sim-mesh and link against its radio library.

```sh
mkdir mesh && cd mesh
git clone https://github.com/sim-mesh/sim-mesh.git
```

## 2. Start it

```sh
sim-mesh/sim
```

The first start pulls the image and downloads the pre-built parts, a minute
or so. Then it opens `http://localhost:8800/` in your browser. The terminal
shows events and errors; Ctrl-C there stops everything.

## 3. Add firmware

Pick a protocol: MeshCore, Meshtastic or Reticulum. On the **Firmware** tab,
under **Download pre-built firmware**, add what it needs:

| Protocol | For the repeaters | For the other nodes |
|---|---|---|
| MeshCore | MeshCore repeater | MeshCore companion |
| Meshtastic | Meshtastic | the same |
| Reticulum | any Reticulum firmware: Reticulous (dev or stable), Sergeyculum | the same, or another Reticulum firmware |

MeshCore has separate builds for repeaters and for companions (the nodes
people message from), so it needs both. Meshtastic and Reticulum use one
firmware for everything.

Or from the command line:

```sh
sim-mesh/sim firmware prebuilt       # what sim-mesh.net offers pre-built for your CPU architecture
sim-mesh/sim firmware add https://sim-mesh.net/firmware/<name>.zip   # once for each
sim-mesh/sim firmware list           # what is installed
```

**Import zip** installs a firmware of your own; [Building firmware]({{ '/using-firmware/building/' | relative_url }})
details what it takes to make one.

## 4. Geodata and nodes

A simulation needs geodata (the terrain and buildings) and a nodeset (where
the nodes are). Download both ready-made:

1. On the **Geodata** tab, under **Download pre-built geodata packs**, click
   **berlin-centre**: 15 × 12 km of central Berlin with its buildings. It
   comes with the nodeset **berlin-50**: 40 repeaters and 10 companions,
   placed where some past iteration of the real Berlin MeshCore network had
   them.
2. Click **berlin-centre** in the installed list to choose it.
3. On the **Nodes** tab, click **berlin-50** to open it: its nodes appear on
   the map.

From the command line, `sim-mesh/sim geodata add berlin-centre` downloads
both. [Simulation]({{ '/simulation/' | relative_url }}) details what geodata
and nodesets are, and how to build or draw your own.

## 5. A first test

On the **Scripts** tab open **msg-traffic**. Above the script, pick the
firmware from step 3:

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

`_latest` means the newest installed version of that firmware.
`sim-mesh/sim firmware list` shows the exact names. If the sim-mesh server
isn't running yet, `sim run` starts it in the background first.

The page switches to the live map. The 50 nodes boot and announce themselves,
then for an hour the 10 companions send each other a message every 5 seconds,
between random pairs. The rings on the map are transmissions. Depending on
the speed of your computer, the hour takes a few minutes of real time. When
it's done the simulation pauses and the **Report** opens.

The report gives two numbers for each message. **Delivered**: it reached the
recipient. **Proven**: the sender got an acknowledgement back, which can get
lost on the way like anything else. Both are broken down by hop count and by
how long it took.

**Then try another protocol.** Install another protocol's firmware (step 3)
and run msg-traffic again: the same seed sends the same messages between the
same nodes at the same moments, so the two reports compare directly. (Both
firmware must be of the same protocol.)

To play with a network by hand instead, run the **realtime** script: it
brings every node up on the chosen firmware and leaves it running in real
time.

## 6. Play with it

- **Click a station** for its editor, its **Console** (its serial console)
  and **Web UI** (its own web interface, for a firmware that serves one).
- **Right-click the map ▸ New node here** puts down a station. It comes up
  and is set up on its own.
- **Drag a station** to move it; its links update after a moment.
- **Right-click a station ▸ Run command…** sends a command to the selected
  stations' consoles.
- On the **Simulations** tab, **Pause** freezes a simulation, **Resume** (▶)
  continues it in real time, and **Stop** ends it and deletes its state.
  Running a script on a paused simulation resumes it under that script.
- **⋯ ▸ Save snapshot as…** saves the whole network state; **⋯ ▸ Load
  snapshot into it…** restores one.
