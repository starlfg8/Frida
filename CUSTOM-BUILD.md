# Custom Android arm64 build

The `Custom Frida Android arm64` workflow is manually triggered from GitHub Actions.
It builds Frida 17.24.3 with the GLib revision recorded in that release's
`releng/deps.toml`, and uploads the server, gadget, and SHA-256 checksums as a
workflow artifact. It does not create a GitHub release.

The workflow first builds an Android SDK from source with the patched GLib,
checks the resulting static libraries for the requested names, and then builds
Frida against the locally packaged SDK. The source patches set:

* GLib thread-pool worker names to `httpdns_db1` (all GLib pool workers can
  share this name; Frida 17.24.3's GLib uses `pool-%d`, not `pool-frida`).
* The GLib D-Bus shared thread to `gws-1`.
* The Gum JavaScript loop thread to `gt-thread-gd`.

This workflow starts from upstream Frida and applies only these two patches;
it does not apply the repository's other anti-detection patches. Runtime
behavior, other identifying strings, and client/server compatibility must be
verified on the intended Android device. The SDK build is expensive and can
take substantial time and disk space. These patches are pinned to this Frida
and GLib revision; upgrading requires reviewing the patches and dependency build.

Push this repository, including `.github/workflows/custom-frida.yml` and
`custom-patches/`, to a GitHub repository. Under Actions, choose
`Custom Frida Android arm64` and run it on the branch containing the workflow.
Download the artifact from the completed run. The local `frida-source/` and
`glib-source/` checkouts are ignored and need not be pushed.
