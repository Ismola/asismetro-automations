# 🚀 Selenium Scraper Quickstarter

**Selenium Scraper Quickstarter** is a professional template for building robust and scalable web scrapers using Selenium and Flask, ready for local development, Docker containers, and cloud deployment.

[![Deploy](https://github.com/Ismola/asismetro-automations/actions/workflows/deploy.yml/badge.svg)](https://github.com/Ismola/asismetro-automations/actions/workflows/deploy.yml)

---

## 📋 Table of Contents

- [✨ Main Features](#-main-features)
- [📁 Project Structure](#-project-structure)
- [⚙️ Environment Variables](#️-environment-variables)
- [🏁 Quick Start](#-quick-start)
- [▶️ Running](#️-running)
- [⚙️ CI/CD and Workflow Customization](#️-cicd-and-workflow-customization)
- [🔗 API Usage](#-api-usage)
- [🛠️ Customization & Extension](#️-customization--extension)
- [🧩 Architecture & Flow](#-architecture--flow)
- [🚢 Deployment](#-deployment)
- [⚙️ GitHub Actions CI/CD](#️-github-actions-cicd)
- [🧪 Automated Testing](#-automated-testing)
- [🐞 Troubleshooting](#-troubleshooting)
- [📚 Resources & Bibliography](#-resources--bibliography)
- [🤝 Contributions](#-contributions)
- [📝 License](#-license)

---

## ✨ Main Features

- **Selenium Automation:** Advanced interaction with dynamic web pages.
- **RESTful API with Flask:** Secure and customizable endpoint exposure.
- **Bearer Authentication:** Security via configurable tokens.
- **Environment Management:** Environment variables for production, testing, and staging.
- **Docker & Codespaces Support:** Ready for containers and cloud development.
- **Logging System:** Activity and error logging for auditing and debugging.
- **Automated Downloads:** File and temporary directory management.
- **Extensible & Modular:** Clean architecture for easily adding actions and endpoints.

---

## 📁 Project Structure

```bash
├── main.py                   # Flask entry point
├── actions/                  # Scraping and automation logic
├── controller/               # Endpoint controllers
├── temp_downloads/           # Temporary downloads
├── utils/                    # Utilities and configuration
├── requirements.txt          # Python dependencies
├── Dockerfile                # Production-ready Docker image
├── .env.example              # Example environment configuration
└── README.md                 # This file
```

---

## ⚙️ Environment Variables

Configure scraper behavior via variables in the `.env` file. Copy `.env.example` to `.env` and customize as needed.

| Variable           | Required | Possible Values / Example                | Description                                                        |
|--------------------|----------|------------------------------------------|--------------------------------------------------------------------|
| `STAGE`            | Yes      | `production`, `testing`, `staging`       | Execution environment (affects visibility and real actions)        |
| `VALID_TOKEN`      | Yes      | `sample`                                 | Bearer token to authenticate requests                              |
| `HEADLESS_MODE`    | Optional | `auto`, `True`, `False`                  | Controls if the browser is visible or headless                     |
| `AUTO_DELETE_LOGS` | Optional | `True`, `False`                          | Automatically deletes old logs                                     |

> **Note:** See `.env.example` for more details and recommendations.
> **Base URL:** The base URL is now set in the constant `BASE_URL` inside `utils/config.py`.  
> To change the target site, edit the value of `BASE_URL` in that file.

---

## 🏁 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/Ismola/selenium-scraper-quickstarter.git
cd selenium-scraper-quickstarter
```

### 2. Set up your environment

- Copy `.env.example` to `.env` and edit it as needed.
- Make sure you have Python 3.x and Google Chrome installed.
- **Set the base URL:** Edit the `BASE_URL` constant in `utils/config.py` to point to your target website.

### 3. Choose your development mode

#### Option A: Dev Container (Recommended)

1. Install [VS Code](https://code.visualstudio.com/) and the **Dev Containers** extension.
2. Install [Docker](https://www.docker.com/).
3. Open the project in VS Code and select "Reopen in Container".

#### Option B: GitHub Codespaces

1. Click "Code" > "Open with Codespaces" on GitHub.
2. Wait for the environment to be set up automatically.

#### Option C: Manual

```bash
python3 -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
pip install -r requirements.txt
```

---

## ▶️ Running

### Local

```bash
python3 main.py
```

### Docker

```bash
docker build -t selenium-scraper .
docker run --env-file .env -p 3000:3000 selenium-scraper
```

### Production (Gunicorn)

```bash
gunicorn -w 2 -b 0.0.0.0:3000 --timeout 600 main:app
```

---

## ⚙️ CI/CD and Workflow Customization

- **Change environment variables for CI/CD:**
  - Go to **Settings > Secrets and variables > Actions** in your GitHub repository.
  - Add or update secrets like `STAGE`, `VALID_TOKEN` as needed.
  - These will be injected into the Docker image during the build and publish process.

> **⚠️ Important:**  
> If you publish the Docker image to a public registry, any environment variable (such as `STAGE`, `VALID_TOKEN`) injected during build may be visible to anyone who downloads the image.  
> **Never use production secrets or sensitive tokens in public images.**  
> For private deployments, always use private registries and restrict access to your images.

- **Change Docker registry or image name:**
  - Edit the `REGISTRY` and `IMAGE_NAME` variables in `.github/workflows/docker-publish.yml`.

- **Trigger the publish workflow:**
  - By default, the Docker image is published only after a successful run of the `Test` workflow.
  - You can change the trigger to run on other branches or events by editing the `on:` section.

> **Tip:** Adjust the port if you change the exposed port in `compose.yaml`.

---

## 🔗 API Usage

### Authentication

All protected routes require the header:

```curl
Authorization: Bearer <VALID_TOKEN>
```

### Default Endpoints

| Method | Route      | Description                        |
|--------|-----------|------------------------------------|
| GET    | `/`        | Server health check                |
| GET    | `/sample`  | Example endpoint (modifiable)      |

#### Example with `curl`

```bash
curl -H "Authorization: Bearer sample" http://localhost:3000/sample
```

---

## 🛠️ Customization & Extension

1. **Add your token in `.env`.**
2. **Set the base URL in `utils/config.py` by editing the `BASE_URL` constant.**
3. **Create new endpoints in `main.py`.**
4. **Implement scraping logic in `actions/` and controllers in `controller/`.**
5. **Use utilities from `utils/` for logging, configuration, and helpers.**

---

## 🧩 Architecture & Flow

1. **main.py:** Defines endpoints and starts Flask.
2. **controller/**: Receives the request, validates, and calls the action.
3. **actions/**: Executes scraping logic (Selenium).
4. **utils/**: Configuration, helpers, and shared utilities.  
   - **BASE_URL** is defined in `utils/config.py`.
5. **temp_downloads/**: Stores temporarily downloaded files.

---

## 🚢 Deployment

There are several recommended ways to deploy this project in a production environment.

> **⚠️ Important:** Always set `STAGE=production` in your environment before deploying. This disables Flask's debug mode and enables production-safe behaviour.

---

### 1. Pre-built Docker image from GHCR (Recommended)

A ready-to-use Docker image is published automatically to the GitHub Container Registry after every successful CI run. This is the fastest way to get the project running without cloning the source code.

**Pull the image:**

```bash
docker pull ghcr.io/ismola/asismetro-automations:latest
```

**Run the container directly:**

```bash
docker run -d \
  -p 3000:3000 \
  -e STAGE=production \
  -e VALID_TOKEN=your_secret_token \
  -v $(pwd)/logs:/app/logs \
  -v $(pwd)/temp_downloads:/app/temp_downloads \
  --name asismetro \
  ghcr.io/ismola/asismetro-automations:latest
```

**Or using an `.env` file:**

```bash
docker run -d \
  -p 3000:3000 \
  --env-file .env \
  -v $(pwd)/logs:/app/logs \
  -v $(pwd)/temp_downloads:/app/temp_downloads \
  --name asismetro \
  ghcr.io/ismola/asismetro-automations:latest
```

Example `.env` for production:

```env
STAGE=production
VALID_TOKEN=your_secret_token
PORT=3000
HEADLESS_MODE=True
BROWSER_LANGUAGE=en
AUTO_DELETE_LOGS=True
```

---

### 2. Docker Compose (Recommended for servers with persistent storage)

The repository includes a `compose.yaml` that wires up volumes, environment variables, and a health check automatically.

**Using the pre-built image (no build needed):**

Create a `compose.yaml` on your server:

```yaml
services:
  server:
    image: ghcr.io/ismola/asismetro-automations:latest
    ports:
      - 3000:3000
    container_name: asismetro
    volumes:
      - ./logs:/app/logs
      - ./temp_downloads:/app/temp_downloads
    restart: unless-stopped
    environment:
      - STAGE=production
      - VALID_TOKEN=your_secret_token
      - HEADLESS_MODE=True
```

Then run:

```bash
docker compose up -d
```

**Or clone the repo and build locally:**

```bash
git clone https://github.com/Ismola/asismetro-automations.git
cd asismetro-automations
cp .env.example .env   # edit .env and set STAGE=production
docker compose up --build -d
```

#### Volumes

| Host path | Container path | Purpose |
|-----------|----------------|---------|
| `./logs` | `/app/logs` | Persists application logs |
| `./temp_downloads` | `/app/temp_downloads` | Persists downloaded files |

---

### 3. Build your own Docker image

If you have modified the source code and want to build your own image:

```bash
docker build -t asismetro-automations .
docker run -d \
  -p 3000:3000 \
  -e STAGE=production \
  -e VALID_TOKEN=your_secret_token \
  asismetro-automations
```

---

### 4. Gunicorn (bare-metal / VPS without Docker)

The project is served by [Gunicorn](https://gunicorn.org/) inside the Docker image. You can also run it directly:

```bash
pip install -r requirements.txt
STAGE=production VALID_TOKEN=your_secret_token \
  gunicorn -w 2 -b 0.0.0.0:3000 --timeout 600 main:app
```

- `-w 2`: Number of worker processes (adjust to your CPU count).
- `-b 0.0.0.0:3000`: Binds to all interfaces on port 3000.
- `--timeout 600`: Increases timeout for long-running scraping tasks.

---

### Verify the deployment

After starting the container, check the health endpoint:

```bash
curl http://localhost:3000/
# Expected: selenium-scraper-quickstarter
```

> **Tip:** You can customize the exposed port and volume paths in `compose.yaml` as needed for your infrastructure.

---

## ⚙️ GitHub Actions CI/CD

This project includes a preconfigured GitHub Actions workflow for continuous integration and automated Docker image publishing. You can find the workflow files in `.github/workflows/`.

### Included Workflows

- **Docker Smoke (`docker-smoke.yml`):**
  - Builds the Docker image and verifies that the application starts correctly using Docker Compose.
  - Performs a smoke test by accessing the root endpoint (`/`) to ensure the container responds.

- **CI Test Suite (`ci-test.yml`):**
  - Runs after the smoke test.
  - Installs dependencies and runs automated tests with `pytest` inside the Docker Compose environment.
  - Ensures the application passes tests before continuing the pipeline.

- **Docker Build & Publish (`docker-publish.yml`):**
  - Runs only if the previous workflows are successful.
  - Builds and publishes the Docker image to GitHub Container Registry (`ghcr.io`).
  - Uses environment variables and secrets configured in the repository.

> ⚙️ You can customize or extend these workflows by editing the files in `.github/workflows/` as needed for your CI/CD requirements.

## 🧪 Automated Testing

The project includes automated tests located in the `test/` folder, using `pytest` and Flask's test client.

### 📂 Test Structure

- `test/test_main.py`: Tests for the main endpoints defined in `main.py`.

### ▶️ How to run the tests

1. Install dependencies if you haven't already:

   ```bash
   pip install -r requirements.txt
   pip install pytest
   ```

2. Run the tests:

   ```bash
   pytest --maxfail=1 --disable-warnings -v
   ```

> 💡 **Tip:** You can also run the tests automatically in the CI/CD flow with GitHub Actions.

### ✏️ How to modify or add tests?

- Edit or add files in the `test/` folder following the example in `test_main.py`.
- Use the Flask client to simulate HTTP requests and validate responses.
- To test new endpoints, create functions starting with `test_` and use the `client` fixture.
- See the [pytest documentation](https://docs.pytest.org/) for more options and best practices.

---

## 🐞 Troubleshooting

### Common error: `local variable 'driver' referenced before assignment`

- This may be due to incompatibility between Chrome and Chromedriver.
- Quick fix:
    1. Delete the drivers folder: `rm -rf ~/.wdm`
    2. Restart the environment.

### Other issues

- Ensure environment variables are correctly set.
- Check generated logs for more details.

---

## 📚 Resources & Bibliography

- [Selenium Python Docs](https://selenium-python.readthedocs.io/)
- [Flask Docs](https://flask.palletsprojects.com/en/3.0.x/)
- [Selenium Tutorial (YouTube)](https://youtube.com/playlist?list=PLheIVUbpfWZ17lCcHnoaa1RD59juFR06C)

---

## 🤝 Contributions

Pull requests and suggestions are welcome! Please open an issue to discuss major changes.

---

## 📝 License

MIT License © Ismola

---
