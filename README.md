# Self-Building Site

This repository contains the codebase for an autonomous, self-improving multi-agent system that designs, builds, tests, and deploys a public-facing website devoted to long-term, humanity-benefitting projects.

## Project Structure

- `frontend/`: Next.js + TailwindCSS application
- `backend/`: Python FastAPI application
- `agents/`: Contains the Orchestrator, Builder, Tester, and Critic agents
- `checkpoints/`: Stores architectural checkpoints and change logs
- `logs/`: Stores agent activity logs
- `principles/`: Contains JSON files for core principles (e.g., `principles.json`)
- `tests/`: End-to-end tests
- `.github/workflows/`: GitHub Actions CI/CD pipelines

## Getting Started

### Prerequisites

- Node.js (LTS) and npm/yarn
- Python 3.9+
- Git

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/<your-user>/selfbuilding-site.git
    cd selfbuilding-site
    ```

2.  **Frontend Setup:**

    ```bash
    cd frontend
    npm install # or yarn install
    ```

3.  **Backend Setup:**

    ```bash
    cd ../backend
    pip install -r requirements.txt
    ```

### Running Locally

1.  **Environment Variables:**

    Create a `.env` file in the root directory of the project with the following environment variables:

    ```
    OPENAI_API_KEY=your_openai_api_key_here
    GITHUB_TOKEN=your_github_pat_here
    # Add other environment variables as needed for specific modules
    ```

2.  **Start Frontend:**

    ```bash
    cd frontend
    npm run dev # or yarn dev
    ```

3.  **Start Backend:**

    ```bash
    cd backend
    uvicorn main:app --reload
    ```

## CI/CD

This project uses GitHub Actions for continuous integration and deployment. Workflows are defined in the `.github/workflows/` directory.

## Deployment

- **Frontend**: Deployed to Vercel.
- **Backend**: Deployed to Render.com.

## Licensing

This project is licensed under the MIT License. See the `LICENSE` file for details.


