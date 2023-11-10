from config.connect_elasticsearch import es
from fastapi.responses import JSONResponse
from fuzzywuzzy import fuzz


async def search_data(keyword):
    search_query = {
        "query": {
            "multi_match": {
                "query": keyword,
                "fields": ["erp_nm_item", "erp_cd_item"]
            }
        }
    }

    index_name = "index_item"

    # Perform the search
    try:
        response = es.search(index=index_name, body=search_query)
        hits = response["hits"]["hits"]

        if hits:

            # Use the custom mapping function to transform the data
            mapped_results = map_search_results(hits, keyword)

            return JSONResponse(content={"results": mapped_results})
        else:
            return JSONResponse(content={"results": "No data"}, status_code=200)


    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


# Define a custom mapping function
def map_search_results(hits, keyword):
    mapped_results = []

    for idx, hit in enumerate(hits, start=1):
        source = hit["_source"]
        product_name = source["erp_nm_item"]

        # Calculate the similarity score using fuzzywuzzy fuzz.ratio
        similarity_score = fuzz.ratio(keyword, product_name)
        similarity_score_percentage = f"{similarity_score}%"

        # Include both the Elasticsearch _score and the similarity score
        mapped_result = {
            "NO": idx,
            "erp_nm_item": source["erp_cd_item"],
            "erp_cd_item": product_name,
            "standard": source["standard"],
            "item_id": source["item_id"],
            "score": hit["_score"],
            "similarity_score_percentage": similarity_score_percentage
        }
        mapped_results.append(mapped_result)

    return mapped_results
