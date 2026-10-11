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

A firmware arrives as a zip and is installed under `firmware/`, unpacked into a 
directory of the zip's own name. sim-mesh holds nothing of any one firmware project:
it only knows how to talk to its driver.
[Building firmware for sim-mesh]({{ '/using-firmware/building/' | relative_url }}) details how to make your own software run in sim-mesh.

## Names

A firmware is called `<base>_<arch>_<version>`, and so is its zip, `.zip`
after it:

- **base** — lower-case letters, digits, `-` and `.`;
- **arch** — the architecture it runs on, as `uname -m` spells it
  (`aarch64`, `x86_64`);
- **version** — a build stamp, `YYYYMMDDhhmmss` in UTC, or a semantic version
  `1.2.3`; a base keeps to one of the two.

Two builds that differ in anything sim-mesh does not read — the radio they
drive among it — are two bases, and by custom the base names the radio:
`relay-sx1262`. **`<base>_latest`** is shorthand for the newest installed firmware with that base name for this server's architecture.

## Categories

A firmware's **category** says what kind of mesh its stations make, and so
which commands its driver answers: currently implemented categories are `reticulum`,
`meshcore` and `meshtastic`. A script command means the same thing on every firmware of a
category — an announce, a message, a path — and each driver does it its
own way. The categories' commands are not alike: MeshCore's carry
meshcore-cli's names and meanings, Meshtastic's the Meshtastic CLI's, and
comparing across protocols is a layer above them. [Scripting]({{ '/simulation/scripting/' | relative_url }})
lists the commands, every firmware's and each category's.

## Adding, listing, deleting

On the **Firmware** tab: **Import zip**, **Download pre-built firmware** below
the installed list, and a trash can per firmware. Deleting one that a paused
simulation needs warns that it stops that simulation for good. The `sim` command will let you do all these things from teh command line also:

```sh
sim firmware add relay-sx1262_aarch64_20260930163128.zip
sim firmware add https://sim-mesh.net/firmware/<name>.zip
sim firmware prebuilt
sim firmware list [SUBSTRING]
sim firmware delete [-f] SUBSTRING        # lists what it would delete, then asks
```

A zip is refused when it is built for another architecture, when its base
already holds firmware versioned the other way, when a firmware of its name
is installed already, or when its `node.yaml` or anything it names is
missing. **Deleting is refused for a firmware referenced bny a paused run or a snapshot**: their state can only be resumed on the firmware that wrote it, so
the run or snapshot goes first.

## Pre-built firmware

[The pre-built firmware]({{ '/firmware/' | relative_url }}) is the `firmware`
release of sim-mesh's repository, which this site serves; its listing carries
each zip's facts, so the Firmware tab lists them without fetching any.
