FROM python:3.11-slim

LABEL org.opencontainers.image.description="LaTeX Index Insertion Tool"
LABEL org.opencontainers.image.source="https://github.com/user/latex-index-tool"

RUN pip install --no-cache-dir pyyaml

WORKDIR /app
COPY latex_index/ latex_index/
COPY pyproject.toml .

RUN pip install --no-cache-dir -e .

ENTRYPOINT ["latex-index"]
CMD ["--help"]
