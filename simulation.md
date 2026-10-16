---
title: Simulation
permalink: /simulation/
redirect_from:
  - /networks/
description: The firmware, antennas, geodata, nodes and scripts a simulation is made of, and how sim-mesh decides who hears whom.
---

A simulation is put together from separate pieces, so you can change one
without touching the others: the **firmware** the nodes run, the **antennas**
they use, the **geodata** they stand on, the **nodeset** that says where they
are, and the **script** that tells them what to do. From geodata and nodeset
sim-mesh computes the **loss table**: who can hear whom.

## Who hears whom

You never draw links between nodes. Whether one node hears another is worked
out from the physics: how far apart they are, the terrain and buildings
between them, their antennas and power, and whatever else is transmitting at
the same moment. The level a frame arrives at is

```
L = P_tx + G_tx + G_rx − loss(tx → rx) − offset − 20·log10(f / f0)
```

transmit power plus both antenna gains, minus the pair's path loss and
offset. A frame below the SNR its spreading factor needs (−7.5 dB at SF7 to
−20 dB at SF12) is lost: that is what "out of range" means here. Anything
else transmitting on the channel at the same time is interference, whatever
its spreading factor, and each receiver decides frame by frame whether it got
a clean copy.

**The loss table** holds the path loss for every pair of nodes on one
geodata. It depends only on the geodata and the nodes' positions and heights
and is cached by those, so changing antennas, power or offsets never
recomputes it. Every pair is computed, even ones far too weak to decode,
because they still add interference.

## Time

A run goes in **real time** or in **virtual time**. In virtual time the clock
advances only when every node is idle, so an hour of network takes as long as
the nodes' computation takes, and a slow or busy computer changes how long
the run takes, not what happens in it. Two runs with the same seed are
identical.

The sections below follow the app's tabs.

## Firmware

Real mesh firmware built for Linux, with its driver, installed from a zip or
from the pre-built list on the **Firmware** tab. Which firmware a node runs is
decided by the script, not the nodeset, so the same nodeset runs on any
firmware, or on a mix by tag. [Firmware]({{ '/using-firmware/' | relative_url }})
has the names, the categories, and how to build firmware for sim-mesh.

## Geodata

The terrain the nodes stand on. There are two kinds.

**Synthetic geodata** is a flat, featureless world at 0°, 0°, for quick
experiments. Loss between two nodes is log-distance: free space (n = 2) or
suburban (n = 2.7).

**A geodata pack** is a real area: terrain, buildings, land cover, roads and
places from public sources. Loss between two nodes is computed with ITU-R
P.1812 over the real terrain profile. **Build** on the **Geodata** tab makes
a pack for a rectangle you draw on the map, using the best source available
there:

| | Where | From |
|---|---|---|
| terrain and clutter | Berlin | its DGM1 and bDOM (1 m) |
| | Brandenburg | its DGM (1 m) and bDOM (0.2 m) |
| | Mecklenburg-Vorpommern | its DGM1 and DOM1 (1 m lidar) |
| | the Netherlands | AHN (0.5 m lidar) |
| | everywhere else | Copernicus GLO-30 |
| buildings | Berlin, Brandenburg, Mecklenburg-Vorpommern | their LoD2 models |
| | the Netherlands | 3DBAG |
| | everywhere else | OpenStreetMap |
| population | Germany | the Zensus 2022 grid |
| | the Netherlands | the CBS 2023 grid |
| land cover, roads, places | the world | ESA WorldCover, OpenStreetMap |

**Export zip** and **Import zip** move a pack between machines. Nodes are not
part of geodata; they live in nodesets.

**Pre-built geodata packs** come from an **index**, a YAML file listing packs
and nodesets with their checksums, so everyone comparing results works on
identical data. sim-mesh's own index is at
[sim-mesh.net/examples/index.yaml]({{ '/examples/index.yaml' | relative_url }}).
Anyone can publish their own: a directory with an `index.yaml` and the files;
**Add index** adds it to the tab.

## Nodes

