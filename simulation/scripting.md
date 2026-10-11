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

A script is plain Python against sim-mesh's own library, run from its top to
its end, each call doing what it says and returning when it has:

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

The library's names come in three kinds: `script_…`, about the script;
`sim_…`, about its simulation; and **selections**, `nodes(…)` and
`node(name)`, with what is done to their nodes as their methods.

## The script

- `script_input(name, type=, label=, default=, category=)` — something the
  script asks for before it runs, at its top level with literal arguments so
  the page can read it without running the script; returns its value. `type`
  is `int`, `float`, `str`, `bool`, `Firmware` (an installed firmware, shown
  on the Scripts tab as a dropdown of those of its `category`) or `Run` (a
  run's name). From a shell it is `--set name=value`; the run keeps the
  values.
- `script_include(path)` — another file run here; every script starts from
  `scripts/startup.py`, which says the roles, the radio from
  `scripts/globals.py`, each nodeset's own setup, then starts the radios.
- `script_results(futures)` — what commands given `wait=False` came to.
- `script_loglevel(level)` — how much goes to the run's `scripts.log`:
  `"output"` (what it prints, its errors), `"commands"` (and every command
  with its answers), `"debug"` (and what goes to and from the simulation).

## The simulation

- `sim_speed(speed)` — `"real"`, `"max"` (virtual time as fast as the
  stations allow) or a number, virtual time paced at that many times the
  wall; said before anything is done.
- `sim_nodesets()`, `sim_now()`, `sim_wait(seconds)`, `sim_until(seconds)`,
  `sim_phase((name, until), …)`, `sim_snapshot(name)`, `sim_pause()`,
  `sim_stop()`, and `sim_script_loglevel(level)` for every script on it.

## Nodes

A selection is a condition over each node's facts —
`nodes(tag="lora", role="transport")`, `nodes(category="reticulum")`,
`node("gw02")` — combined with `&`, `|`, `-`, `~`. What is done to it is
done to each of its nodes:

- `.firmware(name)` — what they run: an installed firmware by name, or
  `<base>_latest`, usually an input's value.
- `.on_first_boot(*rules)` — what each is given the first time it boots with
  no state: lines in its own language, or a firmware's command said on the
  class `Node`, which then is a rule rather than done —
  `Node.radio(freq_mhz, sf, bw_khz, cr, tx_dbm, sync, preamble)`,
  `Node.radio_up()`, `Node.reticulum.role("transport")`,
  `Node.reticulum.lxmf.create()`.
- `.up()`, `.exec(lines)` (macros filled in: `{name}`, `{id}`, `{addr}`,
  `{addr:<node>}`, `{max_dbm}`), `.reset()`, `.factory_reset()`,
  `.move(lat, lon)`, `.facts()`.

Every command that acts takes `after=` (seconds on the run's clock) and
`wait=False` (a future, at once); a firmware's commands take `spread=` too.

## Choosing the firmware

A script asks for its firmware as an input, and the Scripts tab shows a
dropdown for it above the script, offering the installed firmware of the
category the script needs:

```python
firmware = script_input("firmware", type=Firmware, category="reticulum",
                        label="Firmware for nodes not otherwise configured")
nodes().firmware(firmware)
```

From a shell, `sim run lxmf-traffic … --set firmware=relay-sx1262_latest`.
A run keeps what each name resolved to.

## Every firmware's commands

A firmware's commands are done by each node's driver, its own way. These
every driver answers, whatever its category:

| Command | Does |
|---|---|
| `.radio(freq_mhz=, sf=, bw_khz=, cr=, tx_dbm=, sync=, preamble=)` | slot 0's LoRa settings, only those given; `tx_dbm` at the antenna connector, `"max"` each node's own maximum |
| `.radio_up()` | the radio started, for a firmware whose radio waits for it |

## Reticulum commands

Under `.reticulum`, for a selection's nodes of category `reticulum` and
nothing to the others:

| Command | Does | Returns |
|---|---|---|
| `.reticulum.role(role)` | `transport` (forwards others' traffic) or `client` | |
| `.reticulum.path(to=, dest_hash=, iface=)` | | each node's path table, `[{dest, next_hop, iface, hops}]`: to a node or LXMF identity, a destination, on an interface, or all of it |
| `.reticulum.lxmf.create(name=)` | one more LXMF identity, named after the node unless `name` says otherwise, unless it has one by that name | `{node: its address}` |
| `.reticulum.lxmf.identities()` | | each node's `[(name, address)]`, the one it sends from first |
| `.reticulum.lxmf.announce(name=)` | an announce of that identity's delivery destination (none named: the first) | |
| `.reticulum.lxmf.send(to, text, sender=)` | an LXMF message to a node or an LXMF identity by name, from the identity `sender` (none named: the first) | `{node: the message's id}` |

What became of each message the driver reports as the event
`lxmf.message.status` under that id: `pending`, `sent`, `delivered` or
`failed`, with why.

## MeshCore commands

Under `.meshcore`, for a selection's nodes of category `meshcore` and
nothing to the others. Each is meshcore-cli's command of that name:

| Command | Does | Returns |
|---|---|---|
| `.meshcore.repeat(on)` | forwarding others' packets on or off | |
| `.meshcore.advert()` | a zero-hop advert | |
| `.meshcore.floodadv()` | a flooded advert | |
| `.meshcore.contacts()` | | each node's `[(name, public-key prefix, path length)]`, the length None for a contact reached by flood |
| `.meshcore.msg(to, text)` | a direct message to the contact `to`, a node's name once it has advertised it | `{node: the message's id}` |
| `.meshcore.chan(nb, text)` | a message on channel `nb` | `{node: the message's id}` |
| `.meshcore.path(to)` | | each node's path to the contact `to`, its hops' hash prefixes (`[]` for a neighbour), or None for flood |
| `.meshcore.reset_path(to)` | back to flood for that contact | |

What became of each message the sender's driver reports as the event
`msg.status` under that id: `sent`, then for `msg` `delivered` or `failed`,
with why; a channel message ends at `sent`. The receiver's driver reports
each message it got as `msg.received`, with the id, the text, and the
sender's public-key prefix or the channel.

## Meshtastic commands

Under `.meshtastic`, for a selection's nodes of category `meshtastic` and
nothing to the others. Each is named as the Meshtastic CLI's option:

| Command | Does | Returns |
|---|---|---|
| `.meshtastic.role(role)` | its device role, Meshtastic's in lower case (`client`, `router`, `router_late`, …) | |
| `.meshtastic.hop_limit(n)` | the hops a packet it originates may take, 0–7 | |
| `.meshtastic.sendtext(text, to=None, ch_index=0, want_ack=True)` | a text message to the node `to`, by its name, or on channel `ch_index` when `to` is None | `{node: the message's id}` |
| `.meshtastic.traceroute(to)` | | each node's route to `to` and back, `{route, snr_towards, route_back, snr_back}` |
| `.meshtastic.nodes()` | | each node's `[(name, id, hops away, snr, last heard)]` |
| `.meshtastic.nodeinfo()` | a NodeInfo broadcast now | |

What became of each message is reported as for MeshCore: `msg.status` under
its id, `sent`, then for a direct message `delivered` or `failed`, with why,
and a channel message ends at `sent`; `msg.received` at the receiver, with
the sender's `!id` or the channel.

## Running one

The Scripts tab's **Run** starts a new simulation of the script on the Nodes
tab's geodata and its open nodeset, or else the ones checked in its list
(several merged), or runs it on one already running or
paused; from a shell:

```sh
sim run lxmf-traffic --geodata berlin-city --nodeset mitte7 --set firmware=relay-sx1262_latest
sim run lxmf-traffic --sim mitte7 --set firmware=relay-sx1262_latest
sim run lxmf-traffic --resume mitte7 --set firmware=relay-sx1262_latest   # a paused one, resumed
```

A script whose simulation is stopped or paused under it stops with
"simulation … went away" the next time it waits on it. What a script prints
and its errors are kept in the run's `scripts.log`. `def report(run_dir)`
returns the run's report as Markdown, written beside the run with an ETSI
(EN 300 220) compliance section after it.

## The LXMF traffic run

`scripts/lxmf-traffic.py` is a whole LXMF run on virtual time, on any
`reticulum` firmware: announce warm-up until paths stop growing, a seeded
hour of messages, a drain, and the simulation paused. Its report is what the
senders' drivers reported of each message: delivered overall, by route and
radio hops and by size, the latency, and the undelivered by the last status
reported.
