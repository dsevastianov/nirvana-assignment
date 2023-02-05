import statistics
import httpx
import asyncio
from flask import Flask

from flasgger import Swagger

def create_app():
    app = Flask(__name__)
    swag = Swagger(app)
    app.config['upstreams'] = [f"http://api{i}:5000" for i in [1,2,3]]

    
    @app.route('/member_id=<int:member_id>&strategy=<strategy>')
    async def get_aggregated(member_id, strategy):
        """
        Aggregate all numeric values retrieved from APIs using specified strategy.
        ---
        parameters:
          - name: member_id
            in: path
            description: Member ID
            type: integer
            required: true
          - name: strategy
            in: path
            description: Strategy to use for aggregation
            type: string
            enum: ['min', 'max', 'mean', 'median']
            required: true
        definitions:
            Aggregate:
                type: object
                properties:
                    deductible:
                        type: integer
                    stop_loss:
                        type: integer
                    oop_max:
                        type: integer
        responses:
            200:
                description: OK
                schema:
                    $ref: '#/definitions/Aggregate'                      
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
            res = await call_member_apis(member_id)
        except Exception as e:
            if app.debug:
                return f"Something's wrong: {e}", 500
            else:
                return f"Something's wrong", 500
        else:
            # Aggregate values for each attribute
            return { k: agg(v) for k,v in res.items() }

    async def call_member_apis(member_id):
        """
        Calls upstream APIs asynchronously and groups results by json properties.     
        Returns dictionary containing a list of values by json property.
        """
        async with httpx.AsyncClient() as client:
            tasks = [client.get(u + f"/member_id={member_id}") for u in app.config['upstreams']]
            rs = await asyncio.gather(*tasks)
        res={}
        for r in rs:
            for k,v in r.json().items():
                    if k in res:
                        res[k].append(v)
                    else:
                        res[k] = [v] 
        return res
        
    return app
