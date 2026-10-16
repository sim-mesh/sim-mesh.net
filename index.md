---
title: Home
hero:
  - Plan LoRa coverage on real terrain
  - Run real mesh firmware on a virtual radio
hero_sub:
  - Try locations, plan networks, script scenarios, compare mesh protocol performance
  - Free (Apache 2.0), uses public geodata
hero_shots:
  - name: antennas
    alt: "The Antennas tab: an antenna's horizontal and vertical radiation patterns"
  - name: nodes
    alt: "The Nodes tab: a node's coverage over Berlin, a link's terrain profile, and the node's radio and antenna settings"
  - name: geodata
    alt: "The Geodata tab: installed geodata packs, and pre-built ones to download"
  - name: geodata2
    alt: "The Geodata tab: the public sources packs are built from, and where one has data"
  - name: scripts
    alt: "The Scripts tab: a traffic script in the editor"
  - name: report
    alt: "A run's report: message delivery, latency and ETSI duty-cycle compliance"
description: >-
  sim-mesh runs real LoRa mesh firmware, built as Linux processes, over a
  model of the radio chip and one medium that decides who hears what from the
  geodata they stand on, in real time or in virtual time.
---

**sim-mesh** runs real LoRa mesh firmware (MeshCore, Meshtastic, Reticulum) on
your computer, dozens of nodes at once, over simulated radio. Each node is the
actual firmware compiled for Linux. Instead of a radio chip it talks to a model
of one, and a shared medium, the **ether**, decides who hears whom from the
terrain and buildings between them. You place the nodes on a map in your
browser and watch every frame go out.

<ul class="cards">
<li><a href="{{ '/getting-started/' | relative_url }}"><b>Get started</b><span>Clone, start, add firmware, run a script. Docker or Podman is all it needs.</span></a></li>
<li><a href="{{ '/firmware/' | relative_url }}"><b>Pre-built firmware</b><span>Station builds ready to add, for aarch64 and x86_64.</span></a></li>
<li><a href="{{ '/using-firmware/building/' | relative_url }}"><b>Bring your own firmware</b><span>How to build a firmware so sim-mesh can run it.</span></a></li>
</ul>

## What it is made of

What sim-mesh stores:

- **firmware** — the mesh firmware the nodes run, as zips,
  [pre-built]({{ '/firmware/' | relative_url }}) or your own;
- **geodata** — terrain and buildings for an area, downloaded ready-made or
  built from public sources;
- **nodesets** — which nodes stand where, with what antenna and power;
- **scripts** — Python that says which firmware the nodes run and what
  happens when;
- **runs** and **snapshots** — what happened, and saved states to continue
  from.

sim-mesh knows nothing about any particular firmware. Each firmware zip brings
a small Python **driver** that translates between sim-mesh and the firmware,
so a script can say "send a message" and have it mean the same thing on
Reticulum, MeshCore or Meshtastic.

sim-mesh can run in real time, so you can play with a live network as it
happens, or in simulated time, either as fast as your computer allows or at a
speed you choose. In simulated time your firmware sees a clock that only moves
forward once every node is done, so a day of network activity can take
minutes. A slow or busy computer makes the run take longer, but doesn't change
what happens in it. Runs can be reproducible: given the same random seed, a
simulated-time run plays out identically, which makes bugs much easier to
chase down. You can also save a run at any moment and pick it up again later.
