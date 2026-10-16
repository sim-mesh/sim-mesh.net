---
title: Scripting
permalink: /simulation/scripting/
redirect_from:
  - /scripts/
description: Plain Python that says what a simulation's nodes run and what is done to them.
---

A script is how you tell a simulation what to do. It picks which firmware the
nodes run, then plays out a scenario over time: start the nodes, let them
announce, wait ten minutes, send a message, see what arrived. Think of it as
a test script for a whole mesh network.

A script is plain Python using sim-mesh's library. It runs top to bottom, and
each call returns when it has been done:

```python
"""A study: one firmware everywhere, another where tagged."""
from sim_mesh import *

firmware = script_input("firmware", type=Firmware, category="reticulum",
                        label="Firmware for nodes not otherwise configured")
other = script_input("other", type=Firmware, category="reticulum",
                     label="Firmware for the nodes tagged other")
sim_speed("max")                              # declarations first
nodes().firmware(firmware)
nodes(tag="other").firmware(other)
script_include("scripts/startup.py")          # roles, radios, each nodeset's own setup
nodes().on_first_boot(Node.reticulum.lxmf.create())

nodes().up()                                  # the first thing done starts the simulation
nodes(tag="transport").reticulum.lxmf.announce(spread=60)
sim_wait(600)
node("gw02").reticulum.lxmf.send("internet", "hello")
sim_pause()
```

There are three kinds of names: `script_…` functions are about the script
itself, `sim_…` about the simulation, and `nodes(…)` / `node(name)` select
nodes, with the things you can do to them as methods.

## The script

