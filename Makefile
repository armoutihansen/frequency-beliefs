.PHONY: install test verify simulate consistency paper notebook reproduce clean

install:
	uv sync

test:
	uv run pytest -q tests/

verify:
	uv run python scripts/verify_regions.py

simulate:
	uv run python scripts/design_efficiency.py --final --draws 5000

consistency:
	uv run python scripts/consistency_check.py

paper:
	cd paper && latexmk -pdf -interaction=nonstopmode main.tex

notebook:
	uv run jupyter notebook notebooks/reproduce_analysis.ipynb

reproduce: install verify simulate consistency paper
	@echo
	@echo "Reproduction complete. Paper: paper/main.pdf"

clean:
	cd paper && latexmk -C
	rm -rf .pytest_cache notebooks/.ipynb_checkpoints
