.PHONY: tests help init_env init_git pre-commit_update docs_view docs_test test check

####----Basic configurations----####

install_env: ## Install libs with UV and pre-commit
	@echo "🚀 Creating virtual environment using UV"
	uv sync --all-groups
	@echo "🚀 Installing pre-commit..."
	uv run pre-commit install
	@echo "💻 Activate virtual environment..."
	@bash -c "source .venv/bin/activate"

init_git: ## Initialize git repository
	@echo "🚀 Initializing local git repository..."
	git init -b main
	git add .
	git commit -m "🎉 Initial commit"
	@echo "🚀 Local Git already set!"

####----Install Libraries----####

install_data_libs: ## Install pandas, scikit-learn, Jupyter, seaborn
	@echo "🚀 Installing data science libraries..."
	uv add "pandas[parquet]" numpy scipy scikit-learn
	@echo "🚀 Installing Jupyter, matplotlib and seaborn in dev..."
	uv add jupyter matplotlib seaborn --group dev


####----Tests----####
test: ## Test the code with pytest and coverage
	@echo "🚀 Testing code: Running pytest"
	@uv run pytest --cov

test_verbose: ## Test the code with pytest and coverage in verbose mode
	@echo "🚀 Testing code: Running pytest in verbose mode"
	@uv run pytest --no-header -v --cov

test_coverage: ## Test coverage report coverage.xml
	@echo "🚀 Testing code: Running pytest with coverage"
	@uv run pytest --cov --cov-report xml:coverage.xml

####----Pre-commit----####
pre-commit_update: ## Update pre-commit hooks
	@echo "🚀 Updating pre-commit hooks..."
	uv run pre-commit clean
	uv run pre-commit autoupdate

#
####----Docs----####
docs: ## Build and serve the documentation
	@echo "🚀 Viewing documentation..."
	uv run mkdocs serve

docs_test: ## Test if documentation can be built without warnings or errors
	@uv run mkdocs build -s
#

####----Clean----####
clean_env: ## Clean .venv virtual environment
	@echo "🚀 Cleaning the environment..."
	@[ -d .venv ] && rm -rf .venv || echo ".venv directory does not exist"

####----Git----####
switch_main: ## Switch to main branch and pull
	@echo "🚀 Switching to main branch..."
	@git switch main
	@git pull

clean_branchs: ## Clean local branches already merged on the remote
	@echo "🚀 Cleaning up merged branches..."
	@git fetch -p
	@for branch in $$(git for-each-ref --format '%(refname:short)' refs/heads/ | grep -v '^\*' | grep -v ' main$$'); do \
		if ! git show-ref --quiet refs/remotes/origin/$$branch; then \
			if git config --get branch.$$branch.remote > /dev/null 2>&1; then \
				echo "Deleting local branch $$branch"; \
				git branch -D $$branch; \
			fi \
		fi \
	done

####----Checks----####
check: ## Run code quality tools with pre-commit hooks.
	@echo "🚀 Linting, formating and Static type checking code: Running pre-commit"
	@uv run pre-commit run -a

lint: ## Run code quality tools with pre-commit hooks.
	@echo "🚀 Linting, formating and Static type checking code: Running pre-commit"
	@uv run pre-commit run ruff

####----Modelado y despliegue (Entrega 03/04)----####
regenerate_models: ## Reentrena/persiste modelos y artefactos en orden (07->08->09 + labels + stats)
	@echo "🚀 Regenerando artefactos (segmentacion -> churn -> interpretacion)..."
	MPLBACKEND=Agg uv run python execute_notebook.py "notebooks/5-models/07-gc-clustering-2026_04_15.ipynb"
	MPLBACKEND=Agg uv run python execute_notebook.py "notebooks/5-models/08-gc-churn-2026_04_16.ipynb"
	MPLBACKEND=Agg uv run python execute_notebook.py "notebooks/6-interpretation/09-gc-analisis_segmentos-2026_04_16.ipynb"
	uv run python deploy/build_cluster_labels.py
	uv run python deploy/build_feature_stats.py
	@echo "✅ Artefactos en data/06_models/ y data/07_model_output/"

serve_api: ## Levanta la API REST (FastAPI) en el puerto 8000
	@echo "🚀 API en http://localhost:8000/docs"
	uv run uvicorn api.main:app --host 0.0.0.0 --port 8000

serve_app: ## Levanta la interfaz Streamlit en :8501 (consume la API via API_URL)
	@echo "🚀 Interfaz en http://localhost:8501"
	API_URL=$${API_URL:-http://localhost:8000} uv run streamlit run notebooks/7-deploy/streamlit_app.py --server.port 8501

####----Project----####
help:
	@printf "%-30s %s\n" "Target" "Description"
	@printf "%-30s %s\n" "-----------------------" "----------------------------------------------------"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' Makefile | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help
