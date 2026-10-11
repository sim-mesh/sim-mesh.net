---
title: Simulation
permalink: /simulation/
redirect_from:
  - /networks/
description: The firmware, antennas, geodata, nodes and scripts a simulation is made of, and how sim-mesh decides who hears whom.
---

A simulation is several things that change for different reasons, each its
own file so that changing one leaves the others alone: what the nodes run (a
**firmware**), what they transmit and hear with (an **antenna**), where they
are (**geodata**), the nodes on it (a **nodeset**), what they are told (a
**script**), and what follows from geodata and nodes, the **loss table**. The
chapters below follow the app's tabs.

## Firmware

What a node runs: a Linux build of real mesh firmware with a driver beside
it, added from a zip or from the pre-built list on the **Firmware** tab. A
nodeset never says what its nodes run; a script does, so one nodeset runs on
any firmware, or on a mix of them by tag. [Firmware]({{ '/using-firmware/' | relative_url }})
has the names, the categories, and how to build firmware for sim-mesh.

## Antennas

A node carries one antenna from the catalogue — a bare quarter-wave wire, a
spring helical, a fibreglass collinear, a panel, a yagi — each a pattern of
five figures: peak gain, vertical beamwidth, tilt, horizontal beamwidth for
a directional one, and a floor, the same on the sub-GHz bands (433, 868
and 915 MHz). Between two nodes the direction is the line
between their antenna tips in three dimensions, the earth's curvature taken
off, so a low node under a high collinear's narrow beam hears less of it than
one on the horizon, and a yagi hears what it faces. The **Antennas** tab
draws every pattern.

## Geodata

What nodes stand on, one directory each under `testbed/geodata/`, of
one of two kinds.

**Synthetic geodata** lies at 0°, 0°, its degrees metres by one fixed rule (a
nautical mile to the minute of arc), so a nodeset made on one synthetic
geodata stands on any other. A pair's loss is log-distance,
`FSPL(1 m, f) + 10·n·log10(d)`, with `n` 2 for free space, 2.7 suburban.

**A geodata pack** is compiled from public sources — terrain, clutter,
buildings, roads and places, in a UTM zone. A pair's loss on it is ITU-R
P.1812-8 over the real profile, and the map draws the pack's terrain, roads
and buildings with the notices of its sources. **Build** on the
**Geodata** tab makes one over a rectangle of the map, taking the best source
for each part of it:

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

A geodata goes from one machine to another as a zip, **Export zip** and
**Import zip**; a bare planner pack imports too. Nodes are never part of
the geodata: they belong to nodesets.

**Pre-built geodata packs** come from an **index**: one YAML file listing geodata
packs and nodesets, each by its sha256, so geodata meant for comparable tests
is the same bytes on every machine. sim-mesh's own index, `sim-mesh-examples`,
is at [sim-mesh.net/examples/index.yaml]({{ '/examples/index.yaml' | relative_url }}):
reference environments for comparing mesh protocols and firmware versions,
as well as for showing sim-mesh. Anyone
can publish another, a directory holding an `index.yaml` and its files, and
**Add index** lists it. The **Geodata** tab has three sections: the
installed geodata, each with its size, what the indexes offer under
**Download pre-built geodata packs**, and the build's sources with what each holds
in the cache.

## Nodes

Which nodes stand where — latitude, longitude, height above the ground — with
each one's maximum power at the antenna connector, its antenna, its tags, and
offsets: dB added to one pair's computed loss, where a measurement says the
model is wrong. A nodeset stands on any geodata whose extent holds one of its
nodes, and is listed on that geodata's **Nodes** tab: the checked ones
are on its map together, several can be saved or run as one, and a click
on one opens it to edit.

Every node is one board, an SX1262: at 22 dBm or below a bare chip, above it
(up to 27 dBm) an SX1262 behind a GC1109 front end, as a Heltec V4 is. A node
is told its board when its station starts.

**Importing** makes a nodeset of the nodes inside the geodata's extent from
the MeshCore map, a PotatoMesh instance, planner sites, a deployed-network
CSV, any CSV whose columns the dialog asks to be named, GeoJSON points, KML
placemarks, GPX waypoints or a Meshtastic node list, each node tagged with
its source. The Nodes tab's list says each nodeset's size, and below it
what the indexes offer; a nodeset from an index brings the geodata it is
made for.

## Scripts

A script is plain Python that says what each node runs and what is done to
it, run from the **Scripts** tab or with `sim run`. [Scripting]({{ '/simulation/scripting/' | relative_url }})
has the library, the commands and the scripts that come with sim-mesh.

## Simulations

The **Simulations** tab lists every simulation — running, paused, done or
ended — with its nodeset, geodata and script, its pace and time, how many of
its stations are up and its size on disk; **done** is one its script paused
when it was finished, **paused** one a person paused, and both resume.
Play, pause, stop and delete are icons on each row, and checkboxes choose
several rows for Stop, Pause and Delete at once. Clicking a running one
opens its live map, where the same edits as on the Nodes tab go to the
run's own copy of its nodeset.

### Who hears whom

You never draw links between nodes. Whether one node hears another is worked
out from the physics: how far apart they are, the terrain and buildings
between them, their antennas and power, and whatever else is transmitting at
the same moment. The level a frame arrives at is

```
L = P_tx + G_tx + G_rx − loss(tx → rx) − offset − 20·log10(f / f0)
```

the power it went out at, each antenna's gain toward the other end, the loss
table's figure for the pair and the nodeset's offset. A frame that arrives
below the signal-to-noise ratio its spreading factor needs — −7.5 dB at SF7,
down to −20 dB at SF12 — is not delivered at all; that is what "out of range"
means here. Every transmission overlapping a receiver's channel is
interference there, whatever its spreading factor, and each receiver rules
for itself, frame by frame, over every stretch of its air.

**The loss table** is every ordered pair's path loss for one nodeset on one
geodata in one band, derived and cached under a hash of exactly what it
depends on: the geodata and the nodes' positions and heights. Antennas and
offsets are layers put on it when the medium is given it, so changing them
never recomputes it. Every pair is computed, not only those strong enough to
carry a frame, because a pair far too weak to decode still adds to a
receiver's interference.

### Time

A run goes in **real time**, on the wall clock, or in **virtual time**: the
ether owns time and moves it only when every station is idle, so an hour of
a busy network costs what the stations' work costs, and a busy host slows a
run down instead of changing what happens in it. With the same seed, two
runs of one network put the same frames on the air at the same instants.
