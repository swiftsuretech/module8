#!/bin/bash
set -e
# Wait for drivers to be potentially loaded
sleep 5

# 1. Load required kernel modules
modprobe nvidia-modeset || true
modprobe nvidia-drm || true

# 2. Create /dev/nvidia-modeset if missing
if [ ! -e /dev/nvidia-modeset ]; then
    mknod -m 666 /dev/nvidia-modeset c 195 254 || true
fi

# 2b. Create /dev/nvidia0 if missing (sometimes needed)
if [ ! -e /dev/nvidia0 ]; then
    mknod -m 666 /dev/nvidia0 c 195 0 || true
fi

# 2c. Create /dev/nvidiactl if missing
if [ ! -e /dev/nvidiactl ]; then
    mknod -m 666 /dev/nvidiactl c 195 255 || true
fi

# 3. Restart nvidia-persistenced to pick up devices
systemctl restart nvidia-persistenced || true

# 4. Fix library symlinks for Container Toolkit
LIB_PATH="/usr/lib/x86_64-linux-gnu"
# Find any version of the openssl3 lib
TARGET_LIB=$(find "$LIB_PATH" -name "libnvidia-pkcs11-openssl3.so.*" | head -n 1)

if [ -n "$TARGET_LIB" ]; then
    # Construct the link name (replace -openssl3 with empty string)
    LINK_NAME=$(echo "$TARGET_LIB" | sed 's/-openssl3//')
    if [ ! -e "$LINK_NAME" ]; then
        ln -sf "$TARGET_LIB" "$LINK_NAME"
    fi
fi


