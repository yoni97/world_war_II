from datetime import datetime

import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from database.db import db_session
from models.all_cities import CityModel
from models.countries import CountryModel
from models.missions import MissionModel
from models.targets import TargetModel
from models.targettypes import TargetTypeModel


class City(SQLAlchemyObjectType):
    class Meta:
        model = CityModel
        interfaces = (graphene.relay.Node,)

class Country(SQLAlchemyObjectType):
    class Meta:
        model = CountryModel
        interfaces = (graphene.relay.Node,)

class Mission(SQLAlchemyObjectType):
    class Meta:
        model = MissionModel
        interfaces = (graphene.relay.Node,)

class Target(SQLAlchemyObjectType):
    class Meta:
        model = TargetModel
        interfaces = (graphene.relay.Node,)

class TargetType(SQLAlchemyObjectType):
    class Meta:
        model = TargetTypeModel
        interfaces = (graphene.relay.Node,)

class Query(graphene.ObjectType):
    country_by_id = graphene.Field(Country, id=graphene.Int(required=True))
    mission_by_id = graphene.Field(Mission, id=graphene.Int(required=True))
    missions_between_dates = (graphene.List(Mission,
            start_date=graphene.String(required=True), end_date=graphene.String(required=True)))
    missions_by_country = graphene.List(Mission, country_id=graphene.Int(required=True))
    missions_by_target_industry = graphene.List(Mission, target_industry=graphene.String(required=True))

    @staticmethod
    def resolve_country_by_id(root, info, id):
        country = db_session.query(CountryModel).get(id)
        if country:
            return country
        return None

    @staticmethod
    def resolve_mission_by_id(root, info, id):
        mission = db_session.query(MissionModel).get(id)
        if mission:
            return mission
        return None

    @staticmethod
    def resolve_missions_between_dates(root, info, start_date, end_date):
        session = db_session()
        start = datetime.strptime(start_date, '%Y-%m-%d').date()
        end = datetime.strptime(end_date, '%Y-%m-%d').date()
        return (
            session.query(MissionModel)
            .filter(MissionModel.mission_date >= start)
            .filter(MissionModel.mission_date <= end)
            .all()
        )

    @staticmethod
    def resolve_missions_by_country(self, info, country_id):
        session = db_session()
        return (
            session.query(Mission)
            .join(Mission.targets)
            .join(Target.city)
            .join(City.country)
            .filter(Country.country_id == country_id)
            .all()
        )

    @staticmethod
    def resolve_missions_by_target_industry(self, info, target_industry):
        session = db_session()
        return (
            session.query(Mission)
            .join(Mission.targets)
            .filter(TargetModel.target_industry == target_industry)
            .all()
        )

    ###############################



# Mutations

class AddAMission(graphene.Mutation):
    class Arguments:
        mission_id = graphene.Int(required=True)
        mission_date = graphene.Date(required=True)
        airborne_aircraft = graphene.Float(required=True)
        attacking_aircraft = graphene.Float(required=True)
        bombing_aircraft = graphene.Float(required=True)
        aircraft_returned = graphene.Float(required=True)
        aircraft_failed = graphene.Float(required=True)
        aircraft_damaged = graphene.Float(required=True)
        aircraft_lost = graphene.Float(required=True)

    address = graphene.Field(lambda: MissionModel)

    def mutate(self, info, mission_id, mission_date, airborne_aircraft, attacking_aircraft, bombing_aircraft, aircraft_returned, aircraft_failed, aircraft_damaged, aircraft_lost):
        new_mission = MissionModel(mission_id=mission_id, mission_date=mission_date, aircraft_lost=aircraft_lost
                                   , aircraft_returned=aircraft_returned, aircraft_failed=aircraft_failed,
                                   aircraft_damaged=aircraft_damaged, airborne_aircraft=airborne_aircraft,
                                   attacking_aircraft=attacking_aircraft, bombing_aircraft=bombing_aircraft)
        db_session.add(new_mission)
        db_session.commit()
        return AddAMission(address=new_mission)

# class AddUser(graphene.Mutation):
#     class Arguments:
#         name = graphene.String(required=True)
#         birth_date = graphene.String(required=True)  # Format: 'YYYY-MM-DD'
#         address_id = graphene.Int(required=False)
#
#     user = graphene.Field(lambda: User)
#
#     def mutate(self, info, name, birth_date, address_id=None):
#         try:
#             birth_date_obj = datetime.strptime(birth_date, '%Y-%m-%d').date()
#         except ValueError:
#             raise Exception("Invalid birth date format. Expected 'YYYY-MM-DD'")
#         new_user = UserModel(name=name, birth_date=birth_date_obj, address_id=address_id)
#         db_session.add(new_user)
#         db_session.commit()
#         return AddUser(user=new_user)
#
#
# class UpdateUserName(graphene.Mutation):
#     class Arguments:
#         user_id = graphene.Int(required=True)
#         new_name = graphene.String(required=True)
#
#     user = graphene.Field(lambda: User)
#
#     def mutate(self, info, user_id, new_name):
#         user = db_session.query(UserModel).get(user_id)
#         if not user:
#             raise Exception("User not found")
#         user.name = new_name
#         db_session.commit()
#         return UpdateUserName(user=user)
#
#
# class DeleteAddress(graphene.Mutation):
#     class Arguments:
#         address_id = graphene.Int(required=True)
#
#     ok = graphene.Boolean()
#
#     def mutate(self, info, address_id):
#         address = db_session.query(AddressModel).get(address_id)
#         if not address:
#             return DeleteAddress(ok=False)
#         db_session.delete(address)
#         db_session.commit()
#         return DeleteAddress(ok=True)
#
#
# class DeleteSubject(graphene.Mutation):
#     class Arguments:
#         subject_id = graphene.Int(required=True)
#
#     ok = graphene.Boolean()
#
#     def mutate(self, info, subject_id):
#         subject = db_session.query(SubjectModel).get(subject_id)
#         if not subject:
#             return DeleteSubject(ok=False)
#         db_session.delete(subject)
#         db_session.commit()
#         return DeleteSubject(ok=True)
#
#
# class DeleteUser(graphene.Mutation):
#     class Arguments:
#         user_id = graphene.Int(required=True)
#
#     ok = graphene.Boolean()
#
#     def mutate(self, info, user_id):
#         user = db_session.query(UserModel).get(user_id)
#         if not user:
#             return DeleteUser(ok=False)
#         db_session.delete(user)
#         db_session.commit()
#         return DeleteUser(ok=True)
#
#
# class Mutation(graphene.ObjectType):
#     add_address = AddAddress.Field()
#     add_user = AddUser.Field()
#     update_user_name = UpdateUserName.Field()
#     delete_address = DeleteAddress.Field()
#     delete_subject = DeleteSubject.Field()
#     delete_user = DeleteUser.Field()



schema = graphene.Schema(query=Query)
