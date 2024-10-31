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
                                            start_date=graphene.String(required=True),
                                            end_date=graphene.String(required=True)))
    # find mission by country
    missions_by_country = graphene.List(Mission, country_id=graphene.Int(required=True))
    # find mission by target industry
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
    def resolve_missions_between_dates(root, info, start_date=None, end_date=None):
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



    # def resolve_users_by_name(self, info, name_substring):
    #     substring = f"%{name_substring}%"
    #     return db_session.query(UserModel).filter(
    #         UserModel.name.ilike(substring)
    #     ).all()
    #
    # def resolve_subjects_by_name(self, info, name_substring):
    #     substring = f"%{name_substring}%"
    #     return db_session.query(SubjectModel).filter(
    #         SubjectModel.name.ilike(substring)
    #     ).all()
    #
    # def resolve_users_by_subject(self, info, subject_id):
    #     return db_session.query(UserModel).join(
    #         UserModel.subjects
    #     ).filter(
    #         SubjectModel.id == subject_id
    #     ).all()
    #
    # def resolve_subjects_by_user(self, info, user_id):
    #     user = db_session.query(UserModel).get(user_id)
    #     if user:
    #         return user.subjects
    #     else:
    #         return []
    #
    # def resolve_users_by_age(self, info, age):
    #     today = date.today()
    #     birth_date = date(today.year - age, today.month, today.day)
    #     return db_session.query(UserModel).filter(
    #         UserModel.birth_date == birth_date
    #     ).all()
    #
    # def resolve_users_by_age_range(self, info, min_age=None, max_age=None):
    #     today = date.today()
    #     query = db_session.query(UserModel)
    #     if min_age is not None:
    #         max_birth_date = date(today.year - min_age, today.month, today.day)
    #         query = query.filter(UserModel.birth_date <= max_birth_date)
    #     if max_age is not None:
    #         min_birth_date = date(today.year - max_age, today.month, today.day)
    #         query = query.filter(UserModel.birth_date >= min_birth_date)
    #     return query.all()
    #
    # def resolve_users_by_birth_date(self, info, birth_date):
    #     try:
    #         birth_date_obj = datetime.strptime(birth_date, '%Y-%m-%d').date()
    #     except ValueError:
    #         return []
    #     return db_session.query(UserModel).filter(
    #         UserModel.birth_date == birth_date_obj
    #     ).all()
    #
    # def resolve_users_by_country(self, info, country):
    #     return db_session.query(UserModel).join(
    #         UserModel.address
    #     ).filter(
    #         AddressModel.country == country
    #     ).all()



# Mutations

# class AddAddress(graphene.Mutation):
#     class Arguments:
#         street = graphene.String(required=True)
#         city = graphene.String(required=True)
#         country = graphene.String(required=True)
#
#     address = graphene.Field(lambda: AddressModel)
#
#     def mutate(self, info, street, city, country):
#         new_address = AddressModel(street=street, city=city, country=country)
#         db_session.add(new_address)
#         db_session.commit()
#         return AddAddress(address=new_address)
#
#
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
