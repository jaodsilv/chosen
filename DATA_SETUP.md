# Data Repository Setup Guide

This guide explains how to set up and manage the private data repository for CHOSEN.

## Overview

The application's private data (signatures, messages, threads, settings) is stored in a **separate encrypted private repository** for security and version control.

## Architecture

1. **Main Repository**: `chosen` (this repository)
   - Contains application code
   - Has `data/` in `.gitignore` (never commits private data)
   - Has a directory junction at `data/` pointing to the separate data repository

2. **Data Repository**: `chosen-data` (private repository)
   - Contains all private data
   - Uses **git-crypt** for encryption
   - All JSON files are automatically encrypted
   - Only accessible with the encryption key

## Initial Setup (Already Complete)

The data repository has already been set up on this machine:

1. ✅ Private GitHub repository created: <https://github.com/jaodsilv/chosen-data>
2. ✅ git-crypt initialized and configured
3. ✅ Encryption key exported to: `D:\src\chosen\git-crypt-key.key`
4. ✅ Directory structure created (exports, messages, threads, settings)
5. ✅ Existing signature files migrated and encrypted
6. ✅ Directory junction created: `main/data/` → `../data/`

## Setting Up on Additional Machines

Follow these steps to set up the data repository on another computer:

### Step 1: Install git-crypt

**Windows (using Scoop):**

```bash
# Install Scoop (if not already installed)
# Open PowerShell as Administrator
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
irm get.scoop.sh | iex

# Install git-crypt
scoop install git-crypt
```

**macOS (using Homebrew):**

```bash
brew install git-crypt
```

**Linux:**

```bash
# Debian/Ubuntu
sudo apt install git-crypt

# Fedora
sudo dnf install git-crypt
```

### Step 2: Clone the Main Repository

```bash
cd D:\src  # Or your preferred location
git clone https://github.com/jaodsilv/chosen.git
cd chosen
npm install
```

### Step 3: Clone the Data Repository

```bash
cd D:\src\chosen
git clone git@github.com:jaodsilv/chosen-data.git data
```

**Note**: This clones into `data/` subdirectory of the parent folder.

### Step 4: Unlock the Repository

1. **Transfer the encryption key securely** to the new machine:
   - Original location: `D:\src\chosen\git-crypt-key.key`
   - Methods: Password manager, encrypted USB drive, secure file transfer

2. **Unlock the repository**:

   ```bash
   cd data
   git-crypt unlock /path/to/git-crypt-key.key
   ```

3. **Verify unlocking worked**:

   ```bash
   git-crypt status
   # Should show "encrypted: exports/*.json" etc.

   # Files should now be readable
   cat exports/signatures-2025-06-29.json
   ```

### Step 5: Create Directory Junction (Windows)

**On Windows:**

```cmd
cd D:\src\chosen\main
mklink /J data ..\data
```

**On macOS/Linux (symlink):**

```bash
cd /path/to/chosen/main
ln -s ../data data
```

### Step 6: Verify Setup

```bash
cd D:\src\chosen\main
ls -la data/exports/  # Should show your encrypted files
```

## Directory Structure

```
D:\src\chosen\
├── main/                              # Main application repository
│   ├── app/                           # Application code
│   ├── data/ → ../data                # Junction/symlink to data repo
│   ├── .gitignore                     # Excludes data/
│   └── DATA_SETUP.md                  # This file
│
├── data/                              # Separate data repository (encrypted)
│   ├── .git/                          # Git repository
│   ├── .gitattributes                 # Encryption rules
│   ├── exports/                       # Signature exports (encrypted)
│   ├── messages/                      # Message history (encrypted)
│   ├── threads/                       # Conversation threads (encrypted)
│   └── settings/                      # App settings (encrypted)
│
└── git-crypt-key.key                  # Encryption key (NEVER commit!)
```

## Data Management Workflow

### Adding/Modifying Data

The application automatically saves data to the appropriate directories. To version control changes:

```bash
cd D:\src\chosen\data

# Check what changed
git status
git diff

# Stage and commit changes
git add exports/new-signature.json
git commit -m "Add new LinkedIn signature"

# Push to GitHub
git push
```

### Syncing Across Machines

**Before starting work:**

```bash
cd D:\src\chosen\data
git pull
```

