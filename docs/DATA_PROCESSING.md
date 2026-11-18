# Data Processing and Privacy

## Local graph

Fork this repository to run the graph source in `src/unvibecode_graph/` locally. This mode does not upload your source code or require an API key.

## Hosted analysis through the Python package

The Python package selects eligible source files, uploads them to our hosted service over HTTPS, and downloads the reports. Repository mapping, context preparation, workflow analysis and risk analysis run on the server. Code context is sent to OpenAI for AI analysis.

Hosted AI analysis uses our OpenAI API credentials. We will introduce bring-your-own-key support shortly, so you can use your own API credentials.

## Data retention

We do not retain your uploaded source code or analysis results on our server after processing. Results are downloaded to your computer. OpenAI processes the AI requests under its own data policies.

## Before uploading

The package excludes common credential files, private-key files and generated directories. It does not redact secrets embedded in source files. Use `python -m unvibecode review --repository "/path/to/repository" --dry-run` to list the files selected for upload.

Review only repositories you are authorized to process. Remove sensitive information and follow your organization's third-party-processing policies.