A nodeset says where the nodes are (latitude, longitude, height above
ground), each with its maximum power, antenna and tags. You can add an offset
in dB to a pair's loss where a real measurement disagrees with the model. The
**Nodes** tab lists the nodesets that fit the chosen geodata; check several
to show them together, click one to edit it.

Every node is an SX1262 board; above 22 dBm (up to 27) it gets a power
amplifier like the one on a Heltec V4.

**Import** builds a nodeset from real-world data inside the geodata's area:
the MeshCore map, a PotatoMesh instance, a Meshtastic node list, CSV, GeoJSON,
KML or GPX.

## Antennas

Each node has one antenna from a catalogue: a quarter-wave wire, a spring
helical, a fibreglass collinear, a panel, a yagi. Each is described by peak
gain, beamwidths, tilt and a floor, the same for 433, 868 and 915 MHz. Gain
is applied along the actual 3D line between the two antennas, so a node right
below a tall collinear hears less of it than one far away on the horizon, and
a yagi hears what it points at. The **Antennas** tab draws the patterns.

## Scripts

A script is plain Python that says which firmware the nodes run and what
happens when, run from the **Scripts** tab or with `sim run`.
[Scripting]({{ '/simulation/scripting/' | relative_url }}) has the library,
the commands and the scripts that come with sim-mesh.

## Simulations

The **Simulations** tab lists every simulation with its nodeset, geodata,
script, speed, clock and size on disk. A **done** simulation is one its script
finished and paused; a **paused** one was paused by hand; both can resume.
Each row has play, pause, stop and delete. Click a running one for its live
map, where you can edit the nodes as on the Nodes tab; the changes go to the
run's own copy of the nodeset.

Each simulation is its own process. The front end serves the web UI, starts
simulations, computes loss tables, runs scripts and builds geodata:

<figure class="diagram">
<svg viewBox="0 0 960 330" role="img" aria-label="The browser reaches the front on localhost:8800. The front shows the web UI; the planner builds geodata packs; a script runner starts and drives a simd. A simd is one simulation: the ether, the stations and a proxy.">
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" class="head"/>
    </marker>
  </defs>
  <g class="links">
    <path d="M120,140 H218" marker-end="url(#arrow)"/>
    <path d="M400,118 H430 V58 H458" marker-end="url(#arrow)"/>
    <path d="M400,162 H430 V220 H458" marker-end="url(#arrow)"/>
    <path d="M640,220 H698" marker-end="url(#arrow)"/>
  </g>
  <text class="note" x="169" y="129">localhost:8800</text>

  <rect class="box" x="0" y="112" width="120" height="56" rx="8"/>
  <text class="name" x="60" y="146">browser</text>

  <rect class="box" x="220" y="102" width="180" height="76" rx="8"/>
  <text class="name" x="310" y="134">front</text>
  <text class="desc" x="310" y="158">shows the web UI</text>

  <rect class="box" x="460" y="20" width="320" height="76" rx="8"/>
  <text class="name" x="620" y="52">planner</text>
  <text class="desc" x="620" y="76">builds geodata packs from public sources</text>

  <rect class="box" x="460" y="182" width="180" height="76" rx="8"/>
  <text class="name" x="550" y="214">script runner</text>
  <text class="desc" x="550" y="238">runs one script</text>

  <rect class="box" x="700" y="120" width="260" height="200" rx="8"/>
  <text class="name" x="830" y="150">simd</text>
  <text class="desc" x="830" y="172">one simulation</text>
  <rect class="part" x="712" y="186" width="236" height="38" rx="6"/>
  <text class="desc strong left" x="724" y="210">ether</text>
  <text class="desc left" x="796" y="210">who hears what</text>
  <rect class="part" x="712" y="230" width="236" height="38" rx="6"/>
  <text class="desc strong left" x="724" y="254">stations</text>
  <text class="desc left" x="796" y="254">firmware processes</text>
  <rect class="part" x="712" y="274" width="236" height="38" rx="6"/>
  <text class="desc strong left" x="724" y="298">proxy</text>
  <text class="desc left" x="796" y="298">for station web UIs</text>
</svg>
</figure>