**After making changes:**

```bash
cd D:\src\chosen\data
git add -A
git commit -m "Update message templates"
git push
```

## Security Best Practices

### Critical Security Rules

1. **NEVER commit the encryption key** to any repository
2. **NEVER make the data repository public**
3. **ALWAYS verify files are encrypted** before pushing:

   ```bash
   git-crypt status
   ```

4. **Store the encryption key securely**:
   - Use a password manager (1Password, Bitwarden, etc.)
   - Encrypted cloud storage (not Dropbox/Google Drive plaintext!)
   - Encrypted USB drive in a safe location

### Encryption Verification

To verify files are encrypted in the repository:

```bash
cd D:\src\chosen\data

# Check encryption status
git-crypt status

# View raw encrypted data (should be binary garbage)
git show HEAD:exports/signatures.json

# View decrypted data (readable JSON)
cat exports/signatures.json
```

### Key Rotation (Advanced)

If you need to rotate the encryption key:

1. **Export all data** (unencrypted backup)
2. **Remove git-crypt** configuration
3. **Re-initialize git-crypt** with a new key
4. **Re-encrypt** all files
5. **Force push** new history (⚠️ destructive!)

**Note**: This is rarely needed and should only be done if the key is compromised.

## Troubleshooting

### Error: "git-crypt: command not found"

**Solution**: Install git-crypt (see Step 1)

### Error: "git-crypt unlock failed"

**Possible causes**:

1. Wrong key file - ensure you're using the correct `git-crypt-key.key`
2. Corrupted key - verify file size is 148 bytes
3. Repository not initialized with git-crypt

### Files show binary garbage

**Cause**: Repository is locked (encrypted)

**Solution**:

```bash
cd data
git-crypt unlock /path/to/git-crypt-key.key
```

### Junction/Symlink not working

**Windows**: Must use `mklink /J` from cmd (not PowerShell or bash)
**macOS/Linux**: Use `ln -s ../data data`

**Verification**:

```bash
ls -la main/data  # Should show junction/symlink indicator
```

## Environment Variables

Override the data directory location via `.env`:

```bash
# .env file
DATA_DIR=/custom/path/to/data
```

**Default**: `./data` (junction to `../data/`)

## Backup Strategy

### Automatic Backups (via Git)

1. **GitHub serves as primary backup** (private repository)
2. **Every push creates a backup** in the cloud
3. **Version history** allows recovery of any previous state

### Additional Backup (Recommended)

1. **Export the encryption key** to multiple secure locations
2. **Clone the data repository** to an external drive:

   ```bash
   git clone https://github.com/jaodsilv/chosen-data.git /path/to/backup
   cd /path/to/backup
   git-crypt unlock /path/to/key
   ```

3. **Automated backups** with git push hooks (optional)

## FAQ

### Q: Can I access the data without the encryption key?

**A**: No. Without the key, all JSON files are encrypted binary data.

### Q: What happens if I lose the encryption key?

**A**: You **cannot decrypt** the data. This is why secure key backup is critical.

### Q: Can I use the same data repository with multiple main repositories?

**A**: Yes, but create separate junctions/symlinks for each main repository clone.

### Q: Do I need admin rights to create junctions on Windows?

**A**: No, directory junctions (`/J`) don't require admin rights (unlike symlinks `/D`).

### Q: Can I share data with team members?

**A**: Yes:

1. Share the encryption key securely (encrypted email, password manager sharing)
2. Grant them access to the private GitHub repository
3. They follow the "Setting Up on Additional Machines" steps

## Support

1. **Main Repository**: <https://github.com/jaodsilv/chosen>
2. **Data Repository**: <https://github.com/jaodsilv/chosen-data> (private)
3. **git-crypt Documentation**: <https://github.com/AGWA/git-crypt>
4. **Issues**: Create an issue in the main repository (never mention private data!)

## Related Files

1. **Main Repository**:
   - `.gitignore` - Excludes data/ from version control
   - `app/config/data-paths.ts` - Data path configuration
   - `.env.example` - Environment variable examples

2. **Data Repository**:
   - `README.md` - Data repository documentation
   - `.gitattributes` - Encryption rules
   - `.gitignore` - Minimal ignores for data repo
