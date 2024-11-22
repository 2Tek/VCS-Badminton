from flask import Flask, request, jsonify, abort
from flask_migrate import Migrate

from sqlalchemy import exc, desc
import json
from flask_cors import CORS
from datetime import datetime
from pytz import timezone

from .database.models import db, db_drop_all, setup_db, Court, CourtRegistration
from .auth.auth import AuthError, requires_auth, check_permissions

app = Flask(__name__)
setup_db(app)
migrate = Migrate(app, db)
#db_drop_all()
CORS(app)


# COURT ROUTES
def create_court_helper(body):
    try:
        new_id = body.get('id')
        name = body.get('name')
        court_no = body.get('court_no')
        date = body.get('date')
        time = body.get('time')
        max_players = body.get('max_players')
        level = body.get('level')

        if not name or not court_no or not date or not time or not max_players or not level:
            abort(400, 'All fields are required.')

        court = Court(
            id = new_id,
            name=name,
            court_no=court_no,
            date=date,
            time=time,
            max_players=max_players,
            level=level
        )
        court.insert()

        #get the court by id to confirm data has been updated
        court = Court.query.get(new_id)
        # Convert the court object to a dictionary for JSON serialization
        court_data = {
            'id': court.id,
            'name': court.name,
            'court_no': court.court_no,
            'date': court.date,
            'time': court.time,
            'max_players': court.max_players,
            'level': court.level
        }

        return jsonify({
            'success': True,
            'court': court_data
        })
    except Exception as e:
        print(f"Create court helper exception: {e}")
        abort(422)

# Create a new court
@app.route('/courts', methods=["POST"])
@requires_auth('post:court')
def create_court(payload):
    try:
        body = request.get_json()
        print("Request Body: ",body)
        name = body.get('name')
        court_no = body.get('court_no')
        date = body.get('date')
        time = body.get('time')
        max_players = body.get('max_players')
        level = body.get('level')

        if not name or not court_no or not date or not time or not max_players or not level:
            abort(400, 'All fields are required.')

        # get the last court by id 
        # Determine the new court's ID
        court = Court.query.order_by(desc(Court.id)).first()
        new_id = (court.id + 1) if court else 1
        #assign new court id to the body
        body['id'] = new_id

        print("New body: ",body)

        return create_court_helper(body)
    except Exception as e:
        print(f"Create court exception: {e}")
        abort(422)

