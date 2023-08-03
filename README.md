# CogSearchwithAzureOpenAI
This repository has Python notebook scripts that can be helpful when working with Azure OpenAI

1. The 'Chunk data create embeddings then upload to Azure Blob Publish' script will take a source directory in Azure blob storage and then download and chunk up the documents in it based on the chunking parameters you provide. It will then create embeddings for the chunks, then upload a resulting JSON file for each chunk that contains the chunked content and associated embeddings back to a destination directory in Azure Blob storage. It will also create an Azure Cognitive Search index, indexer, and data source you can use to easily pull in the data to Azure Cognitive Search. Once the entire script has run just run the indexer in Azure Cognitive search and it will automatically pull in the chunked JSON files. Make sure to have Azure Cognitive Search Semantic Search turned on.

2. The 'Chunk data then upload to Azure Blob - No Embeddings Publish' script will take a source directory in Azure blob storage and then download and chunk up the documents in it based on the chunking parameters you provide. It will then upload a resulting JSON file for each chunk that contains the chunked content back to a destination directory in Azure Blob storage. It will also create an Azure Cognitive Search index, indexer, and data source you can use to easily pull in the data to Azure Cognitive Search. Once the entire script has run just run the indexer in Azure Cognitive search and it will automatically pull in the chunked JSON files. Make sure to have Azure Cognitive Search Semantic Search turned on. **The Resulting JSON files and Azure Search Index can easily be used with the 'Azure OpenAI on your Data' service.**

Both of the scripts support parsing and chunking documents in the following formats:
*PDF
*JPEG / PNG / 
*Word / Excel / Powerpoint
*HTML