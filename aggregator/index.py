import statistics
import requests
import aggregator

app = aggregator.create_app()

@app.route('/member_id=<int:member_id>&strategy=<strategy>')
def get_aggregated(member_id, strategy):
    """
    Aggregates all numeric values retrieved from APIs using specified strategy
    """
    match strategy:
        case 'min': 
            agg = min
        case 'max': 
            agg = max
        case 'mean': 
            agg = statistics.mean
        case 'median': 
            agg = statistics.median
        case x:
            return f"{x} is unsupported!", 400

    try:
        res = call_member_apis(member_id)
    except Exception as e:
        if app.debug:
            return f"Something's wrong: {e}", 500
        else:
            return f"Something's wrong", 500
    else:
        # Aggregate values for each attribute
        return { k: agg(v) for k,v in res.items() }

def call_member_apis(member_id):
    """
    Calls upstream APIs and groups results by json properties.     
    Returns dictionary containing a list of values by json property.
    """
    res={}
    for api in app.config['upstreams']:
        r = requests.get(api + f"/member_id={member_id}")     
        for k,v in r.json().items():
            if k in res:
                res[k].append(v)
            else:
                res[k] = [v]
    return res
    

