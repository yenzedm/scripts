## 🔄 GitLab CI/CD Flow with GitGraph, Confluence & Jira Integration

### 🧠 Overview

An automated CI/CD process that:

- Checks if a Confluence page exists for the `target` branch release
- Creates or updates a `gitgraph` diagram in Mermaid format
- Synchronizes data with Confluence and Jira
- Creates a historical tracking task in Jira

---

### 🏷️ Variables

- **`source`** branch — defined via GitLab CI variable
- **`target`** branch — used as the name of the release branch

---

### 🧪 Step 1: Check for existing Confluence page

Script: `check_page_exist.py`

- Verifies if a corresponding Confluence page exists
- Returns:
  - `exit(0)` — if the page **exists**
  - `exit(1)` — if the page **does not exist**

---

### ❌ If the page does not exist (`exit(1)`)

1. **`create_gitgraph.py`**  
   Generates a `diagram.mmd` file containing the Mermaid `gitgraph` diagram.

2. **Convert `diagram.mmd` to `diagram.svg`**
   ```bash
   mmdc -i diagram.mmd -o diagram.svg
   ```

3. **`confluence_page_not_exist.py`**
   - Creates a new Confluence page named _"mermaid n.n.n"_ for the `target` branch release
   - Adds to the page:
     - An HTML block with the `diagram.svg`
     - The `diagram.mmd` file as an attachment

4. **`jira_project_releases.py`**
   - Adds or updates a release in the **Recfaces Jira project**

5. **`create-history-task.py`**
   - Creates a historical tracking task in Jira

---

### ✅ If the page exists (`exit(0)`)

1. **`update_gitgraph.py`**
   - Finds the existing Confluence page related to the `target` branch
   - Extracts the current `diagram.mmd` from the page comment
   - Updates the file based on the `target` and `source` branches

2. **Convert `diagram.mmd` to `diagram.svg`**
   ```bash
   mmdc -i diagram.mmd -o diagram.svg
   ```

3. **Update page content**

   - **`confluence_page_exist.py`**
     - Replaces the HTML block with the updated `diagram.svg`
     - Re-uploads the `diagram.mmd` attachment

4. **`jira_project_releases.py`**
   - Adds or updates the release in the **Recfaces Jira project**

5. **`create-history-task.py`**
   - Creates a historical tracking task in Jira

---

### 📦 Scripts used

- `check_page_exist.py`
- `create_gitgraph.py`
- `update_gitgraph.py`
- `confluence_page_not_exist.py`
- `confluence_page_exist.py`
- `jira_project_releases.py`
- `create-history-task.py`

# 🛠️ Installing `@mermaid-js/mermaid-cli` on GitLab Runner

This guide covers installation on Ubuntu versions **20.04**, **22.04**, and **24.04**.

---

## 📦 Ubuntu 20.04 / 22.04

```bash
# Install Node.js and npm
sudo apt install nodejs
sudo apt install npm

# Upgrade Node.js to latest LTS version
sudo npm install -g n
sudo n lts

# Install mermaid-cli globally
sudo npm install -g @mermaid-js/mermaid-cli

# Install necessary Chrome runtime for Puppeteer
npx puppeteer browsers install chrome
# or
npx puppeteer browsers install chrome-headless-shell

# (Optional) Clear Puppeteer cache — run as the 'gitlab-runner' user
rm -rf ~/.cache/puppeteer

# Install additional dependencies required for rendering
sudo apt install -y \
  libnss3 libatk1.0-0 libatk-bridge2.0-0 libxdamage1 libasound2 \
  libcups2 libxcomposite1 libxrandr2 libgbm1 \
  libpango-1.0-0 libpangocairo-1.0-0 libxshmfence1

# Test rendering
mmdc -i diagram.mmd -o diagram.svg
```

---

## 🐧 Ubuntu 24.04

```bash
# Install Node.js and npm
sudo apt install nodejs
sudo apt install npm

# Upgrade Node.js to latest LTS version
sudo npm install -g n
sudo n lts

# Install mermaid-cli globally
sudo npm install -g @mermaid-js/mermaid-cli

# Install Puppeteer browser dependencies
npx puppeteer browsers install chrome
# or
npx puppeteer browsers install chrome-headless-shell

# (Important) Run as 'gitlab-runner' user
rm -rf ~/.cache/puppeteer

# Temporarily disable AppArmor restrictions
sudo sysctl -w kernel.apparmor_restrict_unprivileged_unconfined=0
sudo sysctl -w kernel.apparmor_restrict_unprivileged_userns=0

# Test rendering
mmdc -i diagram.mmd -o diagram.svg

# Re-enable AppArmor restrictions after rendering
sudo sysctl -w kernel.apparmor_restrict_unprivileged_unconfined=1
sudo sysctl -w kernel.apparmor_restrict_unprivileged_userns=1
```

