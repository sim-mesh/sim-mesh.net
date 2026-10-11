# sim-mesh.net

The site at **[sim-mesh.net](https://sim-mesh.net/)**: sim-mesh's pages, how to
build firmware for it, and the pre-built firmware. Its repository on GitHub is
sim-mesh/sim-mesh.net.

```
this repo (Jekyll pages) ───────────────┐
sim-mesh/sim-mesh, CONTRACT.md ─────────┼──► .github/workflows/pages.yml ──► GitHub Pages ──► sim-mesh.net
sim-mesh/sim-mesh, release `firmware` ──┘      (CONTRACT.md as /using-firmware/building/, the release as /firmware/)
```

| Page | What |
|---|---|
| `index.md` | what sim-mesh is |
| `getting-started.md` | clone, start, add firmware, a first simulation |
| `using-firmware.md` | names, categories, adding and deleting, pre-built |
| `using-firmware/building.md` | building firmware for sim-mesh: front matter and nothing else. Its body is sim-mesh's `CONTRACT.md`, which `_tools/contract.py` makes into `_includes/contract.md` (not in this repo): the title left to the page, a table of contents before the first section, links into the repository made GitHub's. Edit the contract in sim-mesh, never here |
| `simulation.md` | a chapter per app tab, in the app's order: firmware, antennas, geodata, nodes, scripts, simulations (who hears whom, time) |
| `simulation/scripting.md` | the script library: every firmware's commands, then each category's |
| `examples/index.yaml` | sim-mesh's own index, `sim-mesh-examples`: the geodata packs and nodesets every sim-mesh lists, each by its sha256, the packs as release assets of sim-mesh/sim-mesh, and the text the page and `sim index list` print about them |

`_config.yml`'s `nav` is both the masthead and the sidebar; an entry's
`children` are sub-pages, listed under it in the sidebar. Pages that moved
keep their old URLs through `redirect_from`.

`/firmware/` is not in this repo: the deploy copies the `firmware` release of
sim-mesh/sim-mesh there — every pre-built zip, `firmware.yaml` and the
`index.html` made from it — since a browser cannot fetch a release asset
across origins. sim-mesh's `sim firmware publish` uploads to that release and
fires this repo's `firmware-published` dispatch, so new firmware is on the
site without a commit here.

## Previewing

With this repo checked out beside sim-mesh, `sim dev` there serves it at
`http://localhost:4000/` from its image, live-reloading as pages are saved;
it makes the contract's page from the sim-mesh beside it when it starts, so
an edit to `CONTRACT.md` shows after `sim dev` is started again. Without
`sim dev`, with Ruby and bundler, make the contract's page first (the build
refuses without it):

```sh
python3 _tools/contract.py ../sim-mesh/CONTRACT.md
bundle install
bundle exec jekyll serve --livereload     # http://localhost:4000/
```

## The domain

**Settings → Pages → Source** on this repo is **GitHub Actions**: the site is
only what `pages.yml` deploys. Deploying from the branch instead runs GitHub's
own build of it beside the workflow on every push, and whichever lands last
is the site; GitHub's has no `/firmware/`.

The site is `sim-mesh.net`: the domain's A and AAAA records are GitHub's
published Pages addresses, and **Settings → Pages → Custom domain** on this
repo holds `sim-mesh.net`, with **Enforce HTTPS** once GitHub has issued the
certificate. A site published by a workflow names its domain there, not in a
`CNAME` file, so this repo has none.
