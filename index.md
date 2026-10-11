---
title: Home
hero:
  - Radio propagation & coverage planning
  - Run real mesh firmware in virtual ether
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

**sim-mesh** is a LoRa testbed. Its stations are real firmware, built for
Linux and run as ordinary processes, each on its own loopback address; below
their radio driver sits a model of the radio chip on a virtual SPI bus, and
between the models sits one medium, the **ether**, which decides who hears
what from a table of every pair's path loss over real-world or synthetic terrain. A
map in the browser places the nodes and shows every frame on the air. It is
the firmware under test, built for a different target — not an emulator.

A run goes in **real time**, for working with stations by hand, or in
**virtual time**, as fast as the stations can compute: an hour of a busy
network in seconds, the same frames at the same instants in every run of one
seed.

<ul class="cards">
<li><a href="{{ '/getting-started/' | relative_url }}"><b>Get started</b><span>Clone, start, add firmware, run a script. Docker or Podman is all it needs.</span></a></li>
<li><a href="{{ '/firmware/' | relative_url }}"><b>Pre-built firmware</b><span>Station builds ready to add, for aarch64 and x86_64.</span></a></li>
<li><a href="{{ '/using-firmware/building/' | relative_url }}"><b>Bring your firmware</b><span>The zip, its driver, the ether's protocol and the virtual radio, specified.</span></a></li>
</ul>

## What it is made of

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

One simulation is one `simd`; the **front** shows the web UI, runs several
simulations behind one port, computes their loss tables, runs scripts against
them and builds geodata packs from public data. Around them are the things sim-mesh keeps:

- **firmware** — station builds, each a zip with its own driver, installed
  from a file or from [the pre-built ones]({{ '/firmware/' | relative_url }});
- **geodata** — a geodata pack fetched pre-built from an index or built from public sources, or synthetic geodata;
- **nodesets** — which nodes stand where, with what antenna and power;
- **scripts** — plain Python that says what each node runs and what is done;
- **runs** and **snapshots** — what a simulation did, and moments of it to
  start again from.

sim-mesh holds nothing of any one firmware project. A firmware tells sim-mesh
how to talk to it through its **driver**, a Python module in its own zip, and
a script asks for the same things — an announce, a message, a path — of every
firmware of a category. There are three categories: Reticulum, MeshCore
(companions, repeaters and room servers) and Meshtastic.

sim-mesh can run in real time, so you can play with a live network as it
happens, or in simulated time, either as fast as your computer allows or at a
speed you choose. In simulated time your firmware sees a clock that only moves
forward once every node is done, so a day of network activity can take
minutes. A slow or busy computer makes the run take longer, but doesn't change
what happens in it. Runs can be reproducible: given the same random seed, a
simulated-time run plays out identically, which makes bugs much easier to
chase down. You
can also save a run at any moment and pick it up again later.
