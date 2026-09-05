# Virtual machines

The Blueprint uses **KVM/QEMU + libvirt + virt-manager** for general-purpose virtual machines.

This is the default virtualization feature for the **Laboratory** profile. Gaming and Work can add the exact same feature during installation or later.

## Why this stack

- KVM gives Linux guests near-native CPU virtualization when hardware virtualization is available.
- libvirt keeps VM definitions, networks and storage consistent.
- virt-manager is a mature desktop UI and gives access to the settings that matter for Hyprland/Linux guests.
- virglrenderer is installed so supported guests can use virtio/3D acceleration instead of falling back to `llvmpipe`.
- UEFI (OVMF), TPM emulation (swtpm), NAT networking and a default storage pool are prepared by the Blueprint.

VirtualBox is intentionally not the Blueprint default. It is portable, but our previous Hyprland/CachyOS testing was materially smoother with KVM/QEMU and virt-manager.

## Install behavior

Laboratory defaults to virtualization = yes. Work and Gaming ask and default to no.

Examples:

```bash
bash scripts/install --profile laboratory
bash scripts/install --profile work --with virtualization
bash scripts/install --profile gaming --with virtualization
```

To explicitly keep Laboratory lean:

```bash
bash scripts/install --profile laboratory --without virtualization
```

## Launch

Use the app launcher and open **Virtual Machines**, or run:

```bash
devos-vm
```

Other helper commands:

```bash
devos-vm list
devos-vm validate
```

## Portability

The feature is hardware-aware rather than laptop-specific. On an Intel or AMD Linux machine with `/dev/kvm`, it uses the host KVM acceleration exposed by the kernel. If firmware virtualization is disabled, the Blueprint warns instead of applying vendor-specific hacks.

Inside a VM, nested virtualization depends on the outer hypervisor exposing `/dev/kvm`; the Blueprint does not pretend nested KVM is available when it is not.

## Creating guests

For now, guest creation stays in virt-manager so CPU/RAM/disk choices remain explicit. For Linux/Hyprland guests, prefer:

- Q35 machine type;
- UEFI/OVMF;
- virtio disk/network;
- virtio graphics with 3D acceleration when the host supports a render node;
- SPICE/virt-viewer for the display.

The current manual clean-install procedure for Gaming, Work and Laboratory is documented in [Clean KVM validation runbook](kvm-validation.md). It intentionally keeps the three guests separate and requires a post-reboot `bash scripts/check` pass for each profile.

A reproducible one-command **Blueprint Test VM** template is a separate roadmap task and will be added only after the new host profiles pass that clean-install validation.
