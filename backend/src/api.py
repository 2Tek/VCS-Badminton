from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_all, setup_db, Court, CourtRegistration
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

# Database reset for testing
db_drop_all()

# COURT ROUTES
# Create a new court
@app.route('/courts', methods=["POST"])
@requires_auth('post:court')
def create_court(payload):
    try:
        body = request.get_json()
        name = body.get('name')
        court_no = body.get('court_no')
        date = body.get('date')
        time = body.get('time')
        max_players = body.get('max_players')
        level = body.get('level')

        if not name or not court_no or not date or not time or not max_players or not level:
            abort(400, 'All fields are required.')

        # get the last court by id 
        court = Court.query.order_by(Court.id.desc()).first()
        if not court:
            id = 0
        else:
            id = court.id

        court = Court(
            id = id + 1,
            name=name,
            court_no=court_no,
            date=date,
            time=time,
            max_players=max_players,
            level=level
        )
        court.insert()

        return jsonify({
            'success': True,
            'court': court
        })
    except Exception as e:
        print(f"Create court exception: {e}")
        abort(422)

# Get all courts
@app.route('/courts', methods=["GET"])
@requires_auth('get:courts')
def get_courts(payload):
    try:
        courts = Court.query.order_by(Court.id).all()

        return jsonify({
            'success': True,
            'courts': courts
        })
    except Exception as e:
        print(f"Get courts exception: {e}")
        abort(422)

# Update a court
@app.route('/courts/<int:id>', methods=["PATCH"])
@requires_auth('patch:courts')
def update_court(payload, id):
    try:
        body = request.get_json()
        court = Court.query.get(id)

        if not court:
            abort(404)

        court.name = body.get('name', court.name)
        court.court_no = body.get('court_no', court.court_no)
        court.date = body.get('date', court.date)
        court.time = body.get('time', court.time)
        court.max_players = body.get('max_players', court.max_players)
        court.level = body.get('level', court.level)
        
        court.update()

        return jsonify({
            'success': True,
            'court': court
        })
    except Exception as e:
        print(f"Update court exception: {e}")
        abort(422)

# Delete a court
@app.route('/courts/<int:id>', methods=["DELETE"])
@requires_auth('delete:courts')
def delete_court(payload, id):
    try:
        court = Court.query.get(id)
        if not court:
            abort(404)

        court.delete()

        #delete all registrations for this court
        registrations = CourtRegistration.query.filter_by(court_id=id).all()
        for registration in registrations:
            registration.delete()

        return jsonify({
            'success': True,
            'delete': id
        })

    except Exception as e:
        print(f"Delete court exception: {e}")
        abort(422)

# COURT REGISTRATION ROUTES
# Register a player to a court
@app.route('/court-registrations', methods=["POST"])
@requires_auth('post:court-registration')
def create_court_registration(payload):
    try:
        body = request.get_json()
        court_id = body.get('court_id')
        name = body.get('name')
        player_unique_id = body.get('player_unique_id')
        role = body.get('role')

        if not court_id or not name or not player_unique_id:
            abort(400, 'All fields are required.')
        
        # get the last registration by id
        court_registration = CourtRegistration.query.order_by(CourtRegistration.id.desc()).first()
        if not court_registration:
            id = 0
        else:
            id = court_registration.id

        # get current time in SGT time zone to string
        reg_time = datetime.now(timezone('Asia/Singapore')).strftime('%Y-%m-%d %H:%M:%S')

        # get the max players of selected court
        court = Court.query.get(court_id)
        if not court:
            abort(404, 'Court not found.')
        else:
            max_players = court.max_players
        
        # get current number of players registered for selected court
        registrations = CourtRegistration.query.filter_by(court_id=court_id).all()

        # avoid duplicate registrations
        for registration in registrations:
                if registration.player_unique_id == player_unique_id and registration.name == name:
                    abort(400, 'Player already registered for this court.')
        
        # check if the court is full for registration to be added to waitlist
        if len(registrations) >= max_players:
            role = 'Waitlist'
        else:
            role = 'Player'

        court_registration = CourtRegistration(
            id = id + 1,
            court_id=court_id,
            name=name,
            player_unique_id=player_unique_id,
            role=role,
            reg_date_time=reg_time
        )
        court_registration.insert()

        return jsonify({
            'success': True,
            'court_registration': court_registration.long()
        })
    except Exception as e:
        print(f"Create court registration exception: {e}")
        abort(422)

# Get all registrations for a specific court
@app.route('/court-registrations/<int:court_id>', methods=["GET"])
@requires_auth('get:court-registrations')
def get_court_registrations(payload, court_id):
    try:
        registrations = CourtRegistration.query.filter_by(court_id=court_id).all()

        return jsonify({
            'success': True,
            'registrations': registrations
        })
    except Exception as e:
        print(f"Get court registrations exception: {e}")
        abort(422)

# Update a court registration
@app.route('/court-registrations/<string:player_unique_id>', methods=["PATCH"])
@requires_auth('patch:court-registrations')
def update_court_registration(payload, player_unique_id):
    try:
        body = request.get_json()
        registration = CourtRegistration.query.get(player_unique_id)

        if not registration:
            abort(404, 'Registration not found.')
        
        # get current time in SGT time zone to string
        reg_time = datetime.now(timezone('Asia/Singapore')).strftime('%Y-%m-%d %H:%M:%S')

        registration.name = body.get('name', registration.name)
        registration.role = body.get('role', registration.role)
        registration.reg_date_time = reg_time
        
        registration.update()

        return jsonify({
            'success': True,
            'registration': registration
        })
    except Exception as e:
        print(f"Update court registration exception: {e}")
        abort(422)

# Delete a court registration
@app.route('/court-registrations/<string:player_unique_id>', methods=["DELETE"])
@requires_auth('delete:court-registrations')
def delete_court_registration(payload, player_unique_id):
    try:
        registration = CourtRegistration.query.get(player_unique_id)
        if not registration:
            abort(404)

        registration.delete()

        return jsonify({
            'success': True,
            'delete': id
        })
    except Exception as e:
        print(f"Delete court registration exception: {e}")
        abort(422)
# Delete a court registration
@app.route('/court-registrations/<string:player_unique_id>', methods=["DELETE"])
@requires_auth('delete:court-registrations')
def delete_court_registration(payload, player_unique_id):
    try:
        registration = CourtRegistration.query.get(player_unique_id)
        if not registration:
            abort(404)

        registration.delete()

        return jsonify({
            'success': True,
            'delete': id
        })
    except Exception as e:
        print(f"Delete court registration exception: {e}")
        abort(422)

#Delete speicific court registration by court_id and name
@app.route('/court-registrations/<int:court_id>/<string:name>', methods=["DELETE"])
@requires_auth('delete:court-registrations')
def delete_court_registration_by_court_id_name(payload, court_id, name):
    try:
        registration = CourtRegistration.query.filter_by(court_id=court_id, name=name).first()
        if not registration:
            abort(404)

        registration.delete()

        return jsonify({
            'success': True,
            'delete': id
        })
    except Exception as e:
        print(f"Delete court registration exception: {e}")
        abort(422)

# Error handling
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"
    }), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422

@app.errorhandler(AuthError)
def handle_auth_error(error):
    response = jsonify(error.error)
    response.status_code = error.status_code
    return response