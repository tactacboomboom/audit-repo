# INSTALL — anthropics-quickstarts

Guide d'installation factorisé pour les 7 quickstarts.

## Prérequis communs

- **Anthropic API key** : https://console.anthropic.com → générer une clé → `export ANTHROPIC_API_KEY='sk-ant-...'`
- **Git** : pour cloner
- **Python 3.11+** ou **Node 18+** selon le quickstart

## Clone du repo

```bash
git clone https://github.com/anthropics/anthropic-quickstarts.git
cd anthropic-quickstarts
```

## Par quickstart

### agents/

```bash
cd agents
pip install anthropic mcp
jupyter notebook agent_demo.ipynb
```

### autonomous-coding/

```bash
cd autonomous-coding
npm install -g @anthropic-ai/claude-code  # CLI requis
pip install -r requirements.txt
python autonomous_agent_demo.py --project-dir ./my_project --max-iterations 3
```

Avertissement : durée totale plusieurs heures pour 200 features. Réduire dans `prompts/initializer_prompt.md` pour démo rapide.

### browser-use-demo/

```bash
cd browser-use-demo
cp .env.example .env
# éditer .env avec ANTHROPIC_API_KEY
docker-compose up
```

### computer-use-best-practices/

```bash
cd computer-use-best-practices
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
cp .env.example .env  # ajouter ANTHROPIC_API_KEY
python -m computer_use "open TextEdit and type hello world"
```

macOS uniquement. Screen Recording + Accessibility permissions requises. VM fortement recommandée.

Mode browser-only (sans contrôle bureau) :
```bash
CU_ENABLE_COMPUTER_USE_TOOLS=false python -m computer_use "..."
```

### computer-use-demo/

```bash
cd computer-use-demo
./setup.sh
docker build -t computer-use-demo .
docker run -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY -p 8080:8080 computer-use-demo
```

### customer-support-agent/

```bash
cd customer-support-agent
npm install
cp .env.example .env.local  # ajouter ANTHROPIC_API_KEY + BAWS_* (AWS Bedrock)
npm run dev
# http://localhost:3000
```

### financial-data-analyst/

```bash
cd financial-data-analyst
npm install
echo "ANTHROPIC_API_KEY=..." > .env.local
npm run dev
# http://localhost:3000
```

## Vérification

Après installation, chaque quickstart doit afficher une réponse Claude en moins d'une minute (sauf autonomous-coding : plusieurs minutes pour la première session).

## Troubleshooting global

- **"API key not set"** : `echo $ANTHROPIC_API_KEY` doit retourner ta clé
- **macOS Python 3.9** : incompatible. Installer 3.11+ via `brew install python@3.11`
- **Docker permission denied** : ajouter user au groupe docker (`sudo usermod -aG docker $USER`, relog)
