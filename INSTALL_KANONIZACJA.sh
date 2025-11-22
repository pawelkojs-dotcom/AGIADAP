#!/bin/bash
# KANONIZACJA SPRINT 2.5.3 - Installation Script
# Installs canonized documents into project structure

set -e  # Exit on error

echo "╔═══════════════════════════════════════════════════╗"
echo "║  KANONIZACJA SPRINT 2.5.3 - INSTALLATION         ║"
echo "╚═══════════════════════════════════════════════════╝"
echo

# Check if running from correct directory
if [ ! -d "/mnt/user-data/outputs" ]; then
    echo "❌ Error: Must run from environment with /mnt/user-data/outputs"
    exit 1
fi

echo "📋 Files to install:"
echo "  • ADR_AGI_001_R4_Thresholds.md"
echo "  • CONCORDANCE_AGI_UPDATED.md → CONCORDANCE_AGI.md"
echo "  • AGI_MASTER_INDEX_UPDATED.md → AGI_MASTER_INDEX.md"
echo

# Backup existing files
echo "💾 Creating backups..."
if [ -f "/mnt/project/CONCORDANCE_AGI.md" ]; then
    cp /mnt/project/CONCORDANCE_AGI.md /mnt/project/CONCORDANCE_AGI.md.backup.$(date +%Y%m%d_%H%M%S)
    echo "  ✓ Backed up CONCORDANCE_AGI.md"
fi

if [ -f "/mnt/project/AGI_MASTER_INDEX.md" ]; then
    cp /mnt/project/AGI_MASTER_INDEX.md /mnt/project/AGI_MASTER_INDEX.md.backup.$(date +%Y%m%d_%H%M%S)
    echo "  ✓ Backed up AGI_MASTER_INDEX.md"
fi
echo

# Install files
echo "📦 Installing canonized documents..."

# 1. ADR (new file)
cp /mnt/user-data/outputs/ADR_AGI_001_R4_Thresholds.md /mnt/project/
echo "  ✓ Installed ADR_AGI_001_R4_Thresholds.md"

# 2. CONCORDANCE (replace)
cp /mnt/user-data/outputs/CONCORDANCE_AGI_UPDATED.md /mnt/project/CONCORDANCE_AGI.md
echo "  ✓ Updated CONCORDANCE_AGI.md (Section 5 added)"

# 3. MASTER_INDEX (replace)
cp /mnt/user-data/outputs/AGI_MASTER_INDEX_UPDATED.md /mnt/project/AGI_MASTER_INDEX.md
echo "  ✓ Updated AGI_MASTER_INDEX.md (Experiments section added)"

echo
echo "✅ Installation complete!"
echo
echo "📊 Summary:"
echo "  • 1 new file added (ADR)"
echo "  • 2 files updated (CONCORDANCE, MASTER_INDEX)"
echo "  • 2 backups created"
echo
echo "🔍 Verify installation:"
echo "  grep -n 'Sprint 2.5.3' /mnt/project/CONCORDANCE_AGI.md"
echo "  grep -n 'EXPERIMENTS' /mnt/project/AGI_MASTER_INDEX.md"
echo "  ls -lh /mnt/project/ADR_AGI_001_R4_Thresholds.md"
echo
echo "📚 Documentation:"
echo "  → KANONIZACJA_FINAL_SUMMARY.md"
echo "  → KANONIZACJA_VISUAL_SUMMARY.txt"
echo
echo "🎉 Sprint 2.5.3 now CANONICAL!"

