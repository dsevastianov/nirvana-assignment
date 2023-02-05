import random
from flask import Flask

def create_app():        
    app = Flask(__name__)

    @app.route('/member_id=<member_id>')
    def get_member_info(member_id):
        r = dict(
                deductible=1000 + random.randrange(-100, 100), 
                stop_loss=10000 + random.randrange(-5000, 5000), 
                oop_max=5000 + random.randrange(-1000, 1000))
        app.logger.warn(r)
        return r
    
    return app