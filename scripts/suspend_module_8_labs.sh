#!/bin/bash

# Stop all instances matching the module 8 pattern
echo "Stopping all module 8 labs..."
brev ls | grep "lab---module-8---nvidia-driver" | awk '{print $1}' | xargs -I {} sh -c 'echo "Stopping {}..."; brev stop {}'
echo "All stop commands issued."
