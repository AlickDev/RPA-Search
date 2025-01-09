from config.connect_elasticsearch import es
from fastapi.responses import JSONResponse
from fuzzywuzzy import fuzz


async def search_data(keyword):
    if not keyword:
        return JSONResponse(content={"error": "Keyword is required"}, status_code=400)
    cd_item_query_one = {
        "query": {
            "bool": {
                "must": [
                    {
                        "match_phrase": {
                            "erp_cd_item": keyword,
                        }
                    },
                    {
                        "match": {
                            "use_yn": "Y" 
                        }
                    }
                ]
            }
        },
        "size": 1
    }
    nm_item_query = {
        "query": {
            "bool": {  
                "must": [
                    {
                        "match": {
                            "erp_nm_item": keyword,
                        }
                    },
                    {
                        "match": {
                            "use_yn": "Y"  
                        }
                    }
                ]
            }
        },
        "size": 1000
    }

    index_name = "index_item"

    try:
        cd_item_response_one = es.search(
            index=index_name, body=cd_item_query_one
        )
        cd_item_hits_one = cd_item_response_one["hits"]["hits"]

        if cd_item_hits_one and any(c.isdigit() or c.isalpha() for c in keyword) and len(keyword) == 7:
            results = process_results(cd_item_hits_one, [], keyword)
        else:
            nm_item_response = es.search(index=index_name, body=nm_item_query)
            nm_item_hits = nm_item_response["hits"]["hits"]
            results = process_results([], nm_item_hits, keyword)

        return JSONResponse(content={"results": results}, status_code=200)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

def process_results(cd_item_hits, nm_item_hits, keyword):
    mapped_results = []
    
    # Process erp_cd_item results
    for idx, cd_hit in enumerate(cd_item_hits, start=1):
        source = cd_hit["_source"]
        product_code = source["erp_cd_item"]
        
        similarity_score = fuzz.ratio(keyword, product_code)
        similarity_score_percentage = f"{similarity_score}%"
        
        mapped_result = {
            "NO": idx,
            "erp_nm_item": source["erp_nm_item"],
            "erp_cd_item": product_code,
            "standard": source["standard"],
            "item_id": source["item_id"],
            "score": cd_hit["_score"],
            "similarity_score_percentage": similarity_score_percentage,
            "use_yn": source["use_yn"],
        }
        mapped_results.append(mapped_result)

    # Process erp_nm_item results
    for idx, nm_hit in enumerate(nm_item_hits, start=len(cd_item_hits) + 1):
        source = nm_hit["_source"]
        product_name = source["erp_nm_item"]

        # Calculate the similarity score using fuzzywuzzy fuzz.ratio
        similarity_score = fuzz.ratio(keyword, product_name)
        similarity_score_percentage = f"{similarity_score}%"

        mapped_result = {
            "NO": idx,
            "erp_nm_item": product_name,
            "erp_cd_item": source["erp_cd_item"],
            "standard": source["standard"],
            "item_id": source["item_id"],
            "score": nm_hit["_score"],
            "similarity_score_percentage": similarity_score_percentage,
            "use_yn": source["use_yn"],
        }
        mapped_results.append(mapped_result)

    return mapped_results



# fetch data index order goods match
async def get_data_index_order_goods_match(page: int = 1, page_size: int = 100):
    if page < 1 or page_size < 1:
        raise ValueError("Page and page_size must be greater than 0")
    
    index_name = "index_order_goods_match"
    
    # Calculate the 'from' parameter based on page and page_size
    from_param = (page - 1) * page_size

    # Elasticsearch query with pagination
    query = {
        "query": {
            "match_all": {}
        },
        "from": from_param,
        "size": page_size
    }

    try:
        # Perform Elasticsearch search
        response = es.search(index=index_name, body=query)
        hits = response["hits"]["hits"]
        total_count = response["hits"]["total"]["value"] 

        # Map the desired fields for each hit
        mapped_results = []
        for hit in hits:
            source = hit["_source"]
            mapped_result = {
                "item_id": source.get("item_id", ""),
                "ch_item_cd": source.get("ch_item_cd", ""),
                "name": source.get("name", ""),
                "erp_cd_item": source.get("erp_cd_item", "")
            }
            mapped_results.append(mapped_result)

        if mapped_results:
            # Return the mapped results with pagination metadata and total count
            return JSONResponse(content={
                "page": page,
                "page_size": page_size,
                "total_count": total_count,  
                "results": mapped_results
            })
        else:
            return JSONResponse(content={"results": "No data"}, status_code=200)

    except Exception as e:
        # Handle Elasticsearch search exception
        return JSONResponse(content={"error": str(e)}, status_code=500)
    
    