# Get all courts
@app.route('/courts', methods=["GET"])
@requires_auth('get:courts')
def get_courts(payload):
    try:
        courts = Court.query.order_by(Court.id).all()
        # Convert courts to JSON serializable format
        formatted_courts = [
            {
                'id': court.id,
                'name': court.name,
                'court_no': court.court_no,
                'date': court.date,
                'time': court.time,
                'max_players': court.max_players,
                'level': court.level
            }
            for court in courts
        ]

        return jsonify({
            'success': True,
            'courts': formatted_courts
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
            # If the court is not found, create new court with the given payload
            print("Court not found. Creating new court", body)
            return create_court_helper(body)

        court.name = body.get('name', court.name)
        court.court_no = body.get('court_no', court.court_no)
        court.date = body.get('date', court.date)
        court.time = body.get('time', court.time)
        court.max_players = body.get('max_players', court.max_players)
        court.level = body.get('level', court.level)
        
        court.update()

        #get the court by id to confirm data has been updated
        court = Court.query.get(id)
        # Convert the court object to a dictionary for JSON serialization
        court_data = {
            'id': court.id,
            'name': court.name,
            'court_no': court.court_no,
            'date': court.date,
            'time': court.time,
            'max_players': court.max_players,
            'level': court.level
        }

        return jsonify({
            'success': True,
            'court': court_data
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
        
        #update registration fee for all players who have more than 1 registration
        all_registrations = CourtRegistration.query.all()
        for registration in all_registrations:
            #get all registrations for this player, order by id
            player_registrations = CourtRegistration.query.filter_by(player_unique_id=registration.player_unique_id, name=registration.name).order_by(CourtRegistration.id).all()
            if len(player_registrations) > 0:
                for i, player_registration in enumerate(player_registrations):
                    print("i: ",i)
                    if i == 0:
                        player_registration.fee = None
                        player_registration.update()
                    if i > 0:
                        player_registration.fee = '$'
                        player_registration.update()

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
        predefine_role = body.get('role')

        if not court_id or not name or not player_unique_id:
            abort(400, 'All fields are required.')
        
        # get the last reg by id 
        # Determine the new reg's ID
        reg = CourtRegistration.query.order_by(desc(CourtRegistration.id)).first()
        new_id = (reg.id + 1) if reg else 1

        # get how many registration from same player based on name and unique id
        previous_reg = CourtRegistration.query.filter_by(player_unique_id=player_unique_id, name=name).all()
        if len(previous_reg) >= 1:
            fee = '$'
        else:
            fee = None


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
        if predefine_role:
            role = predefine_role
        elif len(registrations) >= max_players:
            role = 'Waitlist'
        else:
            role = 'Player'       

        court_registration = CourtRegistration(
            id = new_id,
            court_id=court_id,
            name=name,
            player_unique_id=player_unique_id,
            role=role,
            reg_date_time=reg_time,
            fee=fee
        )
        court_registration.insert()

        #get court registration by id to confirm data has been updated
        court_registration = CourtRegistration.query.get(new_id)
        #format court registration to JSON serializable format
        court_registration = {
            'id': court_registration.id,
            'court_id': court_registration.court_id,
            'name': court_registration.name,
            'player_unique_id': court_registration.player_unique_id,
            'role': court_registration.role,
            'reg_date_time': court_registration.reg_date_time,
            'fee': court_registration.fee
        }

        return jsonify({
            'success': True,
            'court_registration': court_registration
        })
    except Exception as e:
        print(f"Create court registration exception: {e}")
        abort(422)
# Get all registrations from all court
@app.route('/court-registrations', methods=["GET"])
@requires_auth('get:court-registrations')
def get_all_registrations(payload):
    try:
        # get all available courts
        courts = Court.query.order_by(Court.id).all()
        # for each court, use its court_id to get all registrations
        all_registrations = []
        for court in courts:
            registrations = CourtRegistration.query.filter_by(court_id=court.id).all()
            #format registrations to JSON serializable format
            formatted_registrations = [
                {
                    'id': registration.id,
                    'court_id': registration.court_id,
                    'name': registration.name,
                    'player_unique_id': registration.player_unique_id,
                    'role': registration.role,
                    'reg_date_time': registration.reg_date_time,
                    'fee': registration.fee
                }
                for registration in registrations
            ]
            all_registrations.append(formatted_registrations)

        return jsonify({
            'success': True,
            'registrations': all_registrations
        })
    except Exception as e:
        print(f"Get all registrations exception: {e}")
        abort(422)
# Get all registrations for a specific court
@app.route('/court-registrations/<int:court_id>', methods=["GET"])
@requires_auth('get:court-registrations')
def get_court_registrations(payload, court_id):
    try:
        registrations = CourtRegistration.query.filter_by(court_id=court_id).all()
        #format registrations to JSON serializable format
        formatted_registrations = [
            {
                'id': registration.id,
                'court_id': registration.court_id,
                'name': registration.name,
                'player_unique_id': registration.player_unique_id,
                'role': registration.role,
                'reg_date_time': registration.reg_date_time,
                'fee': registration.fee
            }
            for registration in registrations
        ]

        return jsonify({
            'success': True,
            'registrations': formatted_registrations
        })
    except Exception as e:
        print(f"Get court registrations exception: {e}")
        abort(422)

# Update a court registration
# There is some room to update this route to allow for updating the role of a player
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
        registration.reg_date_time = reg_time
        
        registration.update()

        #get court registration by id to confirm data has been updated
        registration = CourtRegistration.query.get(player_unique_id)
        #format court registration to JSON serializable format
        registration = {
            'id': registration.id,
            'court_id': registration.court_id,
            'name': registration.name,
            'player_unique_id': registration.player_unique_id,
            'role': registration.role,
            'reg_date_time': registration.reg_date_time,
            'fee': registration.fee
        }

        return jsonify({
            'success': True,
            'registration': registration
        })
    except Exception as e:
        print(f"Update court registration exception: {e}")
        abort(422)

# Delete a court registration
@app.route('/court-registrations/<int:id>', methods=["DELETE"])
@requires_auth('delete:court-registrations')
def delete_court_registration(payload, id):
    try:
        reg = CourtRegistration.query.get(id)
        if not reg:
            abort(404)
        
        #get sub from payload, then check if the sub is the same as the player_unique_id
        sub = payload['sub']
        if reg.player_unique_id != sub and not ('post:court' in payload['permissions'] or '*:*' in payload['permissions']):
            abort(403, 'Forbidden. You are not allowed to delete this registration.')

        reg.delete()

        # get all remain registrations for this court
        registrations = CourtRegistration.query.filter_by(court_id=reg.court_id).all()
        # get max players for this court
        court = Court.query.get(reg.court_id)
        max_players = court.max_players
        # reassign role based on max players
        for i, registration in enumerate(registrations):
            if i < max_players:
                registration.role = 'Player'
            else:
                registration.role = 'Waitlist'
            registration.update()
        
        # get all registrations of all courts, for each player who has more than 1 registration, set fee to '$' for the second registration onwards
        # only set fee from the second registration onwards, the first registration is free
        all_registrations = CourtRegistration.query.filter_by(player_unique_id=reg.player_unique_id).all()
        for registration in all_registrations:
            #get all registrations for this player, order by id
            player_registrations = CourtRegistration.query.filter_by(player_unique_id=registration.player_unique_id, name=registration.name).order_by(CourtRegistration.id).all()
            if len(player_registrations) > 0:
                for i, player_registration in enumerate(player_registrations):
                    print("i: ",i)
                    if i == 0:
                        player_registration.fee = None
                        player_registration.update()
                    if i > 0:
                        player_registration.fee = '$'
                        player_registration.update()

        return jsonify({
            'success': True,
            'delete': id
        })

    except Exception as e:
        print(f"Delete registration exception: {e}")
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