- `script_input(name, type=, label=, default=, category=)` — a parameter the
  script asks for before it runs, shown as a field on the Scripts tab. Call
  it at the top level with literal arguments, so the page can find it without
  running the script. Returns the value. `type`
  is `int`, `float`, `str`, `bool`, `Firmware` (an installed firmware, shown
  on the Scripts tab as a dropdown of those of its `category`) or `Run` (a
  run's name). From a shell it is `--set name=value`; the run keeps the
  values.
- `script_include(path)` — runs another file at this point. Every script
  includes `scripts/startup.py`, which sets roles and radio settings (from
  `scripts/globals.py`), applies each nodeset's own setup and starts the
  radios.
- `script_results(futures)` — the results of commands started with
  `wait=False`.
- `script_loglevel(level)` — how much goes to the run's `scripts.log`:
  `"output"` (what it prints, its errors), `"commands"` (and every command
  with its answers), `"debug"` (and what goes to and from the simulation).

## The simulation

- `sim_speed(speed)` — `"real"`, `"max"` (virtual time, as fast as possible)
  or a number (virtual time at that multiple of real time). Must come before
  any command.
- `sim_nodesets()`, `sim_now()`, `sim_wait(seconds)`, `sim_until(seconds)`,
  `sim_phase((name, until), …)`, `sim_snapshot(name)`, `sim_pause()`,
  `sim_stop()`, and `sim_script_loglevel(level)` for every script on it.

## Nodes

A selection picks nodes by their properties: `nodes(tag="lora",
role="transport")`, `nodes(category="reticulum")`, `node("gw02")`. Combine
selections with `&`, `|`, `-`, `~`. A method on a selection runs on every
node in it:

- `.firmware(name)` — what they run: an installed firmware by name, or
  `<base>_latest`, usually an input's value.
- `.on_first_boot(*rules)` — what to do the first time a node boots without
  state: console lines in the firmware's own language, or commands written on
  the class `Node` (which records them instead of running them now), such as
  `Node.radio(freq_mhz, sf, bw_khz, cr, tx_dbm, sync, preamble)`,
  `Node.radio_up()`, `Node.reticulum.role("transport")`,
  `Node.reticulum.lxmf.create()`.
- `.up()`, `.exec(lines)` (macros filled in: `{name}`, `{id}`, `{addr}`,
  `{addr:<node>}`, `{max_dbm}`), `.reset()`, `.factory_reset()`,
  `.move(lat, lon)`, `.facts()`.

Every command takes `after=` (delay in simulated seconds) and `wait=False`
(return a future immediately instead of waiting); firmware commands also take
`spread=` (spread the nodes out over that many seconds).

## Every firmware's commands

Firmware commands are carried out by each node's driver. Every driver,
whatever its category, answers these:

| Command | Does |
|---|---|
| `.radio(freq_mhz=, sf=, bw_khz=, cr=, tx_dbm=, sync=, preamble=)` | slot 0's LoRa settings, only those given; `tx_dbm` at the antenna connector, `"max"` each node's own maximum |
| `.radio_up()` | starts the radio, on firmware that waits to be told |

## Messaging, whatever the protocol

Sending a message works differently in every mesh, but a script that just
wants "a message from this node to that one" shouldn't have to care. These
two commands work on any selection, and each node does them in its own
protocol, so one script runs unchanged on Reticulum, MeshCore or Meshtastic,
or on a mix of them:

```python
node("fred").message("sylvia", "hello")    # {node: the message's id}
nodes(tag="repeater").announce()
```

| Command | Reticulum | MeshCore | Meshtastic |
|---|---|---|---|
| `.message(to, text)`: a direct message to the node `to`, answering its id | `.reticulum.lxmf.send` | `.meshcore.msg` | `.meshtastic.sendtext` |
| `.announce(spread=0)`: each node made known to the others | `.reticulum.lxmf.announce` | `.meshcore.floodadv` | `.meshtastic.nodeinfo` |

What happened to each message is logged in the run's events: the recipient's
driver reports arrival, the sender's reports whether an acknowledgement came
back. The traffic runs below count both.

## Reticulum commands

Under `.reticulum`. They apply to the selection's Reticulum nodes and skip
the others:

| Command | Does | Returns |
|---|---|---|
| `.reticulum.role(role)` | `transport` (forwards others' traffic) or `client` | |
| `.reticulum.path(to=, dest_hash=, iface=)` | | each node's path table, `[{dest, next_hop, iface, hops}]`: to a node or LXMF identity, a destination, on an interface, or all of it |
| `.reticulum.lxmf.create(name=)` | creates an LXMF identity, named after the node unless `name` is given; does nothing if one by that name exists | `{node: its address}` |
| `.reticulum.lxmf.identities()` | | each node's identities as `[(name, address)]`, the default sender first |
| `.reticulum.lxmf.announce(name=)` | an announce of that identity's delivery destination (none named: the first) | |
| `.reticulum.lxmf.send(to, text, sender=)` | an LXMF message to a node or an LXMF identity by name, from the identity `sender` (none named: the first) | `{node: the message's id}` |

Each message's fate is reported as the event `lxmf.message.status` under its
id: `pending`, `sent`, `delivered` or `failed`, with a reason.

## MeshCore commands

Under `.meshcore`. They apply to the selection's MeshCore nodes and skip the
others. Each is meshcore-cli's command of that name:

| Command | Does | Returns |
|---|---|---|
| `.meshcore.repeat(on)` | forwarding others' packets on or off | |
| `.meshcore.advert()` | a zero-hop advert | |
| `.meshcore.floodadv()` | a flooded advert | |
| `.meshcore.contacts()` | | each node's `[(name, public-key prefix, path length)]`, the length None for a contact reached by flood |
| `.meshcore.msg(to, text)` | a direct message to contact `to` (a node's name, once that node has advertised) | `{node: the message's id}` |
| `.meshcore.chan(nb, text)` | a message on channel `nb` | `{node: the message's id}` |
| `.meshcore.path(to)` | | each node's path to the contact `to`, its hops' hash prefixes (`[]` for a neighbour), or None for flood |
| `.meshcore.reset_path(to)` | back to flood for that contact | |

The sender's driver reports each message as the event `msg.status`: `sent`,
then for direct messages `delivered` or `failed` with a reason (channel
messages stop at `sent`). The receiver's driver reports `msg.received` with
the id, the text, and the sender's public-key prefix or the channel.

## Meshtastic commands

Under `.meshtastic`. They apply to the selection's Meshtastic nodes and skip
the others. Each is named as the Meshtastic CLI's option:

| Command | Does | Returns |
|---|---|---|
| `.meshtastic.role(role)` | its device role, Meshtastic's in lower case (`client`, `router`, `router_late`, …) | |
| `.meshtastic.hop_limit(n)` | the hops a packet it originates may take, 0–7 | |
| `.meshtastic.sendtext(text, to=None, ch_index=0, want_ack=True)` | a text message to the node `to`, by its name, or on channel `ch_index` when `to` is None | `{node: the message's id}` |
| `.meshtastic.traceroute(to)` | | each node's route to `to` and back, `{route, snr_towards, route_back, snr_back}` |
| `.meshtastic.nodes()` | | each node's `[(name, id, hops away, snr, last heard)]` |
| `.meshtastic.nodeinfo()` | a NodeInfo broadcast now | |

Message events are the same as for MeshCore; the receiver's `msg.received`
carries the sender's `!id` or the channel.

## Running one

**Run** on the Scripts tab starts a new simulation on the Nodes tab's geodata
and open nodeset (or the checked nodesets, merged), or runs the script on a
simulation that is already running or paused. From a shell:

```sh
sim run lxmf-traffic --geodata berlin-city --nodeset mitte7 --set firmware=relay-sx1262_latest
sim run lxmf-traffic --sim mitte7 --set firmware=relay-sx1262_latest
sim run lxmf-traffic --resume mitte7 --set firmware=relay-sx1262_latest   # a paused one, resumed
```

If the simulation is stopped or paused while a script runs, the script stops
with "simulation … went away". Output and errors go to the run's
`scripts.log`. A script may define `report(run_dir)` returning Markdown; it
is written next to the run, followed by an ETSI EN 300 220 duty-cycle
section.

## The traffic runs

Two bundled scripts run a complete test in virtual time: a warm-up until the
nodes have discovered each other, a seeded hour of messages, time for the
last ones to arrive, then pause and report.

**`msg-traffic`** compares protocols. Nodes tagged `repeater` only forward;
the others message each other. It takes two firmware, one for the repeaters
and one for the rest, both of the same protocol. Messages are 20–55
characters, short enough for one packet on every protocol, and the same seed
produces the same messages between the same pairs at the same moments on any
protocol. [Getting started]({{ '/getting-started/' | relative_url }})
runs it on `berlin-centre` with `berlin-50`:

```sh
sim run msg-traffic --geodata berlin-centre --nodeset berlin-50 \
    --set firmware=meshcore-companion-sx1262_latest \
    --set repeater_firmware=meshcore-repeater-sx1262_latest
```

A third input, `reticulous_settings`, is a `;`-separated list of settings
applied to Reticulous nodes at first boot, for example `set
s.lxmf.stamp_cost 0; set s.lxmf.generate_stamps 0` to turn stamps off.

**`lxmf-traffic`** is the same test for Reticulum only, with every node
sending and realistic LXMF message sizes up to 650 characters.

**The report** counts every message twice:

- **delivered**: it reached its recipient, as the recipient's driver
  reports. One that arrived and was refused (a full mailbox) is counted
  apart, and is not delivered.
- **proven**: the sender heard so, a proof or acknowledgement back across the
  mesh, which can be lost like any other packet. Shown as a number of its
  own and as a share of the delivered.

Both are broken down by hop count, by size, and by time to delivery and to
proof; undelivered messages are listed by their last reported status.
