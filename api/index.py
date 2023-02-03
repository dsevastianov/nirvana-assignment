import random
from flask import Flask

app = Flask(__name__)

@app.route('/member_id=<member_id>')
def get_member_info(member_id):
    return dict(
            deductible=1000 + random.randrange(-100, 100), 
            stop_loss=10000 + random.randrange(-5000, 5000), 
            oop_max=5000 + random.randrange(-1000, 1000) 
    )
   