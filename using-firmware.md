---
title: Firmware
permalink: /using-firmware/
description: How sim-mesh names, installs and deletes the firmware its stations run.
---

A station in the simulation runs **firmware**, which in the context of sim-mesh is

- an executable built for Linux
- whatever it needs beside it
- a Python module, called its **driver**, that tells sim-mesh how
to talk to it.

A firmware comes as a zip and is unpacked under `firmware/`. sim-mesh knows
nothing about any firmware beyond what its driver tells it.
[Building firmware for sim-mesh]({{ '/using-firmware/building/' | relative_url }}) details how to make your own software run in sim-mesh.

## Names

A firmware is called `<base>_<arch>_<version>`, and so is its zip, `.zip`
after it:

- **base** — lower-case letters, digits, `-` and `.`;
- **arch** — the architecture it runs on, as `uname -m` spells it
  (`aarch64`, `x86_64`);
- **version** — a build stamp, `YYYYMMDDhhmmss` in UTC, or a semantic version
  `1.2.3`; a base keeps to one of the two.

Builds that differ in anything sim-mesh can't see, such as which radio they
drive, get different base names; by convention the base ends in the radio,
like `relay-sx1262`. **`<base>_latest`** means the newest installed version
of that base.

## Categories

A firmware's **category** is its mesh protocol: `reticulum`, `meshcore` or
`meshtastic`. It decides which script commands the driver answers. Within a
category every firmware answers the same commands; across categories the
commands differ, following each protocol's own CLI, and the protocol-neutral
`message` and `announce` sit on top of all three. [Scripting]({{ '/simulation/scripting/' | relative_url }})
lists the commands, every firmware's and each category's.

## Adding, listing, deleting

On the **Firmware** tab: **Import zip**, **Download pre-built firmware** below
the installed list, and a trash can per firmware. Deleting one that a paused
simulation needs warns that it stops that simulation for good. The same from
the command line:

```sh
sim firmware add relay-sx1262_aarch64_20260930163128.zip
sim firmware add https://sim-mesh.net/firmware/<name>.zip
sim firmware prebuilt
sim firmware list [SUBSTRING]
sim firmware delete [-f] SUBSTRING        # lists what it would delete, then asks
```

A zip is refused if it is for another architecture, if its name is already
installed, if its base mixes version schemes, or if its `node.yaml` or a file
it names is missing. **A firmware that a paused run or snapshot uses can't be
deleted**: that state only resumes on the firmware that wrote it, so delete
the run or snapshot first.

## Pre-built firmware

[The pre-built firmware]({{ '/firmware/' | relative_url }}) is served from
this site, from the `firmware` release of the sim-mesh repository.
